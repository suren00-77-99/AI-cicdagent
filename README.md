# AI DevOps Agent

Phase 1: analyze CI/CD logs locally with a local Ollama model.

## Stack
- Python + FastAPI
- Ollama
- qwen2.5-coder:7b
- Docker Compose
- Pytest

## Quick start (Windows)
1. Install Docker Desktop and make sure it is running.
2. Open PowerShell in this folder.
3. Copy `.env.example` to `.env`.
4. Run:
   docker compose up -d
   docker compose exec ollama ollama pull qwen2.5-coder:7b
5. Check:
   http://localhost:8000/health
6. Analyze the sample:
   curl.exe -X POST http://localhost:8000/analyze -H "Content-Type: application/json" --data-binary "@sample-logs/pipeline-failure.json"

The next phases will connect this agent to GitHub Actions and then add repository context, historical failures, and PR generation.
