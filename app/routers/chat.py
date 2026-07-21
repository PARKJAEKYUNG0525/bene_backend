from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.database import get_db
from app.db.models.user import User
from app.db.scheme.chat import ChatAskRequest
from app.services.chat import ChatService
from app.core.jwt_handle import get_current_user

router = APIRouter(prefix="/chat", tags=["Chat"])


# 하이브리드 검색(BM25+Chroma, RRF) 기반 정책 RAG 챗봇
@router.post("/ask")
async def ask_chat(
    data: ChatAskRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return await ChatService.ask_chat_svc(db, current_user.user_id, data.query, data.top_k)
