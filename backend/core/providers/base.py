"""Base interfaces for LLM providers."""

from __future__ import annotations
from enum import Enum
from typing import AsyncIterator
from pydantic import BaseModel


class Role(str, Enum):
    """Message role in a conversation."""
    SYSTEM = "system"
    USER = "user"
    ASSISTANT = "assistant"


class Message(BaseModel):
    """A message in the conversation."""
    role: Role
    content: str


class LLMProvider:
    """Abstract base class for LLM providers."""

    async def stream_chat(self, messages: list[Message]) -> AsyncIterator[str]:
        """Stream a chat completion response.
        
        Args:
            messages: List of messages in the conversation
            
        Yields:
            Text chunks from the LLM response
        """
        raise NotImplementedError