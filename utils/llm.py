import re
from openai import OpenAI
from config.settings import settings

client = OpenAI(base_url=settings.LMSTUDIO_BASE_URL, api_key=settings.LMSTUDIO_API_KEY)


class LocalChatModel:
    """Chat model served by LM Studio, returning responses as plain dicts."""

    def __init__(self, model_id: str = settings.LLM_MODEL, params: dict = None):
        self.model_id = model_id
        self.params = params or {}

    def chat(self, messages: list) -> dict:
        response = client.chat.completions.create(
            model=self.model_id,
            messages=messages,
            **self.params,
        ).model_dump()

        # Reasoning models put their chain of thought in <think> tags; keep only the answer
        for choice in response["choices"]:
            content = choice["message"].get("content") or ""
            choice["message"]["content"] = re.sub(r"<think>.*?</think>", "", content, flags=re.DOTALL)
        return response
