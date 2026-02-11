"""
Exercise 01a: Genie Space 생성
Databricks Genie Space를 API로 생성합니다.

요구사항:
1. build_serialized_space(): protobuf v2 JSON 형식의 serialized_space 생성
2. create_genie_space(): POST /api/2.0/genie/spaces로 Space 생성

실행: python exercise_01a_create_space.py
"""

import configparser
import json
import os
import subprocess
from uuid import uuid4

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


DATABRICKS_HOST, DATABRICKS_TOKEN, WAREHOUSE_ID = resolve_databricks_config()

if not all([DATABRICKS_HOST, DATABRICKS_TOKEN, WAREHOUSE_ID]):
    print("⚠️  인증 정보를 찾을 수 없습니다.")
    print("   방법 1: databricks CLI 설정 (databricks configure)")
    print("   방법 2: .env 파일 설정 (cp .env.example .env)")
    print("   필요: DATABRICKS_HOST, DATABRICKS_TOKEN, WAREHOUSE_ID")
    exit(1)

headers = {
    "Authorization": f"Bearer {DATABRICKS_TOKEN}",
    "Content-Type": "application/json",
}


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
            [{"left": {"table": "...", "column": "..."}, "right": {...}, "sql": ["..."]}]
        sql_snippets: SQL 스니펫 (expressions, measures, filters)
            {"expressions": [...], "measures": [...], "filters": [...]}

    Returns:
        protobuf v2 형식의 JSON 문자열
    """
    # TODO: protobuf v2 JSON 형식의 serialized_space를 생성하세요
    # 힌트:
    # - text_instructions: [{"id": uuid4().hex, "content": [inst]} for inst in instructions]
    # - example_question_sqls: [{"id": uuid4().hex, "question": [...], "sql": [...]} for ex in example_sqls]
    # - data_sources.tables: [{"identifier": "catalog.schema.table"}]
    # - config.sample_questions: [{"id": uuid4().hex, "question": [q]}]
    # - join_specs와 sql_snippets가 있으면 instructions에 추가
    # - json.dumps()로 직렬화하여 반환
    raise NotImplementedError("build_serialized_space를 구현하세요")


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
    # TODO: Genie Space 생성 API를 호출하세요
    # 힌트:
    # - POST {DATABRICKS_HOST}/api/2.0/genie/spaces
    # - body: {"title": ..., "description": ..., "warehouse_id": ..., "serialized_space": ...}
    # - httpx.post() 사용
    raise NotImplementedError("create_genie_space를 구현하세요")


def main():
    print("🧞 Exercise 01a: Genie Space 생성")
    print("=" * 60)

    # 예제 설정 — Fashion Recommendations 데이터
    tables = [
        {"catalog": "shared", "schema": "fashion_recommendations", "table": "transactions"},
        {"catalog": "shared", "schema": "fashion_recommendations", "table": "customers"},
    ]
    instructions = [
        "## Column Naming Conventions\n"
        "- The transaction date column is `t_dat` in the `transactions` table, not `date` or `transaction_date`.\n"
        "- Customer identifier is `customer_id` in both `transactions` and `customers` tables.\n"
        "- The `price` column in `transactions` represents per-unit price — each row is one unit sold.",
        "## Date and Time Handling\n"
        "- Use `t_dat` for date filtering in the `transactions` table (format: DATE).\n"
        "- The `transactions` table has pre-extracted `year` and `month` integer columns — prefer these for year/month grouping over YEAR() and MONTH() functions.\n"
        "- When users say 'last month' or 'this year', use CURRENT_DATE and DATE_SUB/DATE_TRUNC functions on `t_dat`.",
        "## Sales Channel Mapping\n"
        "- `sales_channel_id = 1` means **Online** sales.\n"
        "- `sales_channel_id = 2` means **In-Store** (offline) sales.\n"
        "- When users ask about 'online sales' or 'store sales', filter on `sales_channel_id` accordingly.",
        "## Customer Segmentation\n"
        "- `club_member_status` in the `customers` table indicates membership tier (ACTIVE, PRE-CREATE, LEFT CLUB, etc.).\n"
        "- `fashion_news_frequency` indicates news subscription (Regularly, Monthly, None).\n"
        "- Use `customers.age` for age-based segmentation.",
    ]
    sample_questions = [
        "How does revenue compare between online and in-store sales by month?",
        "What is the total online revenue for 2020?",
        "What are the monthly sales trends?",
        "Who are the top spending customers and what is their membership status?",
        "How many transactions did each age group make?",
    ]
    example_sqls = [
        {
            "question": "How does revenue compare between online and in-store sales by month?",
            "sql": "SELECT year, month, CASE WHEN sales_channel_id = 1 THEN 'Online' ELSE 'In-Store' END AS sales_channel, COUNT(*) AS num_transactions, CAST(SUM(price) AS DECIMAL(38,2)) AS total_revenue FROM shared.fashion_recommendations.transactions GROUP BY year, month, sales_channel_id ORDER BY year, month, sales_channel_id",
        },
        {
            "question": "What are the monthly sales trends?",
            "sql": "SELECT year, month, COUNT(*) AS num_transactions, CAST(SUM(price) AS DECIMAL(38,2)) AS total_revenue, COUNT(DISTINCT customer_id) AS unique_customers FROM shared.fashion_recommendations.transactions GROUP BY year, month ORDER BY year, month",
        },
        {
            "question": "Who are the top spending customers and what is their membership status?",
            "sql": "SELECT t.customer_id, c.club_member_status, c.age, COUNT(*) AS num_purchases, CAST(SUM(t.price) AS DECIMAL(38,2)) AS total_spent FROM shared.fashion_recommendations.transactions t INNER JOIN shared.fashion_recommendations.customers c ON t.customer_id = c.customer_id GROUP BY t.customer_id, c.club_member_status, c.age ORDER BY total_spent DESC LIMIT 20",
        },
    ]

    join_specs = [
        {
            "left": {"table": "shared.fashion_recommendations.transactions", "column": "customer_id"},
            "right": {"table": "shared.fashion_recommendations.customers", "column": "customer_id"},
            "sql": ["shared.fashion_recommendations.transactions.customer_id = shared.fashion_recommendations.customers.customer_id"],
        }
    ]

    sql_snippets = {
        "filters": [
            {
                "id": uuid4().hex,
                "sql": "transactions.sales_channel_id = 1",
                "display_name": "Online Sales Only",
                "synonyms": ["online", "web sales", "e-commerce"],
            },
            {
                "id": uuid4().hex,
                "sql": "customers.club_member_status = 'ACTIVE'",
                "display_name": "Active Club Members",
                "synonyms": ["active members", "club members", "active customers"],
            },
            {
                "id": uuid4().hex,
                "sql": "transactions.t_dat >= DATE_SUB(CURRENT_DATE(), 365)",
                "display_name": "Last 12 Months",
                "synonyms": ["last year", "past year", "recent year"],
            },
            {
                "id": uuid4().hex,
                "sql": "transactions.sales_channel_id = 2",
                "display_name": "In-Store Sales Only",
                "synonyms": ["in-store", "offline", "store sales", "brick and mortar"],
            },
            {
                "id": uuid4().hex,
                "sql": "transactions.t_dat >= DATE_SUB(CURRENT_DATE(), 30)",
                "display_name": "Last 30 Days",
                "synonyms": ["last month", "recent", "past month"],
            },
        ],
        "expressions": [
            {
                "id": uuid4().hex,
                "alias": "transaction_month",
                "sql": "transactions.month",
                "display_name": "Transaction Month",
                "synonyms": ["month", "sale month"],
            },
            {
                "id": uuid4().hex,
                "alias": "sales_channel_name",
                "sql": "CASE WHEN transactions.sales_channel_id = 1 THEN 'Online' ELSE 'In-Store' END",
                "display_name": "Sales Channel Name",
                "synonyms": ["channel", "sales channel"],
            },
            {
                "id": uuid4().hex,
                "alias": "transaction_year",
                "sql": "transactions.year",
                "display_name": "Transaction Year",
                "synonyms": ["year", "sale year"],
            },
        ],
        "measures": [
            {
                "id": uuid4().hex,
                "alias": "transaction_count",
                "sql": "COUNT(*)",
                "display_name": "Transaction Count",
                "synonyms": ["number of transactions", "sales count", "purchase count"],
            },
            {
                "id": uuid4().hex,
                "alias": "unique_customer_count",
                "sql": "COUNT(DISTINCT transactions.customer_id)",
                "display_name": "Unique Customers",
                "synonyms": ["customer count", "distinct customers", "number of customers"],
            },
            {
                "id": uuid4().hex,
                "alias": "avg_price",
                "sql": "CAST(AVG(transactions.price) AS DECIMAL(38,2))",
                "display_name": "Average Price",
                "synonyms": ["avg price", "mean price", "average transaction value"],
            },
            {
                "id": uuid4().hex,
                "alias": "total_revenue",
                "sql": "CAST(SUM(transactions.price) AS DECIMAL(38,2))",
                "display_name": "Total Revenue",
                "synonyms": ["revenue", "total sales", "sales amount"],
            },
        ],
    }

    print("  1️⃣ serialized_space 생성 중...")
    serialized = build_serialized_space(
        tables=tables,
        instructions=instructions,
        sample_questions=sample_questions,
        example_sqls=example_sqls,
        join_specs=join_specs,
        sql_snippets=sql_snippets,
    )
    print(f"  ✅ serialized_space 생성 완료 ({len(serialized)} bytes)")

    print("  2️⃣ Genie Space 생성 API 호출 중...")
    space = create_genie_space(
        title="Fashion Recommendations Analytics 2",
        description="A natural language analytics space for exploring fashion sales transactions and customer profiles.",
        warehouse_id=WAREHOUSE_ID,
        serialized_space=serialized,
    )
    space_id = space["space_id"]
    print(f"  ✅ Space 생성 완료!")
    print(f"     Space ID: {space_id}")

    print(f"\n💡 Tip: exercise_01b에서 이 Space ID를 사용하세요:")
    print(f"   python exercise_01b_query_space.py {space_id}")


if __name__ == "__main__":
    main()
