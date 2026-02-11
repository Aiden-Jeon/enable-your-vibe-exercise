# Section 08: Deploy to Databricks - Databricks 배포

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

### 3. 환경변수 설정

```bash
cp .env.example .env
# .env 파일을 편집하여 실제 값을 입력합니다
```

## app.yaml 설정 설명

`app.yaml`은 Databricks Apps의 핵심 설정 파일입니다. 참고용으로 포함되어 있습니다.

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
    value: "{{DATABRICKS_HOST}}"
  - name: DATABRICKS_TOKEN
    valueFrom: secret
  - name: GENIE_SPACE_ID
    value: "{{GENIE_SPACE_ID}}"
```

## Claude Code로 구현하기

### Step 1: 스켈레톤 확인
`exercise_01_prepare_deploy.py`의 TODO 주석을 확인합니다.

### Step 2: Claude Code에게 구현 요청
```bash
claude

> exercise_01_prepare_deploy.py의 TODO를 구현해줘
> app.yaml을 참고해서 create_app_yaml 함수를 구현하고,
> check_project_structure에서 배포에 필요한 파일을 확인해줘
```

### Step 3: 실행 및 테스트
```bash
python exercise_01_prepare_deploy.py
```

## 배포 단계별 가이드

### Step 1: 프로젝트 구조 확인

```bash
python exercise_01_prepare_deploy.py
```

### Step 2: 로컬 테스트

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

## 트러블슈팅 팁

### 앱이 시작되지 않는 경우
- **포트 설정 확인**: `app.yaml`의 port와 `app.py`의 port가 일치하는지 확인

### Genie API 호출 실패
- Databricks 시크릿에 토큰이 올바르게 설정되어 있는지 확인
- GENIE_SPACE_ID가 유효한 Space ID인지 확인

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
