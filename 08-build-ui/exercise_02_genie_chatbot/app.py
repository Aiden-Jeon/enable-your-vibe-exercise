"""
Exercise 02: Genie 챗봇 - FastAPI 백엔드
Genie API를 연동한 채팅 애플리케이션 백엔드

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
    if not all([DATABRICKS_HOST, DATABRICKS_TOKEN, GENIE_SPACE_ID]):
        raise HTTPException(status_code=500, detail="Databricks 환경변수가 설정되지 않았습니다")

    try:
        # 대화 생성 또는 기존 대화 사용
        if req.conversation_id:
            conversation_id = req.conversation_id
        else:
            resp = httpx.post(f"{base_url}/conversations", headers=headers)
            resp.raise_for_status()
            conversation_id = resp.json()["conversation_id"]

        # 메시지 전송
        resp = httpx.post(
            f"{base_url}/conversations/{conversation_id}/messages",
            headers=headers,
            json={"content": req.message},
        )
        resp.raise_for_status()
        message_id = resp.json()["message_id"]

        # 결과 폴링
        url = f"{base_url}/conversations/{conversation_id}/messages/{message_id}"
        for _ in range(30):
            resp = httpx.get(url, headers=headers)
            resp.raise_for_status()
            data = resp.json()
            status = data.get("status", "")
            if status == "COMPLETED":
                break
            if status in ("FAILED", "CANCELLED"):
                raise HTTPException(status_code=500, detail=f"Genie 질의 실패: {status}")
            time.sleep(2)
        else:
            raise HTTPException(status_code=504, detail="Genie 응답 시간 초과")

        # 응답 파싱
        attachments = data.get("attachments", [])
        reply_parts = []
        sql = None
        for att in attachments:
            if "text" in att:
                reply_parts.append(att["text"].get("content", ""))
            if "query" in att:
                sql = att["query"].get("query", "")
                reply_parts.append(f"실행된 SQL:\n```sql\n{sql}\n```")

        reply = "\n\n".join(reply_parts) if reply_parts else "응답을 파싱할 수 없습니다."
        return ChatResponse(reply=reply, conversation_id=conversation_id, sql=sql)

    except httpx.HTTPError as e:
        raise HTTPException(status_code=502, detail=f"Genie API 호출 실패: {str(e)}")


@app.get("/api/health")
async def health():
    return {"status": "healthy"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
