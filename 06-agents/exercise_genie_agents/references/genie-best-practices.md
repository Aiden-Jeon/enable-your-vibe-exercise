# Genie Space Best Practices

Genie Space를 설계하고 운영할 때 참고할 가이드입니다.

## 1. 테이블 선정

- Space에 포함할 테이블은 **5개 이하**로 제한
- 비즈니스 도메인이 명확한 테이블만 선택
- 테이블 간 관계(JOIN 가능 여부)를 사전에 파악

```
-- Good: 명확한 도메인의 관련 테이블 조합
fashion_recommendations  -- 추천 데이터
fashion_products         -- 상품 마스터
fashion_categories       -- 카테고리 분류

-- Bad: 도메인이 다른 테이블 혼합
fashion_recommendations + hr_employees + server_logs
```

## 2. Sample Questions 작성

- **5개 이상**의 대표 질문을 준비
- 단순 조회부터 집계/비교 분석까지 난이도 다양화
- 실제 비즈니스 사용자가 물어볼 법한 자연어 질문

```
-- Good: 다양한 난이도의 자연어 질문
"브랜드별 추천 건수는 몇 건인가요?"          -- 단순 집계
"최근 한 달간 추천 점수가 가장 높은 상품은?"   -- 필터 + 정렬
"카테고리별 평균 추천 점수 추이를 보여줘"      -- 시계열 분석

-- Bad: SQL 문법이 포함된 질문
"SELECT COUNT(*) FROM fashion_recommendations GROUP BY brand 실행해줘"
```

## 3. Instructions 품질

- `text_instructions`에 비즈니스 컨텍스트를 충분히 설명
- 도메인 용어, 약어, 비즈니스 규칙을 명시
- `example_question_sqls`로 기대하는 SQL 패턴을 안내

```yaml
# Good: 비즈니스 컨텍스트 포함
text_instructions: |
  이 Space는 패션 추천 시스템의 데이터를 분석합니다.
  recommendation_score는 0-100 사이의 값으로,
  80 이상이면 '강력 추천'으로 분류합니다.
  brand 컬럼은 브랜드명을 저장하며, NULL이면 자체 브랜드입니다.

# Bad: 컨텍스트 없이 테이블만 나열
text_instructions: |
  fashion_recommendations 테이블을 사용합니다.
```

## 4. SQL Snippets 활용

- `expressions`: 자주 사용하는 계산식 정의
- `measures`: 집계 메트릭 정의
- `filters`: 자주 사용하는 필터 조건 정의

```yaml
sql_snippets:
  expressions:
    - name: "recommendation_grade"
      expression: "CASE WHEN recommendation_score >= 80 THEN '강력추천' WHEN recommendation_score >= 60 THEN '추천' ELSE '보통' END"
  measures:
    - name: "avg_score"
      expression: "AVG(recommendation_score)"
    - name: "total_recommendations"
      expression: "COUNT(*)"
  filters:
    - name: "high_score_only"
      expression: "recommendation_score >= 80"
```

## 5. 테스트 전략

- Space 생성 후 sample questions로 응답 품질 검증
- 예상 SQL과 실제 생성 SQL을 비교
- 엣지 케이스(NULL, 빈 결과) 테스트 포함
- 자연어 변형(동의어, 다른 표현)으로도 올바르게 동작하는지 확인

## 6. SQL 작성 가이드

- `SELECT *`를 지양하고 필요한 컬럼만 명시적으로 선택
- `WHERE` 절에 파티션 키를 포함하여 스캔 범위를 줄임
- JOIN 조건이 올바르게 지정되었는지 확인
- 탐색적 쿼리에는 반드시 `LIMIT` 절 포함
- 암묵적 타입 변환 대신 명시적 `CAST` 사용
