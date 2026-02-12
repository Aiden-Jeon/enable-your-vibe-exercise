"""
Exercise 02: Genie MCP 서버 (코딩 실습)
Databricks Genie를 MCP 서버로 래핑하여 Claude Code에서 사용할 수 있게 합니다.
Space 생성, 질의, 후속 질의 3개 tool을 제공합니다.

Exercise 01a/01b의 완성 코드를 참고하여 구현하세요.

실행: uv run python 04-genie-mcp/exercise_02_genie_mcp_server.py
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
    """protobuf v2 JSON 형식의 serialized_space를 생성합니다.

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
    # TODO: protobuf v2 JSON 형식의 serialized_space를 생성하세요
    # 참고: exercise_01a_create_space.py의 build_serialized_space()
    # 힌트:
    # - text_instructions: 모든 instruction을 하나의 항목으로 병합
    #   [{"id": uuid4().hex, "content": instructions}] if instructions else []
    # - 모든 id 기반 리스트를 id 기준으로 정렬
    # - sql_snippets 내부 각 카테고리도 id 기준 정렬
    # - data_sources.tables는 identifier 기준 정렬
    raise NotImplementedError("_build_serialized_space를 구현하세요")


def _send_and_poll(space_id: str, conversation_id: str, question: str) -> dict:
    """메시지를 전송하고 점진적 백오프로 결과를 폴링합니다.

    Args:
        space_id: Genie Space ID
        conversation_id: 대화 ID
        question: 자연어 질문

    Returns:
        완료된 응답 딕셔너리 또는 {"error": "..."} 딕셔너리
    """
    # TODO: 메시지 전송 + 점진적 백오프 폴링을 구현하세요
    # 참고: exercise_01b_query_space.py의 send_message() + poll_result()
    # 힌트:
    # - POST messages → message_id 획득
    # - GET messages/{message_id} 반복 조회
    # - 폴링 간격: 1초 → 최대 5초 (1.5배 증가)
    # - COMPLETED → 결과 반환, FAILED/CANCELLED → error dict 반환
    # - 120초 초과 → error dict 반환
    raise NotImplementedError("_send_and_poll을 구현하세요")


def _format_response(result: dict) -> str:
    """Genie 응답에서 텍스트/SQL 결과를 추출합니다.

    Args:
        result: _send_and_poll()의 반환값

    Returns:
        포맷된 결과 문자열
    """
    # TODO: 응답을 파싱하여 텍스트/SQL을 추출하세요
    # 참고: exercise_01b_query_space.py의 format_result()
    # 힌트:
    # - "error" 키가 있으면 에러 메시지 반환
    # - attachments에서 text.content와 query.query 추출
    raise NotImplementedError("_format_response를 구현하세요")


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
        sql_snippets: SQL 스니펫 (expressions, measures, filters)

    Returns:
        생성된 Space 정보 (space_id 포함)
    """
    # TODO: _build_serialized_space()로 serialized_space 생성 후 API 호출
    # 참고: exercise_01a_create_space.py의 create_genie_space()
    # 힌트:
    # - POST {DATABRICKS_HOST}/api/2.0/genie/spaces
    # - 결과에서 space_id 추출하여 메시지 반환
    raise NotImplementedError("create_genie_space를 구현하세요")


@mcp.tool()
def ask_genie(space_id: str, question: str) -> str:
    """Databricks Genie에 자연어로 데이터를 질의합니다. 새 대화를 시작합니다.

    Args:
        space_id: Genie Space ID
        question: 데이터에 대한 자연어 질문 (예: '이번 달 매출은?')

    Returns:
        Genie의 응답 결과 (텍스트 + SQL)
    """
    # TODO: 새 대화 생성 후 _send_and_poll()로 질의하세요
    # 참고: exercise_01b_query_space.py의 create_conversation() + send/poll 흐름
    # 힌트:
    # - POST {base_url}/conversations → conversation_id
    # - _send_and_poll() 호출
    # - _format_response()로 포맷 후 conversation_id 포함하여 반환
    raise NotImplementedError("ask_genie를 구현하세요")


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
    # TODO: 기존 대화에 후속 질문을 보내세요
    # 참고: exercise_01b_query_space.py의 send/poll 흐름
    # 힌트: _send_and_poll() + _format_response() 사용
    raise NotImplementedError("continue_conversation을 구현하세요")


if __name__ == "__main__":
    mcp.run()
