"""Base interface for agent tools."""

from abc import ABC, abstractmethod
from typing import Any, Dict
from pydantic import BaseModel


class ToolResponse(BaseModel):
    """Response from a tool execution."""
    success: bool
    result: Any
    error: str | None = None


class Tool(ABC):
    """Abstract base class for agent tools."""

    @property
    @abstractmethod
    def name(self) -> str:
        """Get the tool's name."""
        pass

    @property
    @abstractmethod
    def description(self) -> str:
        """Get the tool's description."""
        pass

    @abstractmethod
    async def run(self, params: Dict[str, Any]) -> ToolResponse:
        """Execute the tool with the given parameters.
        
        Args:
            params: Tool-specific parameters
            
        Returns:
            Response containing success status and result/error
        """
        pass