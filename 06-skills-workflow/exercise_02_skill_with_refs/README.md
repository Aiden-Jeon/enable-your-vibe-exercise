# Exercise 02: 레퍼런스 파일이 있는 Skill 만들기

## 개요

`references/` 디렉토리의 API 컨벤션을 활용하여 일관된 코드를 생성하는 Skill을 작성합니다.

## 파일 구조

```
exercise_02_skill_with_refs/
├── SKILL.md                          # 스킬 템플릿 (TODO)
└── references/
    └── api-conventions.md            # API 컨벤션 레퍼런스
```

## Claude Code로 구현하기

### Step 1: 레퍼런스 파일 확인
`references/api-conventions.md`를 읽어 API 컨벤션을 파악합니다.

### Step 2: Claude Code에게 작성 요청
```bash
claude

# 프롬프트 예시
> exercise_02_skill_with_refs/SKILL.md에 api-endpoint 스킬을 작성해줘.
> references/api-conventions.md의 컨벤션을 따르는 FastAPI 엔드포인트를 생성하는 스킬이야.
> 처리 절차에서 반드시 references 파일을 먼저 읽도록 해줘.
```

### Step 3: Skill 테스트
완성된 디렉토리를 `.claude/skills/api-endpoint/`에 배치하고 실행합니다:
```
/api-endpoint "사용자 프로필 조회 API"
```

## 학습 포인트

### 레퍼런스 파일의 역할

- **일관성 보장**: 팀의 모든 구성원이 동일한 컨벤션으로 코드를 생성합니다
- **품질 향상**: 매번 컨벤션을 설명하지 않아도 됩니다
- **유지보수 용이**: 컨벤션이 변경되면 레퍼런스 파일만 수정하면 됩니다

### SKILL.md에서 레퍼런스 참조 방법

처리 절차에서 레퍼런스 파일을 읽으라는 지시를 명시합니다:
```markdown
## 처리 절차
1. `references/api-conventions.md`를 읽어 API 컨벤션 확인
```

### 실습 과제

1. Claude Code에게 SKILL.md를 작성하도록 요청합니다
2. `/api-endpoint "사용자 프로필 조회 API"`를 실행합니다
3. `api-conventions.md`의 응답 형식을 변경하고 다시 실행합니다
4. 두 결과를 비교하여 레퍼런스 파일의 영향을 확인합니다
