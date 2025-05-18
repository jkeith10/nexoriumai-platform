"""Anthropic (Claude) provider implementation."""

from __future__ import annotations
import os
from typing import AsyncIterator

from anthropic import AsyncAnthropic

from .base import LLMProvider, Message, Role


class AnthropicProvider(LLMProvider):
    """Anthropic (Claude) chat completion provider."""
    
    def __init__(self, model: str = "claude-3-opus-20240229") -> None:
        """Initialize the provider.
        
        Args:
            model: Anthropic model to use
        """
        self.client = AsyncAnthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
        self.model = model

    async def stream_chat(self, messages: list[Message]) -> AsyncIterator[str]:
        """Stream a chat completion response."""
        # Convert to Anthropic's format
        system_msg = next(
            (msg for msg in messages if msg.role == Role.SYSTEM),
            None
        )
        
        system = system_msg.content if system_msg else None
        
        # Filter to just user/assistant messages
        chat_messages = [
            {"role": msg.role.value, "content": msg.content}
            for msg in messages
            if msg.role != Role.SYSTEM
        ]
        
        response = await self.client.messages.create(
            model=self.model,
            messages=chat_messages,
            system=system,
            stream=True
        )
        
        async for chunk in response:
            if chunk.delta.text:
                yield chunk.delta.text