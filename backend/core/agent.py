from __future__ import annotations

from typing import AsyncIterator, Dict, List
import os

from pydantic import BaseModel, Field

from .providers import (
    LLMProvider,
    Message,
    Role,
    OpenAIProvider,
    AnthropicProvider
)
from .tools import Tool, HTTPTool, SlackTool


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
        self._tools = self._initialize_tools()

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

        messages = [
            Message(
                role=Role.SYSTEM,
                content=f"""You are a helpful AI assistant with access to the following tools:

{tool_descriptions}

When you need to use a tool, format your response as:
USE_TOOL: <tool_name>
<tool parameters as JSON>
END_TOOL

Respond directly and concisely."""
            ),
            Message(
                role=Role.USER,
                content=self._config.prompt
            )
        ]

        async for chunk in self._provider.stream_chat(messages):
            yield chunk