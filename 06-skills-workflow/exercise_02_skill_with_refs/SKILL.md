# api-endpoint 스킬

FastAPI 엔드포인트 코드를 생성합니다.

## 사용법
/api-endpoint [엔드포인트설명]

## 처리 절차
1. `references/api-conventions.md`를 읽어 API 컨벤션 확인
2. 엔드포인트 설명을 분석하여 HTTP 메서드, 경로, 파라미터 결정
3. Pydantic 모델 정의
4. FastAPI 라우터 함수 생성
5. 컨벤션에 맞는 에러 처리 추가

## 출력
- 엔드포인트 코드 (Python)
- Pydantic 모델 (Python)
