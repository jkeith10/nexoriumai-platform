# Nexorium AI

Autonomous agent platform powered by OpenAI & Claude.

## Quick-start (local)

1. Install [Docker Desktop](https://www.docker.com/).
2. From the repo root, run:

```bash
docker compose up --build
```

The backend will be live at http://localhost:8000. Kick off a run:

```bash
curl -X POST \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Write a haiku about lightning", "max_steps": 3}' \
  http://localhost:8000/agents/run
```

## Project Layout

```
backend/        # FastAPI application and core agent runtime
  core/         # Agents, tools, memory, providers (WIP)
  api/          # HTTP routes
frontend/       # Next.js UI (coming soon)
```

---

Licensed under Apache-2.0. 