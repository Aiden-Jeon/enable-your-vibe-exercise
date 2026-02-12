# Exercise: Genie Analyst 에이전트 만들기

## 개요

이 실습에서는 Databricks Genie Space 데이터를 분석하는 `data-analyst` 에이전트와 SQL 쿼리 품질을 검증하는 `sql-reviewer` 에이전트를 만들어봅니다.

## 파일 구조

```
exercise_genie_analyst/
├── README.md                              # 이 파일
├── data-analyst.md                        # Step 1: 데이터 분석 에이전트 템플릿 (TODO)
├── sql-reviewer.md                        # Step 2: SQL 리뷰 에이전트 템플릿 (TODO)
└── references/
    └── databricks-sql-best-practices.md   # SQL 최적화 가이드 (Step 2에서 활용)
```

## Step 1: `@data-analyst` 에이전트 만들기 (10분)

### 목표

Genie Space 데이터를 분석하는 전문 에이전트를 만듭니다.

### 진행 방법

1. `data-analyst.md` 파일을 열어 TODO 항목을 확인합니다
2. Claude Code에게 TODO를 채워달라고 요청합니다:
   ```
   > data-analyst.md 템플릿의 TODO를 채워서 data-analyst 에이전트를 완성해줘.
   >   Genie Space 데이터를 분석하는 역할이야.
   ```
3. 완성된 파일을 `.claude/agents/data-analyst.md`에 복사합니다
4. `@data-analyst`로 호출하여 테스트합니다:
   ```
   > @data-analyst fashion_recommendations 테이블의 브랜드별 추천 분포를 분석해줘
   ```

### 학습 포인트

- **역할 정의**: "당신은 ~입니다"로 시작하는 명확한 역할 부여
- **제약 조건**: 사용 가능한 도구를 명시하여 에이전트 범위 제한
- **출력 형식**: 일관된 분석 결과를 위한 구조화된 형식

## Step 2: `@sql-reviewer` 에이전트 만들기 (15분)

### 목표

SQL 쿼리의 품질과 성능을 검증하는 전문 에이전트를 만듭니다.

### 진행 방법

1. `references/databricks-sql-best-practices.md`를 먼저 읽어 SQL 최적화 가이드를 파악합니다
2. `sql-reviewer.md` 파일을 열어 TODO 항목을 확인합니다
3. Claude Code에게 레퍼런스를 참고하여 TODO를 채워달라고 요청합니다:
   ```
   > sql-reviewer.md 템플릿의 TODO를 채워줘.
   >   references/databricks-sql-best-practices.md를 참고해서 체크리스트를 작성해줘.
   ```
4. 완성된 파일을 `.claude/agents/sql-reviewer.md`에 복사합니다
5. `@sql-reviewer`로 호출하여 테스트합니다:
   ```
   > @sql-reviewer 이 SQL을 리뷰해줘: SELECT * FROM fashion_recommendations WHERE brand = 'Nike'
   ```

### 학습 포인트

- **레퍼런스 활용**: 외부 가이드를 에이전트 지식으로 내재화
- **체크리스트 패턴**: 검증 에이전트에서 체크리스트를 활용하는 방법
- **읽기 전용 제약**: 리뷰 에이전트가 직접 수정하지 않도록 제한

## 체크리스트

완성된 에이전트를 다음 기준으로 검증하세요:

- [ ] 역할이 명확하게 정의되어 있는가?
- [ ] 제약 조건이 적절히 설정되어 있는가?
- [ ] 출력 형식이 구조화되어 있는가?
- [ ] 단일 책임 원칙을 따르는가? (data-analyst ≠ sql-reviewer)
- [ ] 에이전트를 호출했을 때 기대한 역할로 동작하는가?
