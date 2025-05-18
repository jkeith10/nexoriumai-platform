from __future__ import annotations

from typing import AsyncIterator
import os

from pydantic import BaseModel, Field

from .providers import (
    LLMProvider,
    Message,
    Role,
    OpenAIProvider,
    AnthropicProvider
)


class AgentRunConfig(BaseModel):
    """Configuration payload for running an agent."""

    prompt: str = Field(..., description="Initial prompt or task description for the agent.")
    max_steps: int = Field(5, description="How many reasoning steps the agent may take.")
    provider: str = Field("openai", description="LLM provider to use (openai or anthropic)")


class Agent:
    """Agent that leverages LLMs to accomplish tasks.
    
    Supports both OpenAI and Anthropic (Claude) as providers.
    """

    def __init__(self, config: AgentRunConfig) -> None:
        self._config = config
        self._provider = self._get_provider()

    def _get_provider(self) -> LLMProvider:
        """Get the configured LLM provider."""
        if self._config.provider == "anthropic":
            return AnthropicProvider()
        return OpenAIProvider()

    async def run(self) -> AsyncIterator[str]:
        """Run the agent and stream responses."""
        messages = [
            Message(
                role=Role.SYSTEM,
                content="You are a helpful AI assistant. Respond directly and concisely."
            ),
            Message(
                role=Role.USER,
                content=self._config.prompt
            )
        ]

        async for chunk in self._provider.stream_chat(messages):
            yield chunk