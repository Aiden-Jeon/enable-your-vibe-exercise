# 실습: genie-space 스킬 만들기 (2-Step)

Section 04에서 만든 Genie MCP 서버의 tool들을 활용하는 Skill을 작성합니다.
하나의 스킬을 **2단계**로 발전시키며, "기본 작성 → 레퍼런스로 품질 향상"의 흐름을 체험합니다.

## 파일 구조

```
exercise_genie_skill/
├── SKILL.md                              ← TODO 템플릿 (여기에 스킬을 작성)
├── references/
│   └── genie-best-practices.md           ← Databricks 공식문서 기반 가이드
└── README.md                             ← 이 파일
```

## MCP Tools 참조 (Section 04 기준)

| Tool | 설명 |
|------|------|
| `create_genie_space` | Space 생성 (title, description, warehouse_id, tables, instructions, sample_questions 등) |
| `ask_genie` | 자연어 질의 (space_id, question) |
| `continue_conversation` | 후속 질의 (space_id, conversation_id, question) |

---

## Step 1: genie-space 워크플로우 작성 (10분)

### 1-1. 템플릿 확인
`SKILL.md` 파일을 열어 TODO 주석을 확인합니다.

### 1-2. Claude Code에게 작성 요청
```bash
claude

# 프롬프트 예시
> exercise_genie_skill/SKILL.md에 genie-space 스킬을 작성해줘.
> Genie MCP 서버의 create_genie_space tool로 Space를 생성하고,
> ask_genie tool로 테스트 질의까지 하는 스킬이야.
```

### 1-3. Skill 배치 및 테스트
완성된 스킬을 `.claude/skills/`에 배치하고 실행합니다:
```bash
# 실습 디렉토리를 .claude/skills/에 복사
cp -r exercise_genie_skill/ .claude/skills/genie-space/
```

배치 후 Claude Code에서 스킬을 호출합니다:
```
/genie-space "패션 추천 분석" "shared.fashion_recommendations"
```

**기대 결과:**
1. `create_genie_space` → "패션 추천 분석" Space가 생성됨
2. `ask_genie` → 테스트 질의가 실행됨
3. Space ID와 질의 응답 결과가 출력됨

### 체크포인트
- [ ] SKILL.md에 사용법/처리 절차/출력 형식이 정의되어 있는가?
- [ ] 처리 절차에 `create_genie_space`, `ask_genie` MCP tool 호출이 포함되어 있는가?
- [ ] `/genie-space` 실행 시 Space가 생성되고 질의까지 되는가?

---

## Step 2: 레퍼런스를 반영하여 스킬 업데이트 (15분)

### 2-1. 레퍼런스 파일 확인
`references/genie-best-practices.md`를 읽어 Databricks 공식 best practices를 확인합니다.

### 2-2. Claude Code에게 업데이트 요청
```bash
# 프롬프트 예시
> references/genie-best-practices.md를 참조해서 SKILL.md를 업데이트해줘.
> best practices에 따라 테이블 5개 이하, 명확한 지시사항, 테스트 질의 등을 반영해줘.
```

### 2-3. 재배치 및 개선 확인
업데이트된 스킬을 다시 배치하고 실행하여 Step 1과의 차이를 확인합니다:
```bash
# 업데이트된 스킬을 다시 배치 (기존 덮어쓰기)
cp -r exercise_genie_skill/ .claude/skills/genie-space/
```

```
/exercise_genie_skill "패션 추천 분석" "shared.fashion_recommendations"
```

**기대 결과 (Step 1 대비 개선점):**
- 테이블 5개 이하 제한 등 best practices가 자동 적용됨
- 명확한 지시사항(instructions)이 Space에 포함됨
- 테스트 질의가 best practices에 맞게 개선됨

### 체크포인트
- [ ] SKILL.md 처리 절차에 "레퍼런스 파일을 읽어 컨벤션 확인" 단계가 추가되었는가?
- [ ] 테이블 5개 이하 제한, 명확한 지시사항 등 best practices가 반영되었는가?
- [ ] Step 1 결과와 비교하여 어떤 점이 개선되었는가?

## 사전 준비

- Section 04 (Genie MCP) 실습을 완료하여 Genie MCP 서버가 동작해야 합니다
- Section 05 (Skills) 강의 파트 개념을 이해하고 있어야 합니다
- Claude Code가 설치되어 있어야 합니다
