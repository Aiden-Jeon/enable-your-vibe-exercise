# genie-space 스킬

Genie MCP 서버를 활용하여 분석 목적에 맞는 Genie Space를 생성합니다.

## 사용법
/genie-space [분석목적] [테이블목록]

## 입력
- **분석목적**: 생성할 Genie Space의 분석 목적 (예: "패션 추천 매출 분석")
- **테이블목록**: 분석에 사용할 Unity Catalog 테이블 (예: "shared.fashion_recommendations")

## 처리 절차

1. **분석 목적과 스키마 파악**
   - 사용자가 제공한 분석 목적을 확인합니다
   - 테이블목록의 스키마(컬럼명, 데이터 타입, 설명)를 파악합니다
   - 테이블 간 관계(FK, 공통 컬럼)를 분석합니다

2. **적절한 instruction 작성**
   - 분석 목적에 맞는 텍스트 지시사항(instructions)을 작성합니다
   - 컬럼 네이밍 컨벤션을 명시합니다 (예: 날짜 컬럼명, ID 매핑 등)
   - 비즈니스 용어와 컬럼 간 매핑을 정의합니다 (예: "온라인 매출" → sales_channel_id = 1)
   - 분석에 유용한 sample_questions를 작성합니다

3. **joins, sql_expressions 등 작성 (필요한 경우)**
   - 테이블이 2개 이상일 경우 join_specs를 정의합니다 (조인 키, 관계 유형)
   - 자주 사용되는 SQL 표현식을 sql_snippets로 정의합니다:
     - **expressions**: 계산 컬럼 (예: CASE WHEN을 이용한 카테고리 매핑)
     - **measures**: 집계 메트릭 (예: SUM, COUNT, AVG)
     - **filters**: 자주 사용하는 필터 조건 (예: 최근 30일, 활성 회원)
   - 복잡한 질의에 대한 example_sqls를 작성합니다

4. **create_genie_space MCP를 이용해 Genie Space 생성**
   - `create_genie_space` MCP tool을 호출하여 Space를 생성합니다
     - title: 분석 목적 기반 제목
     - description: Space 설명
     - warehouse_id: 사용자에게 확인하거나 기본값 사용
     - tables: 테이블 목록
     - instructions: 2단계에서 작성한 지시사항
     - sample_questions: 2단계에서 작성한 예제 질문
     - example_sqls: 3단계에서 작성한 예제 SQL
     - join_specs: 3단계에서 작성한 조인 조건 (해당 시)
     - sql_snippets: 3단계에서 작성한 SQL 스니펫 (해당 시)
   - 생성된 Space ID를 확인합니다
   - `ask_genie` MCP tool로 sample_questions 중 하나를 테스트 질의합니다
   - 테스트 결과를 확인하고 사용자에게 보고합니다

## 출력
- 생성된 Genie Space 정보 (Space ID, 제목)
- 설정된 instructions 요약
- 설정된 joins, sql_expressions 요약 (해당 시)
- 테스트 질의 결과
