from __future__ import annotations

from fastapi import FastAPI
from fastapi.responses import StreamingResponse

from nexoriumai.backend.core.agent import Agent, AgentRunConfig

app = FastAPI(title="Nexorium AI")


@app.post("/agents/run", response_class=StreamingResponse)
async def run_agent(config: AgentRunConfig):
    """Run a new agent execution and stream the response as plain text."""

    agent = Agent(config)

    async def _event_stream():
        async for chunk in agent.run():
            yield chunk

    return StreamingResponse(_event_stream(), media_type="text/plain") 