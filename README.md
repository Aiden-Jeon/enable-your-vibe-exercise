# Enable Your Vibe - 실습 코드

> Vibe Coding 핸즈온 세션 실습 코드 모음

## 개요

이 레포는 **Enable Your Vibe** 핸즈온 세션의 실습 코드만 모아둔 저장소입니다.
슬라이드 자료는 별도 레포([enable-your-vibe](https://github.com/aiden-jeon/enable-your-vibe))를 참고하세요.

**실습 방식**: 각 exercise 파일에는 함수 시그니처와 TODO 주석이 포함되어 있습니다.
**Claude Code를 사용하여 TODO를 구현**하는 Vibe Coding 방식으로 진행합니다.

## 사전 준비

| 항목 | 설명 |
|------|------|
| Python 3.11+ | `python --version`으로 확인 |
| [uv](https://docs.astral.sh/uv/) | Python 패키지 매니저 (`curl -LsSf https://astral.sh/uv/install.sh \| sh`) |
| [Claude Code](https://docs.anthropic.com/en/docs/claude-code) | Anthropic CLI (`npm install -g @anthropic-ai/claude-code`) |
| Databricks CLI | `pip install databricks-cli` 또는 `brew install databricks` |
| Databricks 워크스페이스 | 접근 권한 + Personal Access Token |

## 환경 설정

```bash
# 1. 레포 클론
git clone <repo-url>
cd enable-your-vibe-code

# 2. 의존성 설치
uv sync

# 3. 환경변수 설정 (섹션 04부터 필요)
cp 04-genie-mcp/.env.example 04-genie-mcp/.env
# .env 파일에 DATABRICKS_HOST, DATABRICKS_TOKEN, WAREHOUSE_ID 입력
```

## 실습 워크플로우

각 실습은 다음 순서로 진행합니다:

1. **스켈레톤 파일 확인** — TODO 주석과 요구사항을 읽습니다
2. **Claude Code로 구현** — Claude Code에게 TODO 구현을 요청합니다
3. **실행 및 테스트** — 구현된 코드를 실행하여 동작을 확인합니다

### Claude Code 프롬프트 예시

```
# 파일의 TODO를 구현해줘
exercise_01_hello_mcp.py의 TODO를 구현해줘

# 특정 함수 구현 요청
build_serialized_space 함수를 구현해줘

# 전체 파일 구현
이 파일의 모든 TODO를 요구사항에 맞게 구현해줘
```

## 실습 순서

| # | 디렉토리 | 제목 | 설명 |
|---|----------|------|------|
| 02 | `02-claude-code-features/` | Claude Code 사용법 | Claude Code로 Python 함수와 테스트 만들기 |
| 03 | `03-mcp-architecture/` | MCP 아키텍처 | FastMCP로 첫 MCP 서버 만들기 |
| 04 | `04-genie-mcp/` | Genie MCP 서버 | Databricks Genie API → MCP 서버 구현 |
| 05 | `05-skills/` | Skills | Genie Space 스킬 작성, 레퍼런스 활용 |
| 06 | `06-agents/` | Custom Agents | Genie Space 라이프사이클 에이전트 만들기 |

각 디렉토리의 `README.md`에서 상세 실습 가이드를 확인하세요.

## 프로젝트 구조

```
enable-your-vibe-code/
├── 02-claude-code-features/
│   ├── README.md
│   ├── exercise_01_fibonacci.py       # 스켈레톤 (TODO)
│   └── exercise_02_fibonacci_test.py  # 스켈레톤 (TODO)
├── 03-mcp-architecture/
│   ├── README.md
│   ├── exercise_01_hello_mcp.py      # 스켈레톤 (TODO)
│   └── exercise_02_calculator_mcp.py  # 스켈레톤 (TODO)
├── 04-genie-mcp/
│   ├── README.md
│   ├── .env.example
│   ├── exercise_00_checklist.py       # 환경 검증 (완성 코드)
│   ├── exercise_01a_create_space.py   # 스켈레톤 (TODO)
│   ├── exercise_01b_query_space.py    # 스켈레톤 (TODO)
│   └── exercise_02_genie_mcp_server.py # 스켈레톤 (TODO)
├── 05-skills/
│   ├── README.md
│   └── exercise_genie_skill/
│       ├── SKILL.md                   # 스킬 템플릿 (TODO)
│       └── references/
├── 06-agents/
│   ├── README.md
│   ├── exercise_genie_agents/
│   │   ├── genie-space-designer.md    # 에이전트 정의 (TODO)
│   │   ├── genie-instructor.md        # 에이전트 정의 (TODO)
│   │   ├── genie-tester.md            # 에이전트 정의 (TODO)
│   │   └── references/
│   └── exercise_unity_catalog_mcp.py  # MCP 서버 스켈레톤 (TODO)
└── pyproject.toml
```

## 라이선스

Internal Use Only
