# Databricks SQL Best Practices

Databricks SQL 쿼리 작성 시 참고할 성능 및 품질 가이드입니다.

## 1. 컬럼 선택

- `SELECT *`를 지양하고 필요한 컬럼만 명시적으로 선택
- 불필요한 컬럼은 I/O와 네트워크 비용을 증가시킴

```sql
-- Bad
SELECT * FROM fashion_recommendations;

-- Good
SELECT brand, category, recommendation_score
FROM fashion_recommendations;
```

## 2. 파티션 활용

- `WHERE` 절에 파티션 키를 포함하여 스캔 범위를 줄임
- 날짜 기반 파티션의 경우 범위 조건 활용

```sql
-- Bad: 전체 테이블 스캔
SELECT brand, COUNT(*) FROM fashion_recommendations GROUP BY brand;

-- Good: 파티션 키로 필터링
SELECT brand, COUNT(*)
FROM fashion_recommendations
WHERE created_date >= '2024-01-01'
GROUP BY brand;
```

## 3. JOIN 최적화

- JOIN 조건이 올바르게 지정되었는지 확인
- 불필요한 `CROSS JOIN`을 피함
- 작은 테이블을 기준으로 JOIN (브로드캐스트 힌트 활용 가능)

```sql
-- Bad: CROSS JOIN (의도하지 않은 경우)
SELECT a.*, b.*
FROM table_a a, table_b b;

-- Good: 명시적 JOIN 조건
SELECT a.brand, b.category_name
FROM fashion_recommendations a
INNER JOIN categories b ON a.category_id = b.id;
```

## 4. 집계 최적화

- `GROUP BY`와 집계 함수가 올바르게 매칭되는지 확인
- `HAVING` 대신 서브쿼리로 사전 필터링 고려
- `DISTINCT`는 필요한 경우에만 사용

```sql
-- Bad: 불필요한 DISTINCT
SELECT DISTINCT brand FROM fashion_recommendations GROUP BY brand;

-- Good: GROUP BY만으로 충분
SELECT brand FROM fashion_recommendations GROUP BY brand;
```

## 5. 데이터 타입 변환

- 암묵적 타입 변환 대신 명시적 `CAST` 사용
- 문자열과 숫자 비교 시 타입 불일치 주의

```sql
-- Bad: 암묵적 변환
SELECT * FROM orders WHERE order_id = '12345';

-- Good: 명시적 변환
SELECT * FROM orders WHERE order_id = CAST('12345' AS INT);
```

## 6. LIMIT 절 활용

- 탐색적 쿼리에는 반드시 `LIMIT` 절 포함
- 대용량 테이블에서 전체 결과를 가져오는 것을 방지

```sql
-- Bad: 대용량 테이블 전체 조회
SELECT brand, recommendation_score
FROM fashion_recommendations
ORDER BY recommendation_score DESC;

-- Good: 상위 결과만 조회
SELECT brand, recommendation_score
FROM fashion_recommendations
ORDER BY recommendation_score DESC
LIMIT 100;
```

## 7. 보안

- 쿼리에 토큰, 비밀번호 등 민감 정보를 하드코딩하지 않음
- 환경 변수나 Databricks Secrets를 활용

```sql
-- Bad: 하드코딩된 자격 증명
-- SELECT * FROM external_table USING TOKEN 'abc123';

-- Good: Databricks Secrets 활용
-- SELECT * FROM external_table USING SECRET('scope', 'key');
```
