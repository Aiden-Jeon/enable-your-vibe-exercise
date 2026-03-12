"""
Genie API 헬퍼 함수 모음 (완성 코드)
Databricks Genie Space 생성 및 질의에 필요한 유틸리티를 제공합니다.

exercise_genie_mcp_server.py에서 import하여 사용합니다.
"""

import configparser
import json
import os
import subprocess
import time
from uuid import uuid4

import httpx
from dotenv import load_dotenv

load_dotenv()


# ============================================================
# 인증 설정
# ============================================================


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
            profile = cfg["e2-demo-field-eng"] if "e2-demo-field-eng" in cfg else {}
            if not host:
                host = profile.get("host", "").rstrip("/")
            if not token and host:
                result = subprocess.run(
                    ["databricks", "auth", "token", "--host", host, "-p", "e2-demo-field-eng"],
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

headers = {
    "Authorization": f"Bearer {DATABRICKS_TOKEN}",
    "Content-Type": "application/json",
}


# ============================================================
# Space 생성 헬퍼
# ============================================================


def build_serialized_space(
    tables: list[dict],
    instructions: list[str],
    sample_questions: list[str],
    example_sqls: list[dict],
    join_specs: list[dict] | None = None,
    sql_snippets: dict | None = None,
) -> str:
    """Genie Space용 serialized_space(protobuf v2 JSON)를 생성합니다.

    Args:
        tables: [{"catalog": "...", "schema": "...", "table": "..."}]
        instructions: 텍스트 지시사항 리스트
        sample_questions: 예제 질문 리스트
        example_sqls: [{"question": "...", "sql": "..."}]
        join_specs: 테이블 간 조인 조건 리스트
        sql_snippets: SQL 스니펫 (expressions, measures, filters)

    Returns:
        protobuf v2 형식의 JSON 문자열
    """
    inst_block: dict = {
        "text_instructions": [
            {"id": uuid4().hex, "content": instructions}
        ] if instructions else [],
        "example_question_sqls": sorted(
            [
                {
                    "id": uuid4().hex,
                    "question": [ex["question"]],
                    "sql": [ex["sql"]],
                }
                for ex in example_sqls
            ],
            key=lambda x: x["id"],
        ),
    }

    if join_specs:
        inst_block["join_specs"] = join_specs

    if sql_snippets:
        sorted_snippets = {}
        for category, items in sql_snippets.items():
            sorted_snippets[category] = sorted(items, key=lambda x: x["id"])
        inst_block["sql_snippets"] = sorted_snippets

    proto = {
        "version": 2,
        "data_sources": {
            "tables": sorted(
                [
                    {"identifier": f"{t['catalog']}.{t['schema']}.{t['table']}"}
                    for t in tables
                ],
                key=lambda x: x["identifier"],
            )
        },
        "config": {
            "sample_questions": sorted(
                [{"id": uuid4().hex, "question": [q]} for q in sample_questions],
                key=lambda x: x["id"],
            )
        },
        "instructions": inst_block,
    }
    return json.dumps(proto)


def create_genie_space(
    title: str,
    description: str,
    warehouse_id: str,
    serialized_space: str,
) -> dict:
    """POST /api/2.0/genie/spaces로 Space를 생성합니다.

    Args:
        title: Space 제목
        description: Space 설명
        warehouse_id: SQL Warehouse ID
        serialized_space: build_serialized_space()의 반환값

    Returns:
        API 응답 딕셔너리 (space_id 포함)
    """
    resp = httpx.post(
        f"{DATABRICKS_HOST}/api/2.0/genie/spaces",
        headers=headers,
        json={
            "title": title,
            "description": description,
            "warehouse_id": warehouse_id,
            "serialized_space": serialized_space,
        },
    )
    if resp.status_code >= 400:
        print(f"  ❌ API Error {resp.status_code}: {resp.text}")
    resp.raise_for_status()
    return resp.json()


# ============================================================
# 질의 헬퍼
# ============================================================


def start_conversation(space_id: str, question: str) -> dict:
    """새 Genie 대화를 시작하고 첫 질문을 보냅니다.

    Args:
        space_id: Genie Space ID
        question: 자연어 질문

    Returns:
        API 응답 딕셔너리 (conversation_id, message_id 포함)
    """
    base_url = f"{DATABRICKS_HOST}/api/2.0/genie/spaces/{space_id}"
    resp = httpx.post(
        f"{base_url}/start-conversation",
        headers=headers,
        json={"content": question},
    )
    if resp.status_code >= 400:
        print(f"  ❌ API Error {resp.status_code}: {resp.text}")
    resp.raise_for_status()
    return resp.json()


def poll_result(
    space_id: str,
    conversation_id: str,
    message_id: str,
    max_wait: int = 120,
) -> dict:
    """결과가 준비될 때까지 점진적 백오프로 폴링합니다.

    Args:
        space_id: Genie Space ID
        conversation_id: 대화 ID
        message_id: 메시지 ID
        max_wait: 최대 대기 시간 (초)

    Returns:
        완료된 응답 딕셔너리

    Raises:
        RuntimeError: 질의 실패 시
        TimeoutError: 응답 시간 초과 시
    """
    base_url = f"{DATABRICKS_HOST}/api/2.0/genie/spaces/{space_id}"
    url = f"{base_url}/conversations/{conversation_id}/messages/{message_id}"

    start = time.time()
    interval = 1.0
    while time.time() - start < max_wait:
        resp = httpx.get(url, headers=headers)
        resp.raise_for_status()
        data = resp.json()
        status = data.get("status", "")

        if status == "COMPLETED":
            return data
        if status in ("FAILED", "CANCELLED"):
            raise RuntimeError(f"Genie 질의 실패: {status}")

        time.sleep(interval)
        interval = min(interval * 1.5, 5.0)

    raise TimeoutError("Genie 응답 시간 초과")


def send_and_poll(
    space_id: str,
    conversation_id: str,
    question: str,
    max_wait: int = 120,
) -> dict:
    """기존 대화에 메시지를 전송하고 점진적 백오프로 결과를 폴링합니다.

    Args:
        space_id: Genie Space ID
        conversation_id: 대화 ID
        question: 자연어 질문
        max_wait: 최대 대기 시간 (초)

    Returns:
        완료된 응답 딕셔너리 또는 {"error": "..."} 딕셔너리
    """
    base_url = f"{DATABRICKS_HOST}/api/2.0/genie/spaces/{space_id}"
    try:
        resp = httpx.post(
            f"{base_url}/conversations/{conversation_id}/messages",
            headers=headers,
            json={"content": question},
        )
        resp.raise_for_status()
        message_id = resp.json()["id"]
    except Exception as e:
        return {"error": f"메시지 전송 실패: {e}"}

    try:
        return poll_result(space_id, conversation_id, message_id, max_wait)
    except (RuntimeError, TimeoutError) as e:
        return {"error": str(e)}


def format_result(data: dict) -> str:
    """응답에서 텍스트/SQL 결과를 추출합니다.

    Args:
        data: poll_result() 또는 send_and_poll()의 반환값

    Returns:
        포맷된 결과 문자열
    """
    if "error" in data:
        return f"❌ {data['error']}"

    attachments = data.get("attachments", [])
    parts = []
    for att in attachments:
        if "text" in att:
            parts.append(att["text"].get("content", ""))
        if "query" in att:
            parts.append(f"SQL: {att['query'].get('query', '')}")
    return "\n".join(parts) if parts else json.dumps(data, indent=2, ensure_ascii=False)
