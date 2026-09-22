# Agentic Code Review Platform

A FastAPI service that fetches GitHub Pull Requests, parses changed files, runs deterministic rules, optionally invokes specialized structured-output agents, aggregates findings, and can publish a GitHub review in dry-run or live mode.

## Quick start

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
Copy-Item .env.example .env
uvicorn app.main:app --reload
```

The API is available at `http://127.0.0.1:8000`. OpenAPI documentation is at `/docs`.

Run tests with:

```powershell
python -m pytest -q
```

## Configuration

GitHub access uses `GITHUB_TOKEN`. Webhooks require `GITHUB_WEBHOOK_SECRET`; the signature is verified before the JSON body is processed. AI agents are enabled only when `LLM_API_KEY` is configured. `LLM_BASE_URL` supports OpenAI-compatible providers.

Never commit `.env` or API keys. Start from `.env.example`.

## API flow

`POST /reviews/{owner}/{repo}/{pull_number}` fetches PR metadata and files, converts them into domain models, runs the review orchestrator, and returns a `ReviewReport` containing findings and isolated agent errors.

Publishing is opt-in:

```json
{
	"publish": true,
	"dry_run": true
}
```

Use `dry_run: false` only when GitHub credentials and the PR head commit are available. Findings without an exact changed line are retained in the API report but are not emitted as inline GitHub comments.

## Architecture

- `app/api`: HTTP and webhook adapters
- `app/clients`: GitHub and model-provider integrations
- `app/models`: validated domain contracts
- `app/parsers`: unified diff parsing
- `app/rules`: deterministic checks
- `app/agents`: context, structured model client, and specialized roles
- `app/services`: pull-request loading, orchestration, aggregation, and publishing
- `app/evaluation`: precision, recall, and F1 helpers

The normal test suite never calls GitHub or an LLM. External clients are injected or mocked in tests.

## Limitations

The current service runs reviews synchronously and does not persist review runs. Large repositories, asynchronous job execution, repository-wide retrieval, and richer evaluation datasets are natural next steps for production scaling.