"""
Unity Catalog MCP 서버
Unity Catalog REST API를 MCP 서버로 래핑하여 테이블 메타데이터를 조회합니다.
list_schemas, list_tables, describe_table 3개 tool을 제공합니다.

실행: uv run python 06-agents/exercise_unity_catalog_mcp.py
"""

import configparser
import json
import os
import subprocess

import httpx
from dotenv import load_dotenv
from fastmcp import FastMCP

load_dotenv()


def resolve_databricks_config() -> tuple[str, str]:
    """Databricks 인증 정보를 해석합니다. (.env → databricks CLI → 기본값)"""
    host = os.getenv("DATABRICKS_HOST", "").rstrip("/")
    token = os.getenv("DATABRICKS_TOKEN", "")

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

    return host, token


DATABRICKS_HOST, DATABRICKS_TOKEN = resolve_databricks_config()

if not all([DATABRICKS_HOST, DATABRICKS_TOKEN]):
    print("⚠️  인증 정보를 찾을 수 없습니다.")
    print("   방법 1: databricks CLI 설정 (databricks configure)")
    print("   방법 2: .env 파일 설정 (cp .env.example .env)")
    exit(1)

mcp = FastMCP("Unity Catalog MCP")

headers = {
    "Authorization": f"Bearer {DATABRICKS_TOKEN}",
}


@mcp.tool()
def list_schemas(catalog_name: str) -> str:
    """Unity Catalog에서 카탈로그 내 스키마 목록을 조회합니다.

    Args:
        catalog_name: 카탈로그 이름 (예: "main")

    Returns:
        스키마 목록 (이름, 설명 포함)
    """
    resp = httpx.get(
        f"{DATABRICKS_HOST}/api/2.1/unity-catalog/schemas",
        headers=headers,
        params={"catalog_name": catalog_name},
        timeout=30,
    )
    resp.raise_for_status()
    schemas = resp.json().get("schemas", [])

    if not schemas:
        return f"카탈로그 '{catalog_name}'에 스키마가 없습니다."

    lines = [f"📂 카탈로그 '{catalog_name}'의 스키마 목록 ({len(schemas)}개)\n"]
    for s in schemas:
        name = s.get("name", "unknown")
        comment = s.get("comment", "")
        desc = f" — {comment}" if comment else ""
        lines.append(f"  • {name}{desc}")

    return "\n".join(lines)


@mcp.tool()
def list_tables(catalog_name: str, schema_name: str) -> str:
    """Unity Catalog에서 스키마 내 테이블 목록을 조회합니다.

    Args:
        catalog_name: 카탈로그 이름 (예: "main")
        schema_name: 스키마 이름 (예: "default")

    Returns:
        테이블 목록 (이름, 타입, 설명 포함)
    """
    resp = httpx.get(
        f"{DATABRICKS_HOST}/api/2.1/unity-catalog/tables",
        headers=headers,
        params={"catalog_name": catalog_name, "schema_name": schema_name},
        timeout=30,
    )
    resp.raise_for_status()
    tables = resp.json().get("tables", [])

    if not tables:
        return f"스키마 '{catalog_name}.{schema_name}'에 테이블이 없습니다."

    lines = [f"📋 '{catalog_name}.{schema_name}'의 테이블 목록 ({len(tables)}개)\n"]
    for t in tables:
        name = t.get("name", "unknown")
        table_type = t.get("table_type", "UNKNOWN")
        comment = t.get("comment", "")
        desc = f" — {comment}" if comment else ""
        lines.append(f"  • {name} [{table_type}]{desc}")

    return "\n".join(lines)


@mcp.tool()
def describe_table(table_full_name: str) -> str:
    """Unity Catalog에서 테이블의 상세 메타데이터(컬럼, 타입, 설명)를 조회합니다.

    Args:
        table_full_name: 테이블 전체 이름 (예: "main.default.my_table")

    Returns:
        테이블 상세 정보 (컬럼 목록, 타입, 설명 포함)
    """
    resp = httpx.get(
        f"{DATABRICKS_HOST}/api/2.1/unity-catalog/tables/{table_full_name}",
        headers=headers,
        timeout=30,
    )
    resp.raise_for_status()
    table = resp.json()

    name = table.get("full_name", table_full_name)
    table_type = table.get("table_type", "UNKNOWN")
    comment = table.get("comment", "")
    columns = table.get("columns", [])

    lines = [f"📊 테이블: {name}"]
    lines.append(f"   타입: {table_type}")
    if comment:
        lines.append(f"   설명: {comment}")
    lines.append(f"   컬럼 수: {len(columns)}개\n")

    if columns:
        lines.append("   컬럼 목록:")
        for col in columns:
            col_name = col.get("name", "unknown")
            col_type = col.get("type_name", "UNKNOWN")
            col_comment = col.get("comment", "")
            col_desc = f" — {col_comment}" if col_comment else ""
            nullable = "nullable" if col.get("nullable", True) else "not null"
            lines.append(f"     • {col_name} ({col_type}, {nullable}){col_desc}")

    return "\n".join(lines)


if __name__ == "__main__":
    mcp.run()
