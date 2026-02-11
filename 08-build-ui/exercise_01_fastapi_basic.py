"""
Exercise 01: FastAPI 기본 서버
FastAPI로 간단한 웹 서버를 만듭니다.

실행: python exercise_01_fastapi_basic.py
접속: http://localhost:8000
"""
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import uvicorn

app = FastAPI(title="Hello FastAPI")


@app.get("/", response_class=HTMLResponse)
async def home():
    """메인 페이지"""
    return """
    <!DOCTYPE html>
    <html>
    <head><title>Hello FastAPI</title></head>
    <body style="font-family: sans-serif; max-width: 600px; margin: 50px auto; background: #1a1a2e; color: #eee;">
        <h1 style="color: #e94560;">🚀 Hello FastAPI!</h1>
        <p>FastAPI 서버가 정상적으로 실행 중입니다.</p>
        <p>API 문서: <a href="/docs" style="color: #ff6b81;">/docs</a></p>
    </body>
    </html>
    """


@app.get("/api/health")
async def health():
    """헬스 체크 API"""
    return {"status": "healthy", "message": "서버가 정상 동작 중입니다"}


@app.post("/api/echo")
async def echo(message: str):
    """에코 API - 입력받은 메시지를 그대로 반환"""
    return {"status": "success", "data": {"echo": message}}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
