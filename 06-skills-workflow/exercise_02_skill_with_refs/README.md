# Exercise 02: 레퍼런스 파일이 있는 Skill 만들기

## 개요

이 예제는 레퍼런스 파일을 활용하는 Skill을 보여줍니다. `references/` 디렉토리에 API 컨벤션 파일을 배치하여 AI가 항상 팀의 표준에 맞는 코드를 생성하도록 합니다.

## 파일 구조

```
exercise_02_skill_with_refs/
├── SKILL.md                          # 스킬 정의 파일
└── references/
    └── api-conventions.md            # API 컨벤션 레퍼런스
```

## 사용 방법

1. `SKILL.md`와 `references/api-conventions.md`의 내용을 확인합니다
2. 실제 프로젝트에서 사용하려면 `.claude/skills/api-endpoint/` 경로에 전체 디렉토리를 배치합니다
3. Claude Code에서 `/api-endpoint "사용자 프로필 조회 API"` 형태로 실행합니다

## 학습 포인트

### 레퍼런스 파일의 역할

레퍼런스 파일은 AI에게 "이 기준에 맞춰 코드를 생성하라"고 알려주는 가이드입니다.

- **일관성 보장**: 팀의 모든 구성원이 동일한 컨벤션으로 코드를 생성합니다
- **품질 향상**: 매번 컨벤션을 설명하지 않아도 됩니다
- **유지보수 용이**: 컨벤션이 변경되면 레퍼런스 파일만 수정하면 됩니다

### SKILL.md에서 레퍼런스 참조 방법

처리 절차에서 레퍼런스 파일을 읽으라는 지시를 명시합니다:

```markdown
## 처리 절차
1. `references/api-conventions.md`를 읽어 API 컨벤션 확인
```

이렇게 하면 AI는 해당 파일을 먼저 읽고, 그 내용에 기반하여 코드를 생성합니다.

### 실습 과제

1. `SKILL.md`와 `references/api-conventions.md`의 관계를 파악합니다
2. `/api-endpoint "사용자 프로필 조회 API"`를 실행합니다
3. `api-conventions.md`의 응답 형식을 다음과 같이 변경하고 다시 실행합니다:
   ```json
   {
     "code": 200,
     "result": { ... },
     "timestamp": "ISO-8601"
   }
   ```
4. 두 결과를 비교하여 레퍼런스 파일의 영향을 확인합니다
