"""HTTP request tool."""

from typing import Any, Dict
import httpx

from .base import Tool, ToolResponse


class HTTPTool(Tool):
    """Tool for making HTTP requests."""

    @property
    def name(self) -> str:
        return "http"

    @property
    def description(self) -> str:
        return "Make HTTP requests to fetch data from URLs"

    async def run(self, params: Dict[str, Any]) -> ToolResponse:
        """Execute an HTTP request.
        
        Args:
            params:
                url: Target URL
                method: HTTP method (default: GET)
                headers: Optional request headers
                body: Optional request body
        """
        try:
            async with httpx.AsyncClient() as client:
                response = await client.request(
                    method=params.get("method", "GET"),
                    url=params["url"],
                    headers=params.get("headers"),
                    json=params.get("body")
                )
                
                return ToolResponse(
                    success=True,
                    result={
                        "status_code": response.status_code,
                        "headers": dict(response.headers),
                        "body": response.text
                    }
                )
        except Exception as e:
            return ToolResponse(
                success=False,
                error=str(e)
            )