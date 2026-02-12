# Exercise: Genie Space 라이프사이클 에이전트 만들기

## 개요

이 실습에서는 Genie Space 라이프사이클을 담당하는 세 가지 에이전트를 만들어봅니다.
`genie-space-designer`(Space 설계), `genie-instructor`(Instructions 작성), `genie-tester`(품질 테스트)

## 파일 구조

```
exercise_genie_agents/
├── README.md                                    # 이 파일
├── genie-space-designer.md                      # Step 1: Space 설계 에이전트 템플릿 (TODO)
├── genie-instructor.md                          # Step 2: Instructions 작성 에이전트 템플릿 (TODO)
├── genie-tester.md                              # Bonus: 품질 테스트 에이전트 템플릿 (TODO)
└── references/
    ├── genie-best-practices.md                  # Genie Space 설계 가이드
    └── serialized-space-instructions.md         # Instructions 블록 구조 가이드 (Step 2에서 활용)
```

## Step 1: `@genie-space-designer` 에이전트 만들기 (10분)

### 목표

테이블 스키마를 분석하고 최적의 Genie Space 구성을 설계하는 에이전트를 만듭니다.

### 진행 방법

1. `genie-space-designer.md` 파일을 열어 TODO 항목을 확인합니다
2. Claude Code에게 TODO를 채워달라고 요청합니다:
   ```
   > genie-space-designer.md 템플릿의 TODO를 채워서 genie-space-designer 에이전트를 완성해줘.
   >   테이블 스키마를 분석하고 Space 구성을 설계하는 역할이야.
   ```
3. 완성된 파일을 `.claude/agents/genie-space-designer.md`에 복사합니다
4. `@genie-space-designer`로 호출하여 테스트합니다:
   ```
   > @genie-space-designer catalog.schema의 테이블을 분석해서 Space를 설계해줘
   ```

### 학습 포인트

- **역할 정의**: "당신은 ~입니다"로 시작하는 명확한 역할 부여
- **제약 조건**: 분석만 수행하고 생성은 하지 않도록 범위 제한
- **출력 형식**: 테이블 분석, 추천 구성, Sample Questions 등 구조화

## Step 2: `@genie-instructor` 에이전트 만들기 (15분)

### 목표

Genie Space의 instructions 블록(text_instructions, example_sqls, sql_snippets)을 작성하는 에이전트를 만듭니다.

### 진행 방법

1. `references/serialized-space-instructions.md`를 먼저 읽어 instructions 구조를 파악합니다
2. `genie-instructor.md` 파일을 열어 TODO 항목을 확인합니다
3. Claude Code에게 레퍼런스를 참고하여 TODO를 채워달라고 요청합니다:
   ```
   > genie-instructor.md 템플릿의 TODO를 채워줘.
   >   references/serialized-space-instructions.md를 참고해서 instructions 블록을 작성하는 에이전트를 만들어줘.
   ```
4. 완성된 파일을 `.claude/agents/genie-instructor.md`에 복사합니다
5. `@genie-instructor`로 호출하여 테스트합니다:
   ```
   > @genie-instructor designer 결과를 기반으로 instructions를 작성해줘
   ```

### 학습 포인트

- **레퍼런스 활용**: serialized_space 구조를 에이전트 지식으로 내재화
- **도메인 전문성**: instructions 블록의 각 섹션을 이해하고 작성
- **역할 분담**: designer의 결과를 입력으로 받아 instructions를 출력

## Bonus: `@genie-tester` 에이전트 만들기 (선택)

### 목표

완성된 Space에 질의하여 응답 품질을 평가하는 에이전트를 만듭니다.

### 진행 방법

1. `genie-tester.md` 파일을 열어 TODO 항목을 확인합니다
2. Claude Code에게 TODO를 채워달라고 요청합니다
3. 완성된 파일을 `.claude/agents/genie-tester.md`에 복사하고 테스트합니다

## 체크리스트

완성된 에이전트를 다음 기준으로 검증하세요:

- [ ] 역할이 명확하게 정의되어 있는가?
- [ ] 제약 조건이 적절히 설정되어 있는가?
- [ ] 출력 형식이 구조화되어 있는가?
- [ ] 단일 책임 원칙을 따르는가? (designer ≠ instructor ≠ tester)
- [ ] 에이전트를 호출했을 때 기대한 역할로 동작하는가?
