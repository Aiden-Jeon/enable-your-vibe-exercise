"""
Genie MCP 서버 (코딩 실습)
Databricks Genie를 MCP 서버로 래핑하여 Claude Code에서 사용할 수 있게 합니다.
Space 생성, 질의, 후속 질의 3개 tool을 제공합니다.

genie_helpers.py에 헬퍼 함수가 제공되어 있습니다.
MCP tool 3개만 구현하세요.

실행: uv run python 04-genie-mcp/exercise_genie_mcp_server.py
"""

from fastmcp import FastMCP
from genie_helpers import (
    DATABRICKS_HOST,
    DATABRICKS_TOKEN,
    WAREHOUSE_ID,
    headers,
    build_serialized_space,
    create_genie_space as _create_genie_space,
    start_conversation,
    poll_result,
    send_and_poll,
    format_result,
)

if not all([DATABRICKS_HOST, DATABRICKS_TOKEN, WAREHOUSE_ID]):
    print("⚠️  인증 정보를 찾을 수 없습니다.")
    print("   방법 1: databricks CLI 설정 (databricks configure)")
    print("   방법 2: .env 파일 설정 (cp .env.example .env)")
    print("   필요: DATABRICKS_HOST, DATABRICKS_TOKEN, WAREHOUSE_ID")
    exit(1)

mcp = FastMCP("Genie MCP")


# ============================================================
# MCP Tools — 아래 3개 tool을 구현하세요
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
    # TODO: build_serialized_space()로 serialized_space 생성 후 _create_genie_space() 호출
    # 힌트:
    # - build_serialized_space(tables, instructions or [], sample_questions or [], ...)
    # - _create_genie_space(title, description, warehouse_id, serialized_space)
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
    # TODO: start_conversation()으로 새 대화 시작 후 poll_result()로 결과 조회
    # 힌트:
    # - result = start_conversation(space_id, question)
    # - conversation_id, message_id 추출
    # - poll_result()로 결과 대기
    # - format_result()로 포맷 후 conversation_id 포함하여 반환
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
    # TODO: send_and_poll()로 후속 질문 전송 후 format_result()로 포맷
    # 힌트:
    # - result = send_and_poll(space_id, conversation_id, question)
    # - format_result(result) 반환
    raise NotImplementedError("continue_conversation을 구현하세요")


if __name__ == "__main__":
    mcp.run()
