# Exercise 01: 간단한 Skill 만들기

## 개요

SKILL.md 템플릿을 Claude Code에게 전달하여 간단한 Skill을 완성합니다.

## 파일 구조

```
exercise_01_simple_skill/
└── SKILL.md          # 스킬 템플릿 (TODO)
```

## Claude Code로 구현하기

### Step 1: 템플릿 확인
`SKILL.md` 파일을 열어 TODO 주석을 확인합니다.

### Step 2: Claude Code에게 작성 요청
```bash
claude

# 프롬프트 예시
> SKILL.md에 data-summary 스킬을 작성해줘.
> CSV 파일을 분석하여 요약 보고서를 마크다운으로 출력하는 스킬이야.
> 처리 절차: CSV 읽기 → 기본 통계 → 수치형 기술 통계 → 결측치 현황 → 마크다운 출력
```

### Step 3: Skill 테스트
완성된 SKILL.md를 `.claude/skills/data-summary/SKILL.md`에 배치하고 Claude Code에서 실행합니다:
```
/data-summary sample.csv
```

## 학습 포인트

### SKILL.md의 기본 구조

Skill은 최소한 다음 세 가지 섹션을 포함해야 합니다:

- **사용법**: Skill을 호출하는 방법과 인자를 정의합니다
- **처리 절차**: AI가 수행할 단계별 작업을 순서대로 기술합니다
- **출력 형식**: 최종 결과물의 형태를 명시합니다

### 실습 과제

1. Claude Code에게 SKILL.md를 작성하도록 요청합니다
2. 생성된 SKILL.md를 확인하고 필요시 수정합니다
3. 처리 절차에 "상위 5개 빈도 값 출력" 단계를 추가해봅니다
4. 출력 형식을 "JSON 형식"으로 변경하고 결과 차이를 비교합니다
