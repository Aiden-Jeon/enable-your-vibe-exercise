# Section 05: Genie MCP 서버 만들기

## 학습 목표

- Genie Space 생성 API와 serialized_space(protobuf v2) 형식을 이해한다
- FastMCP로 Space 생성 + 질의 MCP 서버를 구현한다
- Claude Code에서 Genie MCP를 연결하여 Space 생성 및 데이터 질의를 수행한다

## 사전 준비

### 필수 요구사항

1. **Databricks 워크스페이스** 접근 권한
2. **Databricks CLI** 설치 및 설정 (`databricks configure`)
3. **SQL Warehouse** — 워크스페이스에 하나 이상 존재 (WAREHOUSE_ID는 자동 조회됨)

### Python 패키지 설치

```bash
# 프로젝트 루트에서 실행 (모든 의존성 한 번에 설치)
uv sync
```

## 환경 설정

각 exercise 파일에 포함된 `resolve_databricks_config()` 함수가 인증 정보를 자동으로 해석합니다.

### 인증 해석 순서

| 항목 | 1순위 | 2순위 | 3순위 |
|------|-------|-------|-------|
| **HOST** | `.env` / 환경변수 | `~/.databrickscfg` | 기본값 (`e2-demo-field-eng`) |
| **TOKEN** | `.env` / 환경변수 | `databricks auth token --host <HOST>` | — |
| **WAREHOUSE_ID** | `.env` / 환경변수 | `GET /api/2.0/sql/warehouses` (RUNNING 우선) | — |

### 방법 1: Databricks CLI (권장)

`databricks configure`로 CLI를 설정한 경우, **별도 설정 없이 바로 실행 가능**합니다.
HOST와 TOKEN은 CLI에서 자동으로 가져오고, WAREHOUSE_ID는 API로 자동 조회됩니다.

```bash
# CLI 설정 (아직 안 했다면)
databricks configure

# 바로 실행 가능!
python exercise_00_checklist.py
```

### 방법 2: `.env` 파일 (수동)

CLI 없이 직접 설정하려면 `.env` 파일을 생성합니다.

```bash
cp .env.example .env
```

```env
DATABRICKS_HOST=https://your-workspace.cloud.databricks.com
DATABRICKS_TOKEN=dapi_xxxxxxxxxxxxxxxx
WAREHOUSE_ID=your-sql-warehouse-id   # 선택: 비워두면 자동 조회
```

### 환경변수 설명

- **DATABRICKS_HOST**: Databricks 워크스페이스 URL (끝에 `/` 없이)
- **DATABRICKS_TOKEN**: Personal Access Token 또는 CLI가 발급한 토큰
- **WAREHOUSE_ID**: SQL Warehouse ID (비워두면 API로 자동 조회 — RUNNING 상태 우선)

## 실습 파일

### Exercise 00: 사전 환경 체크리스트

실습 시작 전 환경 설정이 올바른지 검증합니다.

```bash
python exercise_00_checklist.py
```

**4단계 순차 검증:**

| # | 검증 항목 | 설명 |
|---|----------|------|
| 1 | 인증 정보 확인 | `.env` / databricks CLI / 기본값에서 HOST/TOKEN/WAREHOUSE_ID 해석 |
| 2 | Databricks 호스트 연결 | 호스트 URL 및 토큰 유효성 검증 |
| 3 | SQL Warehouse 접근 | `SELECT 1`로 Warehouse 정상 작동 확인 |
| 4 | 데이터 스키마 확인 | `shared.fashion_recommendations`에 `transactions`, `customers` 테이블 존재 확인 |

**학습 포인트:**
- 이전 단계 실패 시 이후 단계를 건너뛰는 cascading skip 패턴
- Databricks REST API 인증 및 SQL Statement API 활용

### Exercise 01a: Genie Space 생성

Genie Space를 API로 직접 생성합니다.

```bash
python exercise_01a_create_space.py
```

**주요 흐름:**
1. `build_serialized_space()` — protobuf v2 JSON 형식으로 Space 설정 생성
2. `create_genie_space()` — POST /api/2.0/genie/spaces로 Space 생성

**학습 포인트:**
- serialized_space의 protobuf v2 JSON 구조 (version, data_sources, config, instructions)
- instructions의 전체 하위 필드: text_instructions, example_question_sqls, join_specs, sql_snippets
- join_specs로 테이블 간 조인 조건 명시 → Genie의 정확한 JOIN SQL 생성 유도
- sql_snippets(expressions/measures/filters)로 자주 쓰는 계산식·집계·필터 사전 정의
- Databricks API 인증 방식 (Bearer 토큰)

### Exercise 01b: Genie Space 질의

생성된 Genie Space에 자연어 질의를 수행합니다.

```bash
python exercise_01b_query_space.py <SPACE_ID>
```

**주요 흐름:**
1. `create_conversation()` — 새 대화 생성
2. `send_message()` — 자연어 질문 전송
3. `poll_result()` — 점진적 백오프 폴링으로 결과 조회

**학습 포인트:**
- Genie 질의 API의 3단계 구조 (대화 생성 → 메시지 전송 → 결과 폴링)
- 점진적 백오프 폴링 패턴 (1초 → 최대 5초)
- 응답에서 텍스트/SQL 결과 추출

### Exercise 02: Genie MCP 서버

Genie API를 FastMCP로 래핑한 MCP 서버입니다. 3개 tool을 제공합니다.

```bash
python exercise_02_genie_mcp_server.py
```

**제공 Tool:**

| Tool | 설명 |
|------|------|
| `create_genie_space` | Genie Space를 생성합니다 (테이블, 지시사항, 예제 질문 설정) |
| `ask_genie` | 새 대화를 시작하고 자연어로 데이터를 질의합니다 |
| `continue_conversation` | 기존 대화에 후속 질문을 합니다 |

**학습 포인트:**
- FastMCP의 `@mcp.tool()` 데코레이터 활용
- REST API를 MCP tool로 래핑하는 패턴
- space_id를 파라미터로 받아 유연하게 여러 Space 질의 가능

## Claude Code에서 MCP 서버 연결

### `.claude/settings.local.json` 설정

프로젝트 루트에 아래 파일을 생성하거나 수정합니다:

```json
{
  "mcpServers": {
    "genie": {
      "command": "python",
      "args": ["05-genie-mcp/exercise_02_genie_mcp_server.py"],
      "cwd": "."
    }
  }
}
```

### 사용 예시

1. Claude Code를 재시작하거나 `/mcp` 명령으로 MCP 서버 상태를 확인합니다
2. `genie` 서버가 연결되었는지 확인합니다
3. Space 생성 및 데이터 질의:

```
사용자: "samples.nyctaxi.trips 테이블로 Genie Space를 만들어줘"
Claude: create_genie_space tool로 Space를 생성합니다...

사용자: "생성한 Space에서 총 트립 수를 알려줘"
Claude: ask_genie tool로 질의합니다...

사용자: "월별로 나눠서 보여줘"
Claude: continue_conversation tool로 후속 질의합니다...
```

## 학습 포인트 요약

| 개념 | 설명 |
|------|------|
| **serialized_space** | protobuf v2 JSON 형식으로 테이블, 지시사항, 예제 질문을 정의 |
| **text_instructions** | instructions 내 텍스트 지시사항 (예: "한국어로 답변해주세요") |
| **example_question_sqls** | instructions 내 예제 질문-SQL 쌍 — Genie가 참고하는 SQL 패턴 |
| **join_specs** | instructions 내 테이블 간 조인 조건 — left/right 테이블·컬럼과 JOIN SQL 명시 |
| **sql_snippets** | instructions 내 SQL 스니펫 — expressions(계산식), measures(집계), filters(필터) |
| **Space 생성 API** | POST /api/2.0/genie/spaces로 프로그래밍 방식 Space 생성 |
| **Genie 질의 API** | 대화 생성 → 메시지 전송 → 결과 폴링의 3단계 |
| **점진적 백오프** | 폴링 간격을 1초 → 5초로 점진적 증가하여 API 부하 절감 |
| **래핑 패턴** | 복잡한 REST API 호출을 단순한 MCP tool로 추상화 |
| **FastMCP** | Python 데코레이터 기반의 간편한 MCP 서버 구현 |
