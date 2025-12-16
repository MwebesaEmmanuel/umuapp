from pydantic import BaseModel, Field


class AiChatRequest(BaseModel):
    prompt: str = Field(min_length=1, max_length=8000)


class AiChatResponse(BaseModel):
    answer: str
    model: str | None = None

