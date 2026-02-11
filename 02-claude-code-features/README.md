# Section 02: Claude Code Features - 실습 코드

## 사전 준비

### 필수 도구
- **Python 3.11+**: 함수 실행에 필요합니다
- **uv**: Python 패키지 매니저 (권장)
- **Claude Code**: Vibe Coding 실습에 사용

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
| `exercise_01_fibonacci.py` | Fibonacci 함수 스켈레톤 (TODO) |
| `exercise_02_fibonacci_test.py` | Fibonacci 테스트 스켈레톤 (TODO) |

## Claude Code로 구현하기

### Step 1: 스켈레톤 파일 확인
각 파일을 열어 TODO 주석과 요구사항을 확인합니다.

### Step 2: Claude Code에게 구현 요청
```bash
# Claude Code 실행
claude

# 프롬프트 예시
> exercise_01_fibonacci.py의 TODO를 구현해줘
> exercise_02_fibonacci_test.py의 테스트를 구현해줘
```

### Step 3: 실행 및 테스트

#### 함수 실행 확인
```bash
# fibonacci 함수 실행
uv run exercise_01_fibonacci.py
```

#### 테스트 실행
```bash
# pytest로 테스트 실행
uv run --with pytest pytest exercise_02_fibonacci_test.py -v
```

## 학습 포인트

1. **Claude Code 기본 사용법**: 자연어로 함수 구현을 요청하는 경험
2. **코드 생성 품질**: 타입 힌트, docstring, 에러 처리가 포함된 코드 생성 확인
3. **테스트 생성**: edge case를 포함한 테스트 자동 생성
4. **반복 개선**: 테스트 실패 시 Claude Code에게 수정 요청하는 워크플로우 체험

## 도전 과제

실습이 끝나면 다음을 시도해보세요:

- `fibonacci` 함수에 메모이제이션(memoization) 추가 요청
- 재귀(recursive) 방식의 fibonacci 구현 요청
- 두 구현의 성능 비교 테스트 작성 요청
