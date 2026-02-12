# Section 06: Custom Agents - 실습 코드

Custom Agents를 활용하여 데이터 분석 워크플로우를 구조화하는 실습 코드입니다.

## 실습 구성

### Exercise: Genie Analyst 에이전트 만들기

- **경로**: `exercise_genie_analyst/`
- **목표**: Genie Space 데이터 분석과 SQL 리뷰를 수행하는 Custom Agent를 만들어봅니다
- **소요 시간**: 약 25분 (Step 1: 10분 + Step 2: 15분)
- **핵심 학습**: agent.md 구조, 역할 정의, 제약 조건, 출력 형식

## 실습 순서

1. `exercise_genie_analyst/README.md`를 먼저 읽고 전체 흐름을 파악합니다
2. Step 1: `data-analyst.md` 템플릿의 TODO를 채워 에이전트를 완성합니다
3. Step 2: `sql-reviewer.md` 템플릿의 TODO를 채워 에이전트를 완성합니다
4. 완성된 에이전트를 `.claude/agents/`에 배치하고 실제로 호출하여 테스트합니다

## Claude Code 프롬프트 예시

```bash
# data-analyst 에이전트 작성 요청
> exercise_genie_analyst/data-analyst.md 템플릿을 기반으로 data-analyst 에이전트를 완성해줘

# sql-reviewer 에이전트 작성 요청
> exercise_genie_analyst/sql-reviewer.md 템플릿과 references/databricks-sql-best-practices.md를 참고해서 sql-reviewer 에이전트를 완성해줘

# 에이전트 호출 테스트
> @data-analyst fashion_recommendations 테이블의 브랜드별 추천 분포를 분석해줘
> @sql-reviewer 이 SQL 쿼리를 리뷰해줘: SELECT * FROM fashion_recommendations
```

## 사전 준비

- Section 05 (Skills)의 개념을 이해하고 있어야 합니다
- Claude Code가 설치되어 있어야 합니다
- Genie MCP 서버가 설정되어 있어야 합니다 (Section 04에서 구성)
