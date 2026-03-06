# genie-space

사용자가 분석 목적과 테이블 스키마를 제공하면, 최적의 Genie Space를 자동으로 생성하는 스킬입니다.

## 사용법
/genie-space <분석 목적> <테이블 목록>

예시:
```
/genie-space "패션 추천 분석" "shared.fashion_recommendations, shared.user_profiles"
```

## 처리 절차

### 1단계: 분석 목적과 스키마 파악
- 사용자가 제공한 **분석 목적**과 **테이블 목록**을 확인합니다
- `databricks-query` 등을 활용해 각 테이블의 스키마(컬럼명, 타입, 설명)를 조회합니다

### 2단계: Instruction 작성
- 분석 목적에 맞는 **instruction**(지시사항)을 작성합니다
- 비즈니스 용어 정의, 분석 관점, 주의사항 등을 포함합니다
- 예시: "매출은 총 판매금액에서 환불을 제외한 값입니다"

### 3단계: Join 및 SQL Expression 정의 (필요 시)
- 테이블 간 관계가 있다면 **join 조건**을 정의합니다
- 계산 필드가 필요하면 **sql_expressions**를 작성합니다
- 예시: join → `orders.user_id = users.id`, sql_expression → `revenue - refund AS net_revenue`

### 4단계: Genie Space 생성
- `create_genie_space` MCP tool을 호출하여 Space를 생성합니다
- 전달 파라미터: title, description, warehouse_id, tables, instructions, sample_questions 등

### 5단계: 테스트 질의
- `ask_genie` MCP tool로 생성된 Space에 테스트 질의를 수행합니다
- 분석 목적에 맞는 기본 질문으로 Space가 정상 동작하는지 확인합니다

## 출력

```
Genie Space 생성 완료
- Space ID: <space_id>
- Space 이름: <title>
- 포함 테이블: <table_list>

테스트 질의 결과:
- 질문: <test_question>
- 응답: <query_result>
```
