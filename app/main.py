import json
import os
from pathlib import Path
import httpx
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

load_dotenv()

app = FastAPI(title="AI DevOps Agent", version="0.1.0")
OLLAMA_URL = os.getenv("OLLAMA_URL", "http://ollama:11434")
AI_MODEL = os.getenv("AI_MODEL", "qwen2.5-coder:7b")
AI_TEMPERATURE = float(os.getenv("AI_TEMPERATURE", "0.1"))

SYSTEM_PROMPT = """You are an AI DevOps incident analyst.
Analyze CI/CD logs carefully. Do not invent facts.
Return JSON with exactly these keys:
summary, root_cause, failed_component, error, proposed_change, verification, auto_fix, human_review, confidence.
verification must be an array of concrete checks.
auto_fix must be false unless the evidence clearly supports a safe automated change.
confidence must be a number from 0 to 100.
"""

class AnalyzeRequest(BaseModel):
    repository: str = "unknown"
    workflow: str = "unknown"
    branch: str = "unknown"
    commit: str = "unknown"
    log: str

async def call_ollama(prompt: str):
    payload = {
        "model": AI_MODEL,
        "system": SYSTEM_PROMPT,
        "prompt": prompt,
        "stream": False,
        "format": "json",
        "options": {"temperature": AI_TEMPERATURE},
    }
    async with httpx.AsyncClient(timeout=180) as client:
        response = await client.post(f"{OLLAMA_URL}/api/generate", json=payload)
        response.raise_for_status()
        data = response.json()
        return json.loads(data["response"])

@app.get("/health")
async def health():
    try:
        async with httpx.AsyncClient(timeout=5) as client:
            r = await client.get(f"{OLLAMA_URL}/api/tags")
            r.raise_for_status()
        return {"status": "ok", "model": AI_MODEL}
    except Exception as exc:
        raise HTTPException(status_code=503, detail=f"Ollama unavailable: {exc}")

@app.post("/analyze")
async def analyze(request: AnalyzeRequest):
    prompt = f"""Repository: {request.repository}
Workflow: {request.workflow}
Branch: {request.branch}
Commit: {request.commit}

CI/CD LOG:
---BEGIN LOG---
{request.log}
---END LOG---

Identify the most likely root cause using only evidence in the log. Mention exact error text, relevant component, likely correction, and verification steps."""
    try:
        result = await call_ollama(prompt)
        return {
            "metadata": request.model_dump(exclude={"log"}),
            "analysis": result,
        }
    except Exception as exc:
        raise HTTPException(status_code=502, detail=f"AI analysis failed: {exc}")
