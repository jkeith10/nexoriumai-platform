"""OpenAI provider implementation."""

from __future__ import annotations
import os
from typing import AsyncIterator

from openai import AsyncOpenAI

from .base import LLMProvider, Message, Role


class OpenAIProvider(LLMProvider):
    """OpenAI chat completion provider."""
    
    def __init__(self, model: str = "gpt-4-turbo-preview") -> None:
        """Initialize the provider.
        
        Args:
            model: OpenAI model to use
        """
        self.client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.model = model

    async def stream_chat(self, messages: list[Message]) -> AsyncIterator[str]:
        """Stream a chat completion response."""
        openai_messages = [
            {"role": msg.role.value, "content": msg.content}
            for msg in messages
        ]
        
        response = await self.client.chat.completions.create(
            model=self.model,
            messages=openai_messages,
            stream=True
        )
        
        async for chunk in response:
            if chunk.choices[0].delta.content:
                yield chunk.choices[0].delta.content