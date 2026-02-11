# Section 05: Skills - 실습 코드

Skills를 활용하여 개발 워크플로우를 구조화하는 실습 코드입니다.

## 실습 구성

### Exercise 01: 간단한 Skill 만들기

- **경로**: `exercise_01_simple_skill/`
- **목표**: SKILL.md의 기본 구조를 이해하고 Claude Code에게 Skill을 작성하도록 요청합니다
- **소요 시간**: 약 10분
- **핵심 학습**: SKILL.md의 3가지 핵심 섹션 (사용법, 처리 절차, 출력 형식)

### Exercise 02: 레퍼런스 파일이 있는 Skill 만들기

- **경로**: `exercise_02_skill_with_refs/`
- **목표**: 레퍼런스 파일을 활용하여 일관된 품질의 코드를 생성하는 Skill을 만듭니다
- **소요 시간**: 약 15분
- **핵심 학습**: references 디렉토리 활용, 컨벤션 기반 코드 생성

## Claude Code로 구현하기

### Step 1: 템플릿 확인
각 exercise 디렉토리의 SKILL.md 템플릿과 README.md를 확인합니다.

### Step 2: Claude Code에게 작성 요청

```bash
# Claude Code 실행
claude

# Exercise 01: 간단한 Skill 작성
> exercise_01_simple_skill/SKILL.md에 data-summary 스킬을 작성해줘.
> CSV 파일을 분석하여 기본 통계와 결측치 현황을 마크다운으로 출력하는 스킬이야.

# Exercise 02: 레퍼런스 활용 Skill 작성
> exercise_02_skill_with_refs/SKILL.md에 api-endpoint 스킬을 작성해줘.
> references/api-conventions.md를 참고하여 FastAPI 엔드포인트를 생성하는 스킬이야.
```

### Step 3: 실제로 Skill 실행
작성된 SKILL.md를 `.claude/skills/` 디렉토리에 배치하여 테스트합니다.

## 사전 준비

- Section 05 (Skills)의 강의 파트 개념을 이해하고 있어야 합니다
- Claude Code가 설치되어 있어야 합니다
