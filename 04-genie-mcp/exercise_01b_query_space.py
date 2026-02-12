"""
Exercise 01b: Genie Space 질의 (완성 코드)
생성된 Genie Space에 자연어 질의를 수행합니다.
이 코드를 실행하여 Genie 질의 API가 정상 동작하는지 확인하세요.

사용법: uv run python 04-genie-mcp/exercise_01b_query_space.py <SPACE_ID>
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


def start_conversation(space_id: str, question: str) -> dict:
    """새 Genie 대화를 시작하고 첫 질문을 보냅니다."""
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
    """결과가 준비될 때까지 점진적 백오프로 폴링합니다."""
    base_url = f"{DATABRICKS_HOST}/api/2.0/genie/spaces/{space_id}"
    url = f"{base_url}/conversations/{conversation_id}/messages/{message_id}"

    # 💡 학습 포인트: 점진적 백오프 — 초반엔 짧게, 오래 걸리면 간격을 늘림
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

        elapsed = time.time() - start
        print(f"  ⏳ 상태: {status} ({elapsed:.0f}초 경과)")
        time.sleep(interval)
        interval = min(interval * 1.5, 5.0)  # 최대 5초까지 증가

    raise TimeoutError("Genie 응답 시간 초과")


def format_result(data: dict) -> str:
    """응답에서 텍스트/SQL 결과를 추출합니다."""
    attachments = data.get("attachments", [])
    parts = []
    for att in attachments:
        if "text" in att:
            parts.append(att["text"].get("content", ""))
        if "query" in att:
            parts.append(f"SQL: {att['query'].get('query', '')}")
    return "\n".join(parts) if parts else json.dumps(data, indent=2, ensure_ascii=False)


def main():
    print("🔍 Exercise 01b: Genie Space 질의")
    print("=" * 60)
    print(f"  Space ID: {SPACE_ID}")

    question = "What is the total online revenue for 2020?"
    print(f"\n  1️⃣ 대화 시작 + 질문 전송: '{question}'")
    result = start_conversation(SPACE_ID, question)
    conversation_id = result["conversation_id"]
    message_id = result["message_id"]
    print(f"     대화 ID: {conversation_id}")
    print(f"     메시지 ID: {message_id}")

    print("  2️⃣ 결과 대기 중...")
    final = poll_result(SPACE_ID, conversation_id, message_id)
    print(f"\n✅ 결과:")
    print(f"   {format_result(final)}")

    print(f"\n💡 Tip: 생성된 Space ID를 exercise_02에서 활용할 수 있습니다.")
    print(f"   Space ID: {SPACE_ID}")


if __name__ == "__main__":
    main()
