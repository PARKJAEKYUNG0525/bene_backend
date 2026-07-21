from pydantic import BaseModel


class ChatAskRequest(BaseModel):
    """하이브리드 검색(BM25+Chroma) 기반 RAG 챗봇에 보내는 자유 질문."""

    query: str
    top_k: int = 3
