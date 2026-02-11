"""
Exercise 01: FastAPI 기본 서버
FastAPI로 간단한 웹 서버를 만듭니다.

요구사항:
1. GET / : HTML 메인 페이지 (제목, 서버 상태 안내)
2. GET /api/health : 헬스 체크 JSON 응답
3. POST /api/echo : 메시지를 받아 그대로 반환하는 에코 API

실행: python exercise_01_fastapi_basic.py
접속: http://localhost:8000
"""
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import uvicorn

app = FastAPI(title="Hello FastAPI")


@app.get("/", response_class=HTMLResponse)
async def home():
    """메인 페이지 — HTML로 서버 상태를 보여줍니다."""
    # TODO: HTML 문자열을 반환하세요
    # 힌트: 제목, 서버 상태 메시지, /docs 링크를 포함
    raise NotImplementedError("home 엔드포인트를 구현하세요")


@app.get("/api/health")
async def health():
    """헬스 체크 API — 서버 상태를 JSON으로 반환합니다."""
    # TODO: {"status": "healthy", "message": "..."} 형태로 반환하세요
    raise NotImplementedError("health 엔드포인트를 구현하세요")


@app.post("/api/echo")
async def echo(message: str):
    """에코 API — 입력받은 메시지를 그대로 반환합니다."""
    # TODO: {"status": "success", "data": {"echo": message}} 형태로 반환하세요
    raise NotImplementedError("echo 엔드포인트를 구현하세요")


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
