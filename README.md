# WhatsApp & Gmail Communication Analyzer

Analyzes WhatsApp chat exports and Gmail threads. Uploads WhatsApp analysis to Google Sheets and lists Gmail threads (e.g. threads you started without a reply, or where you were the last to reply). Uses Google APIs for Sheets and Gmail.

## What you need

- Python 3.9+
- Google API credentials (service account for Sheets; OAuth or service account for Gmail)
- A WhatsApp chat export file (text format)
- Optional: Docker

## How to use

### 1. Configure environment

Copy `env.production.example` to `.env` for production or Docker. For local development you can use `env.example` and adjust paths. Edit `.env` and set:

- `CLIENT_SECRETS_PATH` — path to your Google service account JSON (for Sheets)
- `AUTH_CLIENT_SECRET_PATH` — path to OAuth client secret JSON (for Gmail)
- `WHATSAPP_FILE_PATH` — path to your WhatsApp chat export file
- `TOKEN_PATH` — path where Gmail token will be stored (e.g. `./credentials/token.pickle`)

Place your Google API credential files in `./credentials/` (or the paths you set in `.env`).

### 2. Run with Docker

```bash
docker-compose up --build
```

To use the helper script:

```bash
./scripts/docker-run.sh
```

### 3. Run locally

```bash
pip install -r requirements.txt
python main.py
```

The app will read the WhatsApp file, run the analysis, upload results to a new Google Sheet, then authenticate with Gmail and print thread summaries. On failure it exits with code 1.

### 4. Environment files

- **env.example** — development/local example (paths and placeholders).
- **env.production.example** — production/Docker example; copy to `.env` and fill in credentials and paths.

## Project layout

- `main.py` — entry point; loads `.env` and calls the main workflow.
- `src/core/main.py` — orchestrates WhatsApp and Gmail analysis.
- `src/services/` — WhatsApp analysis, Google Sheets upload, Gmail analysis.
- `src/config/` — configuration and paths.
- `src/utils/` — file reading and helpers.
- `scripts/` — `docker-run.sh`, `deploy.sh`, and other run/deploy scripts.
- `credentials/` — put Google API credential files here (not committed).
- `archive/` — legacy Colab prototype kept for reference.

## Docker

- Build: `docker-compose build`
- Run: `docker-compose up` (or `docker-compose up -d`)
- Logs: `docker-compose logs`
- Shell: `docker-compose exec communication-analyzer bash`

See `docs/DEPLOYMENT.md` for deployment options (Heroku, Railway, Cloud Run, etc.).
