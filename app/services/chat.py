from sqlalchemy.ext.asyncio import AsyncSession

from app.services.ai_client import AiClient
from app.services.recommendation import RecommendationService


class ChatService:

    @staticmethod
    async def ask_chat_svc(db: AsyncSession, user_id: int, query: str, top_k: int = 3) -> dict:
        """
        bene_ai의 하이브리드 검색(BM25+Chroma) RAG 챗봇에 질문하고, sources를 기존
        추천 카드와 동일한 형태(apply_period_type/link/required_fields/is_bookmarked 등)로
        풍부하게 만들어 돌려준다. RecommendationService의 attach 헬퍼들은 버킷 키 구성과
        무관하게 동작하므로("sources" 버킷 하나만 있어도) 그대로 재사용한다.
        """
        result = await AiClient.ask_chat(query, top_k)

        wrapped = {"sources": result["sources"]}
        wrapped = await RecommendationService._attach_policy_cards(db, wrapped)
        wrapped = await RecommendationService._attach_db_policy_ids(db, wrapped)
        wrapped = await RecommendationService._attach_income_required_fields(db, wrapped)
        wrapped = await RecommendationService._attach_bookmark_flags(db, user_id, wrapped)

        return {
            "answer": result["answer"],
            "llm_called": result["llm_called"],
            "sources": wrapped["sources"],
        }
