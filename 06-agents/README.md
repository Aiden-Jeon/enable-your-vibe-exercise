# Section 06: Custom Agents - 실습 코드

Custom Agents를 활용하여 Genie Space 라이프사이클 워크플로우를 구조화하는 실습 코드입니다.

## 실습 구성

### Exercise: Genie Space 라이프사이클 에이전트 만들기

- **경로**: `exercise_genie_agents/`
- **목표**: Genie Space 설계, Instructions 작성, 품질 테스트를 수행하는 Custom Agent를 만들어봅니다
- **소요 시간**: 약 25분 (Step 1: 10분 + Step 2: 15분 + Bonus: 선택)
- **핵심 학습**: agent.md 구조, 역할 정의, 제약 조건, 출력 형식, 에이전트 간 역할 분담

## 실습 순서

1. `exercise_genie_agents/README.md`를 먼저 읽고 전체 흐름을 파악합니다
2. Step 1: `genie-space-designer.md` 템플릿의 TODO를 채워 에이전트를 완성합니다
3. Step 2: `genie-instructor.md` 템플릿의 TODO를 채워 에이전트를 완성합니다
4. Bonus: `genie-tester.md` 템플릿의 TODO를 채워 에이전트를 완성합니다 (선택)
5. 완성된 에이전트를 `.claude/agents/`에 배치하고 실제로 호출하여 테스트합니다

## Claude Code 프롬프트 예시

```bash
# genie-space-designer 에이전트 작성 요청
> exercise_genie_agents/genie-space-designer.md 템플릿을 기반으로 genie-space-designer 에이전트를 완성해줘

# genie-instructor 에이전트 작성 요청
> exercise_genie_agents/genie-instructor.md 템플릿과 references/serialized-space-instructions.md를 참고해서 genie-instructor 에이전트를 완성해줘

# 에이전트 호출 테스트
> @genie-space-designer catalog.schema의 테이블을 분석해서 Space를 설계해줘
> @genie-instructor designer 결과를 기반으로 instructions를 작성해줘
> @genie-tester Space에 sample questions를 질의하고 응답 품질을 평가해줘
```

## 사전 준비

- Section 05 (Skills)의 개념을 이해하고 있어야 합니다
- Claude Code가 설치되어 있어야 합니다
- Genie MCP 서버가 설정되어 있어야 합니다 (Section 04에서 구성)

### Unity Catalog MCP 서버 설정

`@genie-space-designer` 에이전트가 테이블 스키마를 분석하려면 Unity Catalog MCP 서버가 필요합니다.

**제공 Tools:**

| Tool | 설명 | 예시 |
|------|------|------|
| `list_schemas` | 카탈로그 내 스키마 목록 조회 | `list_schemas("main")` |
| `list_tables` | 스키마 내 테이블 목록 조회 | `list_tables("main", "default")` |
| `describe_table` | 테이블 상세 메타데이터 조회 | `describe_table("main.default.my_table")` |

**`.mcp.json` 설정:**

```bash
claude mcp add -s project unity-catalog -- uv run python 06-agents/exercise_unity_catalog_mcp.py
```

> 💡 `exercise_unity_catalog_mcp.py`는 완성 코드로 제공됩니다. 위 명령어 한 줄로 MCP 서버가 등록됩니다.
