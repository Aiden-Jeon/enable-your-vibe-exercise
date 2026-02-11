"""
Exercise 02: Genie MCP 서버
Databricks Genie를 MCP 서버로 래핑하여 Claude Code에서 사용할 수 있게 합니다.
Space 생성, 질의, 후속 질의 3개 tool을 제공합니다.

실행: python exercise_02_genie_mcp_server.py
"""

import configparser
import json
import os
import subprocess
import time
from uuid import uuid4

import httpx
from dotenv import load_dotenv
from fastmcp import FastMCP

load_dotenv()


def resolve_databricks_config() -> tuple[str, str, str]:
    """Databricks 인증 정보를 해석합니다. (.env → databricks CLI → 기본값)"""
    host = os.getenv("DATABRICKS_HOST", "").rstrip("/")
    token = os.getenv("DATABRICKS_TOKEN", "")
    warehouse_id = os.getenv("WAREHOUSE_ID", "")

    # databricks CLI fallback
    if not host or not token:
        try:
            cfg = configparser.ConfigParser()
            cfg.read(os.path.expanduser("~/.databrickscfg"))
            profile = cfg["DEFAULT"] if "DEFAULT" in cfg else {}
            if not host:
                host = profile.get("host", "").rstrip("/")
            if not token and host:
                result = subprocess.run(
                    ["databricks", "auth", "token", "--host", host],
                    capture_output=True,
                    text=True,
                    timeout=10,
                )
                if result.returncode == 0:
                    token = json.loads(result.stdout).get("access_token", "")
        except Exception:
            pass

    # 기본 호스트
    if not host:
        host = "https://e2-demo-field-eng.cloud.databricks.com"

    # Warehouse 자동 조회
    if not warehouse_id and host and token:
        try:
            resp = httpx.get(
                f"{host}/api/2.0/sql/warehouses",
                headers={"Authorization": f"Bearer {token}"},
                timeout=10,
            )
            resp.raise_for_status()
            warehouses = resp.json().get("warehouses", [])
            for wh in warehouses:
                if wh.get("state") == "RUNNING":
                    warehouse_id = wh["id"]
                    break
            if not warehouse_id and warehouses:
                warehouse_id = warehouses[0]["id"]
        except Exception:
            pass

    return host, token, warehouse_id


DATABRICKS_HOST, DATABRICKS_TOKEN, WAREHOUSE_ID = resolve_databricks_config()

if not all([DATABRICKS_HOST, DATABRICKS_TOKEN, WAREHOUSE_ID]):
    print("⚠️  인증 정보를 찾을 수 없습니다.")
    print("   방법 1: databricks CLI 설정 (databricks configure)")
    print("   방법 2: .env 파일 설정 (cp .env.example .env)")
    exit(1)

mcp = FastMCP("Genie MCP")

headers = {
    "Authorization": f"Bearer {DATABRICKS_TOKEN}",
    "Content-Type": "application/json",
}


# ============================================================
# 내부 헬퍼 함수
# ============================================================


def _build_serialized_space(
    tables: list[dict],
    instructions: list[str],
    sample_questions: list[str],
    example_sqls: list[dict],
    join_specs: list[dict] | None = None,
    sql_snippets: dict | None = None,
) -> str:
    """protobuf v2 JSON 형식의 serialized_space를 생성합니다."""
    inst_block: dict = {
        "text_instructions": [
            {"id": uuid4().hex, "content": [inst]} for inst in instructions
        ],
        "example_question_sqls": [
            {
                "id": uuid4().hex,
                "question": [ex["question"]],
                "sql": [ex["sql"]],
            }
            for ex in example_sqls
        ],
    }

    if join_specs:
        inst_block["join_specs"] = join_specs

    if sql_snippets:
        inst_block["sql_snippets"] = sql_snippets

    proto = {
        "version": 2,
        "data_sources": {
            "tables": [
                {"identifier": f"{t['catalog']}.{t['schema']}.{t['table']}"}
                for t in tables
            ]
        },
        "config": {
            "sample_questions": [
                {"id": uuid4().hex, "question": [q]} for q in sample_questions
            ]
        },
        "instructions": inst_block,
    }
    return json.dumps(proto)


def _send_and_poll(space_id: str, conversation_id: str, question: str) -> dict:
    """메시지를 전송하고 점진적 백오프로 결과를 폴링합니다."""
    base_url = f"{DATABRICKS_HOST}/api/2.0/genie/spaces/{space_id}"
    resp = httpx.post(
        f"{base_url}/conversations/{conversation_id}/messages",
        headers=headers,
        json={"content": question},
    )
    resp.raise_for_status()
    message_id = resp.json()["message_id"]

    url = f"{base_url}/conversations/{conversation_id}/messages/{message_id}"
    start = time.time()
    interval = 1.0
    max_wait = 120

    while time.time() - start < max_wait:
        resp = httpx.get(url, headers=headers)
        resp.raise_for_status()
        data = resp.json()
        status = data.get("status", "")
        if status == "COMPLETED":
            return data
        if status in ("FAILED", "CANCELLED"):
            return {"error": f"질의 실패: {status}"}
        time.sleep(interval)
        interval = min(interval * 1.5, 5.0)

    return {"error": "응답 시간 초과 (120초)"}


def _format_response(result: dict) -> str:
    """Genie 응답에서 텍스트/SQL 결과를 추출합니다."""
    if "error" in result:
        return f"오류: {result['error']}"

    attachments = result.get("attachments", [])
    parts = []
    for att in attachments:
        if "text" in att:
            parts.append(att["text"].get("content", ""))
        if "query" in att:
            parts.append(f"SQL: {att['query'].get('query', '')}")
    return "\n".join(parts) if parts else json.dumps(result, indent=2, ensure_ascii=False)


# ============================================================
# MCP Tools
# ============================================================


@mcp.tool()
def create_genie_space(
    title: str,
    description: str,
    warehouse_id: str,
    tables: list[dict],
    instructions: list[str] | None = None,
    sample_questions: list[str] | None = None,
    example_sqls: list[dict] | None = None,
    join_specs: list[dict] | None = None,
    sql_snippets: dict | None = None,
) -> str:
    """Databricks Genie Space를 생성합니다.

    Args:
        title: Space 제목
        description: Space 설명
        warehouse_id: SQL Warehouse ID
        tables: 포함할 테이블 목록 [{"catalog": "...", "schema": "...", "table": "..."}]
        instructions: 텍스트 지시사항 (예: ["한국어로 답변해주세요"])
        sample_questions: 예제 질문 (예: ["총 매출은?"])
        example_sqls: 예제 SQL [{"question": "...", "sql": "..."}]
        join_specs: 테이블 간 조인 조건 리스트
            [{"left": {"table": "...", "column": "..."}, "right": {...}, "sql": ["..."]}]
        sql_snippets: SQL 스니펫 (expressions, measures, filters)
            {"expressions": [...], "measures": [...], "filters": [...]}

    Returns:
        생성된 Space 정보 (space_id 포함)
    """
    serialized = _build_serialized_space(
        tables=tables,
        instructions=instructions or [],
        sample_questions=sample_questions or [],
        example_sqls=example_sqls or [],
        join_specs=join_specs,
        sql_snippets=sql_snippets,
    )

    resp = httpx.post(
        f"{DATABRICKS_HOST}/api/2.0/genie/spaces",
        headers=headers,
        json={
            "title": title,
            "description": description,
            "warehouse_id": warehouse_id,
            "serialized_space": serialized,
        },
    )
    resp.raise_for_status()
    data = resp.json()
    space_id = data.get("space_id", "unknown")
    return f"Space 생성 완료\nSpace ID: {space_id}\nTitle: {title}"


@mcp.tool()
def ask_genie(space_id: str, question: str) -> str:
    """Databricks Genie에 자연어로 데이터를 질의합니다. 새 대화를 시작합니다.

    Args:
        space_id: Genie Space ID
        question: 데이터에 대한 자연어 질문 (예: '이번 달 매출은?')

    Returns:
        Genie의 응답 결과 (텍스트 + SQL)
    """
    base_url = f"{DATABRICKS_HOST}/api/2.0/genie/spaces/{space_id}"
    resp = httpx.post(f"{base_url}/conversations", headers=headers)
    resp.raise_for_status()
    conversation_id = resp.json()["conversation_id"]

    result = _send_and_poll(space_id, conversation_id, question)
    response = _format_response(result)
    return f"{response}\n\n(conversation_id: {conversation_id})"


@mcp.tool()
def continue_conversation(
    space_id: str,
    conversation_id: str,
    question: str,
) -> str:
    """기존 Genie 대화에 후속 질문을 합니다.

    Args:
        space_id: Genie Space ID
        conversation_id: 기존 대화 ID (ask_genie 결과에서 확인)
        question: 후속 질문 (예: '월별로 나눠서 보여줘')

    Returns:
        Genie의 응답 결과
    """
    result = _send_and_poll(space_id, conversation_id, question)
    return _format_response(result)


if __name__ == "__main__":
    mcp.run()
