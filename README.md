# Enable Your Vibe - 실습 코드

> Vibe Coding 핸즈온 세션 실습 코드 모음

## 개요

이 레포는 **Enable Your Vibe** 핸즈온 세션의 실습 코드만 모아둔 저장소입니다.
슬라이드 자료는 별도 레포([enable-your-vibe](https://github.com/aiden-jeon/enable-your-vibe))를 참고하세요.

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

# 3. 환경변수 설정 (섹션 05부터 필요)
cp 05-genie-mcp/.env.example 05-genie-mcp/.env
# .env 파일에 DATABRICKS_HOST, DATABRICKS_TOKEN, WAREHOUSE_ID 입력
```

## 실습 순서

| # | 디렉토리 | 제목 | 설명 |
|---|----------|------|------|
| 03 | `03-mcp-architecture/` | MCP 아키텍처 | FastMCP로 첫 MCP 서버 만들기 |
| 05 | `05-genie-mcp/` | Genie MCP 서버 | Databricks Genie API → MCP 서버 구현 |
| 06 | `06-skills-workflow/` | Skills 워크플로우 | Custom Skill 작성, 레퍼런스 활용 |
| 08 | `08-build-ui/` | UI 만들기 | FastAPI + 채팅 UI 구현 |
| 09 | `09-deploy-to-databricks/` | Databricks 배포 | Databricks Apps로 배포 |

각 디렉토리의 `README.md`에서 상세 실습 가이드를 확인하세요.

## 프로젝트 구조

```
enable-your-vibe-code/
├── 03-mcp-architecture/
│   ├── README.md
│   ├── exercise_01_hello_mcp.py
│   └── exercise_02_calculator_mcp.py
├── 05-genie-mcp/
│   ├── README.md
│   ├── .env.example
│   ├── exercise_00_checklist.py
│   ├── exercise_01a_create_space.py
│   ├── exercise_01b_query_space.py
│   └── exercise_02_genie_mcp_server.py
├── 06-skills-workflow/
│   ├── README.md
│   ├── exercise_01_simple_skill/
│   └── exercise_02_skill_with_refs/
├── 08-build-ui/
│   ├── README.md
│   ├── .env.example
│   ├── exercise_01_fastapi_basic.py
│   └── exercise_02_genie_chatbot/
├── 09-deploy-to-databricks/
│   ├── README.md
│   ├── .env.example
│   ├── app.yaml
│   └── exercise_01_prepare_deploy.py
└── pyproject.toml
```

## 라이선스

Internal Use Only
