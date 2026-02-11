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

```bash
# CLI 설정 (아직 안 했다면)
databricks configure

# 바로 실행 가능!
python exercise_00_checklist.py
```

### 방법 2: `.env` 파일 (수동)

```bash
cp .env.example .env
```

```env
DATABRICKS_HOST=https://your-workspace.cloud.databricks.com
DATABRICKS_TOKEN=dapi_xxxxxxxxxxxxxxxx
WAREHOUSE_ID=your-sql-warehouse-id   # 선택: 비워두면 자동 조회
```

## Claude Code로 구현하기

### Step 1: 환경 검증
```bash
# Exercise 00은 완성 코드 — 바로 실행하여 환경을 확인합니다
python exercise_00_checklist.py
```

### Step 2: Claude Code에게 구현 요청

```bash
# Claude Code 실행
claude

# Exercise 01a: Space 생성
> exercise_01a_create_space.py의 TODO를 구현해줘

# Exercise 01b: Space 질의
> exercise_01b_query_space.py의 TODO를 구현해줘

# Exercise 02: Genie MCP 서버
> exercise_02_genie_mcp_server.py의 모든 TODO를 구현해줘
```

### Step 3: 실행 및 테스트

```bash
# Exercise 01a: Space 생성
python exercise_01a_create_space.py

# Exercise 01b: Space 질의 (01a에서 얻은 SPACE_ID 사용)
python exercise_01b_query_space.py <SPACE_ID>

# Exercise 02: MCP 서버 실행
python exercise_02_genie_mcp_server.py
```

## 실습 파일

### Exercise 00: 사전 환경 체크리스트 (완성 코드)

실습 시작 전 환경 설정이 올바른지 검증합니다.

```bash
python exercise_00_checklist.py
```

### Exercise 01a: Genie Space 생성 (스켈레톤)

TODO: `build_serialized_space()`와 `create_genie_space()` 구현

**주요 흐름:**
1. `build_serialized_space()` — protobuf v2 JSON 형식으로 Space 설정 생성
2. `create_genie_space()` — POST /api/2.0/genie/spaces로 Space 생성

### Exercise 01b: Genie Space 질의 (스켈레톤)

TODO: `create_conversation()`, `send_message()`, `poll_result()`, `format_result()` 구현

**주요 흐름:**
1. `create_conversation()` — 새 대화 생성
2. `send_message()` — 자연어 질문 전송
3. `poll_result()` — 점진적 백오프 폴링으로 결과 조회

### Exercise 02: Genie MCP 서버 (스켈레톤)

TODO: 헬퍼 함수 3개 + MCP tool 3개 구현

**제공 Tool:**

| Tool | 설명 |
|------|------|
| `create_genie_space` | Genie Space를 생성합니다 |
| `ask_genie` | 새 대화를 시작하고 자연어로 데이터를 질의합니다 |
| `continue_conversation` | 기존 대화에 후속 질문을 합니다 |

## Claude Code에서 MCP 서버 연결

### `.claude/settings.local.json` 설정

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
| **join_specs** | 테이블 간 조인 조건 — left/right 테이블·컬럼과 JOIN SQL 명시 |
| **sql_snippets** | SQL 스니펫 — expressions(계산식), measures(집계), filters(필터) |
| **Space 생성 API** | POST /api/2.0/genie/spaces로 프로그래밍 방식 Space 생성 |
| **Genie 질의 API** | 대화 생성 → 메시지 전송 → 결과 폴링의 3단계 |
| **점진적 백오프** | 폴링 간격을 1초 → 5초로 점진적 증가하여 API 부하 절감 |
| **래핑 패턴** | 복잡한 REST API 호출을 단순한 MCP tool로 추상화 |
