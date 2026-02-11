# Genie Chatbot UI 요구사항

Claude Code에게 이 요구사항을 전달하여 채팅 UI를 생성하세요.

## 필요한 파일
- `index.html` — 채팅 UI HTML
- `style.css` — 다크 테마 스타일
- `app.js` — 채팅 프론트엔드 로직

## UI 요구사항

### 레이아웃
- 중앙 정렬된 채팅 컨테이너 (최대 700px)
- 헤더: 제목 + 설명
- 메시지 영역: 스크롤 가능
- 입력 영역: 텍스트 입력 + 전송 버튼

### 디자인
- 다크 테마 (배경: #1a1a2e, 강조: #e94560)
- 사용자 메시지: 오른쪽 정렬
- 봇 메시지: 왼쪽 정렬
- 코드 블록 지원 (SQL 결과 표시용)

### 기능
- Enter 키로 메시지 전송
- 전송 중 로딩 표시
- `POST /api/chat`으로 메시지 전송
- `conversation_id`로 대화 이어가기
- 에러 처리 (네트워크 오류, API 오류)

### API 인터페이스
```
POST /api/chat
Request:  { "message": "질문", "conversation_id": "optional" }
Response: { "reply": "응답", "conversation_id": "id", "sql": "optional" }
```
