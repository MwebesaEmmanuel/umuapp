from fastapi import APIRouter

from app.schemas.ai import AiChatRequest, AiChatResponse


router = APIRouter()


@router.post("/chat", response_model=AiChatResponse)
def chat(payload: AiChatRequest) -> AiChatResponse:
    # MVP placeholder:
    # - We will connect this to an open-source LLM (self-hosted) + UMU knowledge base (RAG).
    return AiChatResponse(
        answer="AI assistant is not configured yet. Next step is to add UMU documents (policies/FAQs) and connect a hosted model.",
        model=None,
    )

