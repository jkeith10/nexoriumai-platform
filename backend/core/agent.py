from __future__ import annotations

from datetime import datetime
from typing import AsyncIterator, Dict, List
import os
import uuid

from pydantic import BaseModel, Field

from .providers import (
    LLMProvider,
    Message,
    Role,
    OpenAIProvider,
    AnthropicProvider
)
from .tools import Tool, HTTPTool, SlackTool
from .memory import MemoryManager


class AgentRunConfig(BaseModel):
    """Configuration payload for running an agent."""

    prompt: str = Field(..., description="Initial prompt or task description for the agent.")
    max_steps: int = Field(5, description="How many reasoning steps the agent may take.")
    provider: str = Field("openai", description="LLM provider to use (openai or anthropic)")


class Agent:
    """Agent that leverages LLMs to accomplish tasks."""
    
    def __init__(self, config: AgentRunConfig) -> None:
        self._config = config
        self._provider = self._get_provider()
        self._tools = self._initialize_tools()
        self._id = str(uuid.uuid4())
        self._memory = MemoryManager(self._id)

    def _get_provider(self) -> LLMProvider:
        """Get the configured LLM provider."""
        if self._config.provider == "anthropic":
            return AnthropicProvider()
        return OpenAIProvider()

    def _initialize_tools(self) -> Dict[str, Tool]:
        """Initialize available tools."""
        tools: List[Tool] = [
            HTTPTool(),
            SlackTool()
        ]
        return {tool.name: tool for tool in tools}

    async def run(self) -> AsyncIterator[str]:
        """Run the agent and stream responses."""
        tool_descriptions = "\n".join(
            f"- {tool.name}: {tool.description}"
            for tool in self._tools.values()
        )

        # Get recent context from memory
        recent_memories = self._memory.get_recent_memories(limit=5)
        memory_context = "\n".join(
            f"{mem.role}: {mem.content}"
            for mem in recent_memories
        )

        system_prompt = f"""You are a helpful AI assistant with access to the following tools:

{tool_descriptions}

Recent conversation context:
{memory_context}

When you need to use a tool, format your response as:
USE_TOOL: <tool_name>
<tool parameters as JSON>
END_TOOL

Respond directly and concisely."""

        messages = [
            Message(
                role=Role.SYSTEM,
                content=system_prompt
            ),
            Message(
                role=Role.USER,
                content=self._config.prompt
            )
        ]

        # Store the user's prompt in memory
        self._memory.add_entry(self._config.prompt, "user")

        response_chunks = []
        async for chunk in self._provider.stream_chat(messages):
            response_chunks.append(chunk)
            yield chunk

        # Store the complete response in memory
        self._memory.add_entry("".join(response_chunks), "assistant")