FROM python:3.11-slim

WORKDIR /app

COPY pyproject.toml README.md ./
COPY src ./src
COPY ui ./ui
COPY scripts ./scripts
COPY skills ./skills
COPY agents_md ./agents_md
COPY AGENTS.md ./AGENTS.md

RUN pip install --no-cache-dir -e ".[dev]"
RUN mkdir -p /app/data && python scripts/seed_demo_data.py

EXPOSE 8000

CMD ["uvicorn", "operational_dashboard.api.main:app", "--host", "0.0.0.0", "--port", "8000"]
