# Section 08: Build UI - UI 만들기

Genie API를 연동한 채팅 UI를 Claude Code와 함께 구현하는 실습입니다.

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

## Claude Code로 구현하기

### Exercise 01: FastAPI 기본 서버

#### Step 1: 스켈레톤 확인
`exercise_01_fastapi_basic.py`의 TODO 주석을 확인합니다.

#### Step 2: Claude Code에게 구현 요청
```bash
claude

> exercise_01_fastapi_basic.py의 TODO를 구현해줘
```

#### Step 3: 실행 및 테스트
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

#### Step 1: 스켈레톤 확인
- `exercise_02_genie_chatbot/app.py`의 TODO를 확인합니다
- `exercise_02_genie_chatbot/static/GUIDE.md`의 UI 요구사항을 확인합니다

#### Step 2: Claude Code에게 구현 요청
```bash
cd exercise_02_genie_chatbot
claude

# 백엔드 구현
> app.py의 chat 엔드포인트 TODO를 구현해줘

# 프론트엔드 생성
> static/GUIDE.md의 요구사항을 읽고 index.html, style.css, app.js를 생성해줘
```

#### Step 3: 실행 및 테스트
```bash
python app.py
```
- 접속: http://localhost:8000

**학습 포인트:**
- FastAPI로 정적 파일(HTML/CSS/JS) 서빙
- Pydantic 모델로 요청/응답 스키마 정의
- Genie API 호출 및 폴링 패턴
- Claude Code로 프론트엔드 UI 생성

## 파일 구조

```
code/
├── exercise_01_fastapi_basic.py       # 스켈레톤 (TODO)
├── exercise_02_genie_chatbot/
│   ├── app.py                         # 스켈레톤 (TODO)
│   └── static/
│       └── GUIDE.md                   # UI 요구사항 가이드
├── .env.example
└── README.md
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
