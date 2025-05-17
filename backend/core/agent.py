from __future__ import annotations

import asyncio
from typing import AsyncIterator

from pydantic import BaseModel, Field


class AgentRunConfig(BaseModel):
    """Configuration payload for running an agent."""

    prompt: str = Field(..., description="Initial prompt or task description for the agent.")
    max_steps: int = Field(5, description="How many reasoning steps the agent may take.")


class Agent:
    """Very small proof-of-concept agent.

    In later versions this will orchestrate an LLM, tools, and memory back-ends.
    For now it simply echoes the prompt a few times so that the API / UI can
    stream tokens end-to-end.
    """

    def __init__(self, config: AgentRunConfig) -> None:
        self._config = config

    async def run(self) -> AsyncIterator[str]:
        """Async generator that streams chunks of text back to the caller."""

        for step in range(self._config.max_steps):
            # Simulate latency as if calling an LLM
            await asyncio.sleep(0.2)
            yield f"step {step + 1}: {self._config.prompt}\n" 