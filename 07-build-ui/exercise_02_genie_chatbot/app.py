"""
Exercise 02: Genie 챗봇 - FastAPI 백엔드
Genie API를 연동한 채팅 애플리케이션 백엔드

요구사항:
1. POST /api/chat : Genie에 질문을 보내고 결과를 반환
   - 새 대화 생성 또는 기존 대화 이어가기
   - 메시지 전송 → 폴링 → 응답 파싱
2. GET / : 정적 HTML 파일 서빙
3. GET /api/health : 헬스 체크

실행: python app.py
접속: http://localhost:8000
"""
import os
import time

import httpx
import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel

load_dotenv()

DATABRICKS_HOST = os.getenv("DATABRICKS_HOST", "")
DATABRICKS_TOKEN = os.getenv("DATABRICKS_TOKEN", "")
GENIE_SPACE_ID = os.getenv("GENIE_SPACE_ID", "")

app = FastAPI(title="Genie Chatbot")

# 정적 파일 서빙
app.mount("/static", StaticFiles(directory="static"), name="static")


class ChatRequest(BaseModel):
    message: str
    conversation_id: str | None = None


class ChatResponse(BaseModel):
    reply: str
    conversation_id: str
    sql: str | None = None


headers = {
    "Authorization": f"Bearer {DATABRICKS_TOKEN}",
    "Content-Type": "application/json",
}
base_url = f"{DATABRICKS_HOST}/api/2.0/genie/spaces/{GENIE_SPACE_ID}"


@app.get("/")
async def home():
    return FileResponse("static/index.html")


@app.post("/api/chat", response_model=ChatResponse)
async def chat(req: ChatRequest):
    """Genie에 질문을 보내고 결과를 반환합니다.

    흐름:
    1. conversation_id가 없으면 새 대화 생성 (POST /conversations)
    2. 메시지 전송 (POST /conversations/{id}/messages)
    3. 결과 폴링 (GET /conversations/{id}/messages/{msg_id})
    4. 응답 파싱 (attachments에서 text/query 추출)
    """
    if not all([DATABRICKS_HOST, DATABRICKS_TOKEN, GENIE_SPACE_ID]):
        raise HTTPException(status_code=500, detail="Databricks 환경변수가 설정되지 않았습니다")

    # TODO: Genie API를 호출하여 채팅 기능을 구현하세요
    # 힌트:
    # 1. req.conversation_id가 없으면 POST {base_url}/conversations로 새 대화 생성
    # 2. POST {base_url}/conversations/{conversation_id}/messages로 메시지 전송
    # 3. GET {url}로 폴링하여 status가 "COMPLETED"될 때까지 대기
    # 4. attachments에서 text.content와 query.query를 추출
    # 5. ChatResponse(reply=..., conversation_id=..., sql=...)로 반환
    raise NotImplementedError("chat 엔드포인트를 구현하세요")


@app.get("/api/health")
async def health():
    return {"status": "healthy"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
