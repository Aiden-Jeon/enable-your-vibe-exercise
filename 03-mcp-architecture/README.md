# Section 03: MCP Architecture - 실습 코드

## 사전 준비

### 필수 도구
- **Python 3.11+**: MCP 서버 실행에 필요합니다
- **uv**: Python 패키지 매니저 (권장)

### uv 설치 (미설치 시)
```bash
# macOS / Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

## 실습 파일 목록

| 파일 | 설명 |
|------|------|
| `exercise_01_hello_mcp.py` | Hello MCP - echo, greet 도구를 가진 기본 MCP 서버 |
| `exercise_02_calculator_mcp.py` | Calculator MCP - 사칙연산 도구를 가진 MCP 서버 |

## 실행 방법

### 방법 1: uv로 직접 실행 (권장)
별도의 패키지 설치 없이 바로 실행할 수 있습니다.

```bash
# Exercise 01 실행
uv run --with fastmcp fastmcp run exercise_01_hello_mcp.py

# Exercise 02 실행
uv run --with fastmcp fastmcp run exercise_02_calculator_mcp.py
```

### 방법 2: uv sync 후 실행
```bash
# 프로젝트 루트에서 의존성 설치
uv sync

# Exercise 01 실행
python exercise_01_hello_mcp.py

# Exercise 02 실행
python exercise_02_calculator_mcp.py
```

## Claude Code에서 사용하기

### 1. 설정 파일 생성
프로젝트 루트의 `.claude/settings.local.json` 파일에 아래 내용을 추가합니다:

```json
{
  "mcpServers": {
    "hello-mcp": {
      "command": "uv",
      "args": [
        "run",
        "--with", "fastmcp",
        "fastmcp", "run",
        "03-mcp-architecture/exercise_01_hello_mcp.py"
      ]
    },
    "calculator": {
      "command": "uv",
      "args": [
        "run",
        "--with", "fastmcp",
        "fastmcp", "run",
        "03-mcp-architecture/exercise_02_calculator_mcp.py"
      ]
    }
  }
}
```

### 2. Claude Code 재시작
설정 파일을 저장한 후 Claude Code를 재시작합니다.

### 3. 도구 사용 확인
Claude Code에서 다음과 같이 사용할 수 있습니다:
- "echo 도구로 'Hello World' 메시지를 보내줘"
- "3과 5를 더해줘" (계산기 서버 사용)
- "100을 7로 나눠줘"

## 학습 포인트

1. **FastMCP의 핵심 패턴**: `FastMCP` 인스턴스 생성 -> `@mcp.tool()` 데코레이터로 도구 등록 -> `mcp.run()`으로 서버 실행
2. **타입 힌트의 역할**: Python 타입 힌트(`str`, `float` 등)가 자동으로 MCP 도구의 입력 스키마(JSON Schema)로 변환됩니다
3. **Docstring의 역할**: 함수의 docstring이 도구의 설명(description)으로 사용됩니다. AI 모델이 이 설명을 보고 도구를 선택합니다
4. **에러 처리**: `raise ValueError()`로 에러를 발생시키면 MCP 프로토콜을 통해 클라이언트에 에러가 전달됩니다

## 도전 과제

실습이 끝나면 다음을 시도해보세요:

- `exercise_01_hello_mcp.py`에 문자열을 뒤집는 `reverse` 도구 추가
- `exercise_02_calculator_mcp.py`에 거듭제곱(`power`) 도구 추가
- 새로운 MCP 서버를 처음부터 만들어보기 (예: 단위 변환기, 문자열 유틸리티 등)
