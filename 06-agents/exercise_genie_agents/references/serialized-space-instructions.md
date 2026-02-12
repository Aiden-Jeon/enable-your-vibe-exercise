# Serialized Space Instructions 구조 가이드

Genie Space의 `serialized_space` 내 `instructions` 블록 구조를 설명합니다.
`genie-instructor` 에이전트가 이 구조에 맞는 instructions를 작성합니다.

## Instructions 블록 전체 구조

```yaml
instructions:
  text_instructions: "비즈니스 컨텍스트 설명"
  example_question_sqls:
    - question: "자연어 질문"
      sql: "SELECT ..."
  sql_snippets:
    expressions:
      - name: "이름"
        expression: "SQL 표현식"
    measures:
      - name: "이름"
        expression: "집계 SQL"
    filters:
      - name: "이름"
        expression: "WHERE 조건"
  join_specs:
    - left_table: "테이블A"
      right_table: "테이블B"
      join_condition: "ON 조건"
```

## 1. text_instructions

Space의 비즈니스 컨텍스트를 자연어로 설명하는 텍스트입니다.

**포함할 내용:**
- 데이터의 비즈니스 의미
- 도메인 용어 및 약어 정의
- 컬럼별 비즈니스 규칙 (예: score 범위, NULL 의미)
- 데이터 기간 및 갱신 주기

```yaml
text_instructions: |
  이 Space는 패션 추천 시스템의 데이터를 분석합니다.

  주요 테이블:
  - fashion_recommendations: 사용자별 패션 추천 결과
  - fashion_products: 상품 마스터 데이터

  비즈니스 규칙:
  - recommendation_score: 0-100 사이 값, 80 이상이면 '강력 추천'
  - brand: 브랜드명, NULL이면 자체 브랜드
  - created_date: 추천 생성일 (UTC 기준)
```

## 2. example_question_sqls

자연어 질문과 대응하는 SQL 쌍입니다. Genie가 유사한 질문에 올바른 SQL을 생성하도록 안내합니다.

**작성 가이드:**
- 최소 3개 이상의 예시 포함
- 단순 조회, 집계, 필터링, 정렬 등 다양한 패턴
- 실제 사용자가 물어볼 법한 자연어 표현

```yaml
example_question_sqls:
  - question: "브랜드별 추천 건수를 알려줘"
    sql: |
      SELECT brand, COUNT(*) AS recommendation_count
      FROM fashion_recommendations
      GROUP BY brand
      ORDER BY recommendation_count DESC

  - question: "최근 한 달간 추천 점수가 가장 높은 상품 Top 10은?"
    sql: |
      SELECT product_name, brand, recommendation_score
      FROM fashion_recommendations
      WHERE created_date >= DATE_ADD(CURRENT_DATE(), -30)
      ORDER BY recommendation_score DESC
      LIMIT 10

  - question: "카테고리별 평균 추천 점수는?"
    sql: |
      SELECT category, AVG(recommendation_score) AS avg_score
      FROM fashion_recommendations
      GROUP BY category
      ORDER BY avg_score DESC
```

## 3. sql_snippets

자주 사용하는 SQL 표현식을 미리 정의하여 Genie가 활용하도록 합니다.

### expressions — 계산식 정의

```yaml
expressions:
  - name: "recommendation_grade"
    expression: >
      CASE
        WHEN recommendation_score >= 80 THEN '강력추천'
        WHEN recommendation_score >= 60 THEN '추천'
        ELSE '보통'
      END
  - name: "score_percentile"
    expression: "PERCENT_RANK() OVER (ORDER BY recommendation_score)"
```

### measures — 집계 메트릭 정의

```yaml
measures:
  - name: "avg_score"
    expression: "AVG(recommendation_score)"
  - name: "total_recommendations"
    expression: "COUNT(*)"
  - name: "high_score_ratio"
    expression: "SUM(CASE WHEN recommendation_score >= 80 THEN 1 ELSE 0 END) * 100.0 / COUNT(*)"
```

### filters — 필터 조건 정의

```yaml
filters:
  - name: "high_score_only"
    expression: "recommendation_score >= 80"
  - name: "recent_30_days"
    expression: "created_date >= DATE_ADD(CURRENT_DATE(), -30)"
  - name: "exclude_null_brand"
    expression: "brand IS NOT NULL"
```

## 4. join_specs

테이블 간 조인 조건을 명시합니다.

```yaml
join_specs:
  - left_table: "fashion_recommendations"
    right_table: "fashion_products"
    join_condition: "ON fashion_recommendations.product_id = fashion_products.id"
  - left_table: "fashion_recommendations"
    right_table: "fashion_categories"
    join_condition: "ON fashion_recommendations.category_id = fashion_categories.id"
```

## 참고

- instructions는 Genie가 SQL을 생성할 때 참조하는 컨텍스트입니다
- 더 구체적인 instructions일수록 정확한 SQL이 생성됩니다
- example_question_sqls가 가장 직접적인 영향을 미칩니다
