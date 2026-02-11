# API 컨벤션

## 응답 형식
모든 API 응답은 다음 구조를 따릅니다:
```json
{
  "status": "success" | "error",
  "data": { ... },
  "message": "설명"
}
```

## 네이밍
- 엔드포인트: kebab-case (/api/v1/user-profiles)
- 함수명: snake_case (get_user_profiles)
- 모델명: PascalCase (UserProfile)

## 에러 처리
- HTTPException 사용
- 상태 코드: 400 (잘못된 요청), 404 (없음), 500 (서버 에러)
