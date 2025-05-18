"""Slack webhook tool."""

import os
from typing import Any, Dict
import httpx

from .base import Tool, ToolResponse


class SlackTool(Tool):
    """Tool for sending messages to Slack."""

    def __init__(self) -> None:
        """Initialize the tool."""
        self.webhook_url = os.getenv("SLACK_WEBHOOK_URL")
        if not self.webhook_url:
            raise ValueError("SLACK_WEBHOOK_URL environment variable is required")

    @property
    def name(self) -> str:
        return "slack"

    @property
    def description(self) -> str:
        return "Send messages to Slack channels"

    async def run(self, params: Dict[str, Any]) -> ToolResponse:
        """Send a message to Slack.
        
        Args:
            params:
                text: Message text
                blocks: Optional message blocks
        """
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    self.webhook_url,
                    json={
                        "text": params.get("text", ""),
                        "blocks": params.get("blocks", [])
                    }
                )
                
                if response.status_code == 200:
                    return ToolResponse(
                        success=True,
                        result="Message sent successfully"
                    )
                else:
                    return ToolResponse(
                        success=False,
                        error=f"Slack API error: {response.text}"
                    )
        except Exception as e:
            return ToolResponse(
                success=False,
                error=str(e)
            )