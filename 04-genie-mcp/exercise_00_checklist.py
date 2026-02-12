"""
Exercise 00: 사전 환경 체크리스트
Genie MCP 실습 전 환경 설정이 올바른지 검증합니다.

실행: python exercise_00_checklist.py
"""

import configparser
import json
import os
import subprocess
import sys

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


DATABRICKS_HOST, DATABRICKS_TOKEN, WAREHOUSE_ID = resolve_databricks_config()

HTTP_TIMEOUT = 60.0
WAIT_TIMEOUT = "30s"


def mask_token(token: str) -> str:
    """토큰을 마스킹하여 표시합니다. (예: ****...abcd)"""
    if len(token) <= 4:
        return "****"
    return f"****...{token[-4:]}"


# ── Step 1: 환경변수 확인 ──────────────────────────────────────────


def check_auth_info() -> tuple[bool, str]:
    """DATABRICKS_HOST, DATABRICKS_TOKEN, WAREHOUSE_ID 존재를 확인합니다."""
    missing = []
    if not DATABRICKS_HOST:
        missing.append("DATABRICKS_HOST")
    if not DATABRICKS_TOKEN:
        missing.append("DATABRICKS_TOKEN")
    if not WAREHOUSE_ID:
        missing.append("WAREHOUSE_ID")

    if missing:
        return False, (
            f"누락: {', '.join(missing)}\n"
            "   → .env 파일을 확인하거나, databricks CLI를 설정해주세요\n"
            "     (databricks configure)"
        )

    # 인증 출처 판별
    env_host = os.getenv("DATABRICKS_HOST", "")
    env_token = os.getenv("DATABRICKS_TOKEN", "")
    env_wh = os.getenv("WAREHOUSE_ID", "")

    if env_host and env_token:
        host_source = ".env"
    elif DATABRICKS_HOST == "https://e2-demo-field-eng.cloud.databricks.com" and not env_host:
        host_source = "기본값"
    else:
        host_source = "databricks CLI"

    wh_source = ".env" if env_wh else "API 자동 조회"

    lines = [
        f"DATABRICKS_HOST  = {DATABRICKS_HOST}",
        f"DATABRICKS_TOKEN = {mask_token(DATABRICKS_TOKEN)}",
        f"WAREHOUSE_ID     = {WAREHOUSE_ID}",
        f"인증 출처: HOST/TOKEN={host_source}, WAREHOUSE={wh_source}",
    ]
    return True, "\n     ".join(lines)


# ── Step 2: Databricks 호스트 연결 ─────────────────────────────────


def check_host_connection() -> tuple[bool, str]:
    """GET /api/2.0/clusters/spark-versions 로 호스트 연결을 확인합니다."""
    headers = {
        "Authorization": f"Bearer {DATABRICKS_TOKEN}",
    }
    try:
        resp = httpx.get(
            f"{DATABRICKS_HOST}/api/2.0/clusters/spark-versions",
            headers=headers,
            timeout=HTTP_TIMEOUT,
        )
        resp.raise_for_status()
        return True, f"{DATABRICKS_HOST} 연결 성공"
    except httpx.ConnectError:
        return False, f"호스트에 연결할 수 없습니다: {DATABRICKS_HOST}\n   → URL을 확인해주세요"
    except httpx.HTTPStatusError as e:
        if e.response.status_code == 401:
            return False, "인증 실패 (401) → DATABRICKS_TOKEN을 확인해주세요"
        if e.response.status_code == 403:
            return False, "권한 부족 (403) → 워크스페이스 접근 권한을 확인해주세요"
        return False, f"HTTP 오류 {e.response.status_code}: {e.response.text[:200]}"
    except httpx.TimeoutException:
        return False, f"연결 시간 초과 ({HTTP_TIMEOUT}s) → 네트워크 상태를 확인해주세요"


# ── Step 3: SQL Warehouse 접근 ─────────────────────────────────────


def check_warehouse() -> tuple[bool, str]:
    """POST /api/2.0/sql/statements 로 SQL Warehouse 접근을 확인합니다."""
    headers = {
        "Authorization": f"Bearer {DATABRICKS_TOKEN}",
        "Content-Type": "application/json",
    }
    try:
        resp = httpx.post(
            f"{DATABRICKS_HOST}/api/2.0/sql/statements",
            headers=headers,
            json={
                "warehouse_id": WAREHOUSE_ID,
                "statement": "SELECT 1",
                "wait_timeout": WAIT_TIMEOUT,
            },
            timeout=HTTP_TIMEOUT,
        )
        resp.raise_for_status()
        data = resp.json()
        status = data.get("status", {}).get("state", "UNKNOWN")
        if status == "SUCCEEDED":
            return True, f"Warehouse {WAREHOUSE_ID} 정상 작동"
        return False, f"쿼리 상태: {status} → Warehouse가 실행 중인지 확인해주세요"
    except httpx.HTTPStatusError as e:
        body = e.response.text[:300]
        if "RESOURCE_DOES_NOT_EXIST" in body or "does not exist" in body.lower():
            return False, f"Warehouse를 찾을 수 없습니다: {WAREHOUSE_ID}\n   → WAREHOUSE_ID를 확인해주세요"
        return False, f"HTTP 오류 {e.response.status_code}: {body}"
    except httpx.TimeoutException:
        return False, f"쿼리 시간 초과 ({HTTP_TIMEOUT}s) → Warehouse 콜드스타트 중일 수 있습니다. 잠시 후 다시 시도해주세요"


# ── Step 4: 데이터 스키마 확인 ─────────────────────────────────────


def check_schema() -> tuple[bool, str]:
    """shared.fashion_recommendations 스키마에 필요한 테이블이 있는지 확인합니다."""
    headers = {
        "Authorization": f"Bearer {DATABRICKS_TOKEN}",
        "Content-Type": "application/json",
    }
    required_tables = {"transactions", "customers"}

    try:
        resp = httpx.post(
            f"{DATABRICKS_HOST}/api/2.0/sql/statements",
            headers=headers,
            json={
                "warehouse_id": WAREHOUSE_ID,
                "statement": "SHOW TABLES IN shared.fashion_recommendations",
                "wait_timeout": WAIT_TIMEOUT,
            },
            timeout=HTTP_TIMEOUT,
        )
        resp.raise_for_status()
        data = resp.json()
        status = data.get("status", {}).get("state", "UNKNOWN")

        if status != "SUCCEEDED":
            return False, f"쿼리 상태: {status} → shared.fashion_recommendations 스키마 접근 권한을 확인해주세요"

        # 결과에서 테이블명 추출
        columns = [col["name"] for col in data.get("manifest", {}).get("schema", {}).get("columns", [])]
        table_name_idx = columns.index("tableName") if "tableName" in columns else 0

        found_tables = set()
        for row in data.get("result", {}).get("data_array", []):
            found_tables.add(row[table_name_idx])

        missing = required_tables - found_tables
        if missing:
            return False, f"누락된 테이블: {', '.join(sorted(missing))}\n   → shared.fashion_recommendations 스키마에 데이터가 있는지 확인해주세요"

        return True, f"테이블 확인 완료: {', '.join(sorted(required_tables))}"

    except httpx.HTTPStatusError as e:
        body = e.response.text[:300]
        if "SCHEMA_NOT_FOUND" in body or "not found" in body.lower():
            return False, "스키마를 찾을 수 없습니다: shared.fashion_recommendations\n   → 카탈로그/스키마 접근 권한을 확인해주세요"
        return False, f"HTTP 오류 {e.response.status_code}: {body}"
    except httpx.TimeoutException:
        return False, f"쿼리 시간 초과 ({HTTP_TIMEOUT}s) → 잠시 후 다시 시도해주세요"


# ── 메인 실행 ──────────────────────────────────────────────────────


STEPS: list[tuple[str, callable]] = [
    ("인증 정보 확인", check_auth_info),
    ("Databricks 호스트 연결", check_host_connection),
    ("SQL Warehouse 접근", check_warehouse),
    ("데이터 스키마 확인", check_schema),
]


def main():
    print("🔍 Exercise 00: Genie MCP 사전 환경 체크리스트")
    print("=" * 60)

    all_passed = True

    for i, (label, check_fn) in enumerate(STEPS, 1):
        print(f"\n  {i}️⃣  {label}...")

        if not all_passed:
            print(f"     ⏭️  건너뜀 (이전 단계 실패)")
            continue

        ok, message = check_fn()
        if ok:
            print(f"     ✅ {message}")
        else:
            print(f"     ❌ {message}")
            all_passed = False

    print("\n" + "=" * 60)
    if all_passed:
        print("✅ 모든 환경 설정이 정상입니다!")
        print(f"   Warehouse ID: {WAREHOUSE_ID}")
        print(f"\n💡 다음 단계: exercise_01a로 Genie Space를 생성하세요")
        print(f"   python exercise_01a_create_space.py")
    else:
        print("❌ 환경 설정에 문제가 있습니다. 위 메시지를 확인해주세요.")
        sys.exit(1)


if __name__ == "__main__":
    main()
