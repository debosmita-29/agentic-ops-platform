from fastapi import Depends, FastAPI
from sqlalchemy.orm import Session

from operational_dashboard.api.schemas import AnalyzeRequest
from operational_dashboard.config import settings
from operational_dashboard.db.base import Base, engine, get_db
from operational_dashboard.db.repository import Repository
from operational_dashboard.orchestration.engine import OperationalOrchestrator

Base.metadata.create_all(bind=engine)

app = FastAPI(title=settings.app_name, version="1.0.0")


@app.get("/health")
def health():
    return {"status": "ok", "app": settings.app_name, "env": settings.env}


@app.post("/analyze")
async def analyze(request: AnalyzeRequest, db: Session = Depends(get_db)):
    return await OperationalOrchestrator(Repository(db)).analyze(request.prompt)


@app.get("/metrics")
def list_metrics(db: Session = Depends(get_db)):
    return [
        {
            "id": m.id,
            "service_name": m.service_name,
            "environment": m.environment,
            "availability": m.availability,
            "latency_p95_ms": m.latency_p95_ms,
            "error_rate_pct": m.error_rate_pct,
            "cpu_pct": m.cpu_pct,
            "memory_pct": m.memory_pct,
            "kafka_lag": m.kafka_lag,
            "created_at": m.created_at.isoformat(),
        }
        for m in Repository(db).list_metrics()
    ]


@app.get("/test-runs")
def list_test_runs(db: Session = Depends(get_db)):
    return [
        {
            "id": t.id,
            "pipeline_name": t.pipeline_name,
            "total_tests": t.total_tests,
            "passed_tests": t.passed_tests,
            "failed_tests": t.failed_tests,
            "flaky_tests": t.flaky_tests,
            "duration_minutes": t.duration_minutes,
            "created_at": t.created_at.isoformat(),
        }
        for t in Repository(db).list_test_runs()
    ]


@app.get("/incidents")
def list_incidents(db: Session = Depends(get_db)):
    return [
        {
            "id": i.id,
            "service_name": i.service_name,
            "severity": i.severity,
            "title": i.title,
            "description": i.description,
            "status": i.status,
            "created_at": i.created_at.isoformat(),
        }
        for i in Repository(db).list_incidents()
    ]
