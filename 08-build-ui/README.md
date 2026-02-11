# Section 08: Build UI - UI 만들기

Genie API를 연동한 채팅 UI를 FastAPI로 구현하는 실습입니다.

## 사전 준비

### 필수 패키지 설치

```bash
# 프로젝트 루트에서 실행 (모든 의존성 한 번에 설치)
uv sync
```

### 환경변수 설정 (Exercise 02)

```bash
cp .env.example .env
```

`.env` 파일을 열어 아래 값을 설정합니다:

| 변수 | 설명 |
|------|------|
| `DATABRICKS_HOST` | Databricks 워크스페이스 URL (예: `https://xxx.cloud.databricks.com`) |
| `DATABRICKS_TOKEN` | Databricks Personal Access Token |
| `GENIE_SPACE_ID` | Genie Space ID |

## 실습 내용

### Exercise 01: FastAPI 기본 서버

FastAPI의 기본 구조를 익히는 워밍업 실습입니다.

```bash
python exercise_01_fastapi_basic.py
```

- 접속: http://localhost:8000
- API 문서: http://localhost:8000/docs

**학습 포인트:**
- FastAPI 앱 생성 및 라우트 등록
- HTML 응답과 JSON 응답의 차이
- 자동 생성 Swagger UI 활용

### Exercise 02: Genie 채팅 UI

Genie API를 연동한 완전한 채팅 애플리케이션입니다.

```bash
cd exercise_02_genie_chatbot
python app.py
```

- 접속: http://localhost:8000

**학습 포인트:**
- FastAPI로 정적 파일(HTML/CSS/JS) 서빙
- Pydantic 모델로 요청/응답 스키마 정의
- Genie API 호출 및 폴링 패턴
- fetch API를 이용한 프론트엔드-백엔드 통신
- 채팅 UI 구현 패턴

## 파일 구조

```
code/
├── exercise_01_fastapi_basic.py    # Exercise 01: FastAPI 기본 서버
├── exercise_02_genie_chatbot/      # Exercise 02: Genie 채팅 UI
│   ├── app.py                      # FastAPI 백엔드
│   └── static/
│       ├── index.html              # 채팅 UI HTML
│       ├── style.css               # 다크 테마 스타일
│       └── app.js                  # 채팅 프론트엔드 로직
├── .env.example                    # 환경변수 템플릿
└── README.md                       # 이 파일
```

## 트러블슈팅

### 포트가 이미 사용 중인 경우

```bash
# 기존 프로세스 종료
lsof -i :8000 | grep LISTEN
kill -9 <PID>
```

### Databricks 연결 오류

- `DATABRICKS_HOST`에 `https://`가 포함되어 있는지 확인
- `DATABRICKS_TOKEN`이 유효한지 확인
- `GENIE_SPACE_ID`가 올바른지 확인

### 모듈을 찾을 수 없는 경우

```bash
# 프로젝트 루트에서 실행
uv sync
```
