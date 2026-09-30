# Step 1 - Run the AI DevOps Agent locally

## 1. Prerequisites
Install:
- Docker Desktop
- Git
- VS Code

Make sure Docker Desktop is running.

## 2. Open the project
Extract the ZIP and open `ai-devops-agent` in VS Code.

## 3. Create `.env`
PowerShell:
```powershell
cp .env.example .env
```

## 4. Start the containers
```powershell
docker compose up -d --build
```

Check:
```powershell
docker compose ps
```

Both `ollama` and `agent` should be running.

## 5. Download the AI model
```powershell
docker compose exec ollama ollama pull qwen2.5-coder:7b
```

This downloads the local model into the Docker volume. The first download can take some time.

## 6. Test the agent
Open:
`http://localhost:8000/health`

You should get JSON similar to:
```json
{"status":"ok","model":"qwen2.5-coder:7b"}
```

## 7. Send a sample pipeline error
```powershell
$body = Get-Content .\sample-logs\pipeline-failure.json -Raw
Invoke-RestMethod -Uri http://localhost:8000/analyze -Method Post -ContentType "application/json" -Body $body
```

The response should contain:
- summary
- root_cause
- failed_component
- error
- proposed_change
- verification
- auto_fix
- human_review
- confidence

## 8. Stop the project
```powershell
docker compose down
```

Do not delete the Docker volume if you want to keep the downloaded model:
```powershell
docker compose down
```

Next phase: connect GitHub Actions so a failed workflow can automatically send its failed-job log to this agent.
