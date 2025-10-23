# secret-mission : Simple AI Agent with RAG feature

### Overview

This repo contains a minimal Bot reply by finding knowledge in vector store:

1. Scrapes ≥30 support articles from **support.optisigns.com**
2. Converts them into clean Markdown (slug-based filenames)
3. Uploads + chunks them into an OpenAI **Vector Store** via API
4. Deploys a **daily DigitalOcean Scheduled Job** to re-scrape and upload only deltas
   (new/updated articles detected via hash comparison)
5. Assistant answers only from uploaded docs with citations

---

### Local Setup

```bash
cp .env.sample .env
# fill in OPENAI_API_KEY
```

---

### Run Locally (one-shot)

```bash
docker build -t optibot-mini .
docker run --rm -e OPENAI_API_KEY=$OPENAI_API_KEY optibot-mini:latest python main.py
```

This triggers:

- scrape
- clean markdown
- create assistant
- upload file to vector store
- link assistant to vector store

---

### Daily Job (DigitalOcean)

Not finish yet

---

### Assistant

The Assistant is created in the Playground:

📷 Screenshot proof:

<img src="picture/cite-answer-form-playground.png" alt='video-call-p2p' width="70%" height="70%"/>

---

### Repo Structure

```
/app/                       # application core
  ├── __init__.py
  ├── logger.py             # unified log formatting
  ├── scraper.py            # Zendesk API fetch, fetch aricles
  ├── tools.py              # slugify, loadfile, save file
  └── upload_article.py     # init openai client, create assistant, vector_store and upload file
/articles/                  # cleaned Markdown output (stored as <slug>.md)
/picture/                   # evident picture
main.py                     # entrypoint: scrape + detect delta + upload vector store
Dockerfile                  # container for daily job
.env.sample                 # env variables placeholder (no real keys)
requirements.txt.           # install requirement lib
optibot.json                # save exist bot and vector_store to upload

```

## Example file

optibot.json

```json
{
  "assistant_id": "asst_xSG...",
  "vector_store_id": "vs_68..."
}
```

.env

```
DOMAIN_TARGET=https://support.optisigns.com/
OPENAI_API_KEY=sk-pr...
```

---

### Notes / Limitations

- Dont have check metadata for updated file and upload only delta file
