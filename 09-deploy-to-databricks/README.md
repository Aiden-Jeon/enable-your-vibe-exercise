# Section 09: Deploy to Databricks - Databricks 배포

## 학습 목표

- Databricks Apps의 개념과 배포 구조를 이해한다
- `app.yaml` 설정 파일 작성법을 학습한다
- Databricks CLI를 사용하여 앱을 배포한다

## 사전 준비

### 1. Databricks CLI 설치

```bash
pip install databricks-cli
```

### 2. CLI 인증 설정

```bash
databricks configure --token
# Databricks Host: https://your-workspace.cloud.databricks.com
# Token: your-personal-access-token
```

### 3. 워크스페이스 접근 권한

- Databricks 워크스페이스에 로그인 가능해야 합니다
- Apps 생성 권한이 필요합니다
- Genie Space에 접근 가능해야 합니다

### 4. 환경변수 설정

```bash
cp .env.example .env
# .env 파일을 편집하여 실제 값을 입력합니다
```

## app.yaml 설정 설명

`app.yaml`은 Databricks Apps의 핵심 설정 파일입니다.

```yaml
command:        # 앱 실행 명령어 (리스트 형태)
  - uvicorn
  - app:app
  - --host
  - "0.0.0.0"
  - --port
  - "8000"

env:            # 환경변수 설정
  - name: DATABRICKS_HOST
    value: "{{DATABRICKS_HOST}}"       # 일반 값
  - name: DATABRICKS_TOKEN
    valueFrom: secret                   # Databricks 시크릿에서 가져옴
  - name: GENIE_SPACE_ID
    value: "{{GENIE_SPACE_ID}}"
```

| 필드 | 설명 |
|------|------|
| `command` | 앱을 시작하는 명령어를 리스트로 지정합니다 |
| `env[].name` | 환경변수 이름 |
| `env[].value` | 환경변수 값 (직접 지정) |
| `env[].valueFrom` | `secret`으로 지정하면 Databricks 시크릿에서 값을 가져옵니다 |

## 배포 단계별 가이드

### Step 1: 프로젝트 구조 확인

```bash
python exercise_01_prepare_deploy.py
```

필요한 파일들이 모두 있는지 확인합니다:
- `app.py` - FastAPI 서버
- `app.yaml` - Databricks Apps 설정
- `requirements.txt` - Python 의존성
- `static/` - 정적 파일 (HTML, CSS, JS)

### Step 2: 로컬 테스트

배포 전에 로컬에서 먼저 테스트합니다:

```bash
uvicorn app:app --port 8000
# 브라우저에서 http://localhost:8000 접속
```

### Step 3: 앱 생성

```bash
databricks apps create genie-chatbot
```

### Step 4: 앱 배포

```bash
databricks apps deploy genie-chatbot --source-code-path .
```

### Step 5: 상태 확인

```bash
databricks apps get genie-chatbot
```

RUNNING 상태가 되면 배포가 완료된 것입니다.

### Step 6: URL 접속

출력된 URL로 브라우저에서 접속하여 앱이 정상 동작하는지 확인합니다.

## 트러블슈팅 팁

### 앱이 시작되지 않는 경우

- **포트 설정 확인**: `app.yaml`의 port와 `app.py`의 port가 일치하는지 확인
- **`$PORT` 환경변수**: Databricks Apps가 주입하는 PORT 환경변수를 사용하는 것을 권장

### ModuleNotFoundError 발생

- `requirements.txt`에 모든 의존성이 포함되어 있는지 확인
- `pyproject.toml`을 사용하는 경우 해당 파일이 프로젝트 루트에 있는지 확인

### Genie API 호출 실패

- Databricks 시크릿에 토큰이 올바르게 설정되어 있는지 확인
- GENIE_SPACE_ID가 유효한 Space ID인지 확인
- 워크스페이스에서 Genie Space에 접근 권한이 있는지 확인

### 로그 확인 방법

```bash
# 앱 로그 조회
databricks apps logs genie-chatbot

# 실시간 로그 스트리밍
databricks apps logs genie-chatbot --follow
```

## 학습 포인트

1. **Databricks Apps**는 별도 인프라 없이 웹앱을 배포할 수 있는 서비스입니다
2. **app.yaml** 하나로 실행 환경과 환경변수를 정의합니다
3. **시크릿 관리**: 민감한 정보는 `valueFrom: secret`으로 안전하게 관리합니다
4. **배포 워크플로우**: create -> deploy -> 확인의 3단계로 간편하게 배포합니다
5. **전체 여정**: MCP 서버 -> Skill -> UI -> 배포로 이어지는 Vibe Coding 워크플로우를 완성했습니다
