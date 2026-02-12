# Section 05: Skills - 실습 코드

Skills를 활용하여 Genie MCP 서버의 tool들을 고수준 워크플로우로 구성하는 실습 코드입니다.

## 실습 구성

### exercise_genie_skill: genie-space 스킬 만들기 (2-Step)

- **경로**: `exercise_genie_skill/`
- **목표**: SKILL.md 작성 → 레퍼런스로 품질 향상하는 흐름을 체험합니다
- **소요 시간**: 약 25분 (Step 1: 10분 + Step 2: 15분)

| Step | 내용 | 핵심 학습 |
|------|------|-----------|
| Step 1 | SKILL.md 워크플로우 작성 | SKILL.md 구조, MCP tool 호출 |
| Step 2 | 레퍼런스 반영하여 업데이트 | references 활용, 품질 향상 |

## Claude Code로 구현하기

### Step 1: genie-space 워크플로우 작성 (10분)

```bash
# Claude Code 실행
claude

# SKILL.md 템플릿의 TODO를 확인하고 작성 요청
> exercise_genie_skill/SKILL.md에 genie-space 스킬을 작성해줘.
> Genie MCP 서버의 create_genie_space tool로 Space를 생성하고,
> ask_genie tool로 테스트 질의까지 하는 스킬이야.
```

### Step 2: 레퍼런스 반영하여 업데이트 (15분)

```bash
# 레퍼런스를 반영하여 스킬 업데이트 요청
> references/genie-best-practices.md를 참조해서 SKILL.md를 업데이트해줘.
> best practices에 따라 테이블 5개 이하, 명확한 지시사항, 테스트 질의 등을 반영해줘.
```

### Step 3: 실제로 Skill 실행
작성된 SKILL.md를 `.claude/skills/genie-space/` 디렉토리에 배치하여 테스트합니다.

## 사전 준비

- Section 04 (Genie MCP)의 실습을 완료하여 Genie MCP 서버가 동작해야 합니다
- Section 05 (Skills)의 강의 파트 개념을 이해하고 있어야 합니다
- Claude Code가 설치되어 있어야 합니다
