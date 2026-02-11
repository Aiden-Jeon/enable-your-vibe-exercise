"""
Exercise 01b: Genie Space 질의
생성된 Genie Space에 자연어 질의를 수행합니다.

요구사항:
1. create_conversation(): 새 대화 생성
2. send_message(): 자연어 질문 전송
3. poll_result(): 점진적 백오프로 결과 폴링
4. format_result(): 응답에서 텍스트/SQL 추출

사용법: python exercise_01b_query_space.py <SPACE_ID>
"""

import configparser
import json
import os
import subprocess
import sys
import time

import httpx
from dotenv import load_dotenv

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


DATABRICKS_HOST, DATABRICKS_TOKEN, _ = resolve_databricks_config()

if not all([DATABRICKS_HOST, DATABRICKS_TOKEN]):
    print("⚠️  인증 정보를 찾을 수 없습니다.")
    print("   방법 1: databricks CLI 설정 (databricks configure)")
    print("   방법 2: .env 파일 설정 (cp .env.example .env)")
    exit(1)

if len(sys.argv) < 2:
    print("⚠️  사용법: python exercise_01b_query_space.py <SPACE_ID>")
    print("   exercise_01a_create_space.py를 먼저 실행하여 Space ID를 얻으세요.")
    exit(1)

SPACE_ID = sys.argv[1]

headers = {
    "Authorization": f"Bearer {DATABRICKS_TOKEN}",
    "Content-Type": "application/json",
}


def create_conversation(space_id: str) -> str:
    """새 Genie 대화를 생성합니다.

    Args:
        space_id: Genie Space ID

    Returns:
        conversation_id 문자열
    """
    # TODO: 새 대화를 생성하세요
    # 힌트:
    # - POST {DATABRICKS_HOST}/api/2.0/genie/spaces/{space_id}/conversations
    # - 응답에서 conversation_id를 반환
    raise NotImplementedError("create_conversation을 구현하세요")


def send_message(space_id: str, conversation_id: str, question: str) -> dict:
    """Genie에 자연어 질문을 보냅니다.

    Args:
        space_id: Genie Space ID
        conversation_id: 대화 ID
        question: 자연어 질문

    Returns:
        API 응답 딕셔너리 (message_id 포함)
    """
    # TODO: 메시지를 전송하세요
    # 힌트:
    # - POST {base_url}/conversations/{conversation_id}/messages
    # - body: {"content": question}
    raise NotImplementedError("send_message를 구현하세요")


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
        max_wait: 최대 대기 시간(초)

    Returns:
        완료된 응답 딕셔너리
    """
    # TODO: 점진적 백오프 폴링을 구현하세요
    # 힌트:
    # - GET {base_url}/conversations/{conversation_id}/messages/{message_id}
    # - status가 "COMPLETED"이면 반환
    # - status가 "FAILED" 또는 "CANCELLED"이면 RuntimeError 발생
    # - 폴링 간격: 1초 시작 → 최대 5초까지 1.5배씩 증가
    raise NotImplementedError("poll_result를 구현하세요")


def format_result(data: dict) -> str:
    """응답에서 텍스트/SQL 결과를 추출합니다.

    Args:
        data: poll_result()의 반환값

    Returns:
        포맷된 결과 문자열
    """
    # TODO: 응답을 파싱하여 텍스트/SQL을 추출하세요
    # 힌트:
    # - data["attachments"]에서 "text"와 "query" 추출
    # - text: att["text"]["content"]
    # - query: att["query"]["query"]
    raise NotImplementedError("format_result를 구현하세요")


def main():
    print("🔍 Exercise 01b: Genie Space 질의")
    print("=" * 60)
    print(f"  Space ID: {SPACE_ID}")

    print("\n  1️⃣ 대화 생성 중...")
    conversation_id = create_conversation(SPACE_ID)
    print(f"     대화 ID: {conversation_id}")

    question = "What is the total online revenue for 2020?"
    print(f"  2️⃣ 질문 전송: '{question}'")
    result = send_message(SPACE_ID, conversation_id, question)
    message_id = result["message_id"]
    print(f"     메시지 ID: {message_id}")

    print("  3️⃣ 결과 대기 중...")
    final = poll_result(SPACE_ID, conversation_id, message_id)
    print(f"\n✅ 결과:")
    print(f"   {format_result(final)}")

    print(f"\n💡 Tip: 생성된 Space ID를 exercise_02에서 활용할 수 있습니다.")
    print(f"   Space ID: {SPACE_ID}")


if __name__ == "__main__":
    main()
