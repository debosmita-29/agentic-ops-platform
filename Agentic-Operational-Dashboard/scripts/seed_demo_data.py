from pathlib import Path

from operational_dashboard.db.base import Base, SessionLocal, engine
from operational_dashboard.db.repository import Repository

Path("data").mkdir(exist_ok=True)
Base.metadata.create_all(bind=engine)

db = SessionLocal()
try:
    repo = Repository(db)

    if not repo.list_metrics():
        repo.add_metric(
            service_name="payment-service",
            environment="prod",
            availability=99.82,
            latency_p95_ms=420,
            error_rate_pct=1.8,
            cpu_pct=82,
            memory_pct=76,
            kafka_lag=1200,
        )
        repo.add_metric(
            service_name="account-service",
            environment="prod",
            availability=99.95,
            latency_p95_ms=280,
            error_rate_pct=0.4,
            cpu_pct=63,
            memory_pct=71,
            kafka_lag=200,
        )
        repo.add_metric(
            service_name="notification-service",
            environment="prod",
            availability=99.70,
            latency_p95_ms=610,
            error_rate_pct=2.4,
            cpu_pct=88,
            memory_pct=91,
            kafka_lag=7200,
        )

    if not repo.list_test_runs():
        repo.add_test_run(
            pipeline_name="nightly-regression",
            total_tests=420,
            passed_tests=392,
            failed_tests=18,
            flaky_tests=10,
            duration_minutes=74,
        )
        repo.add_test_run(
            pipeline_name="pr-smoke-suite",
            total_tests=95,
            passed_tests=91,
            failed_tests=2,
            flaky_tests=2,
            duration_minutes=18,
        )

    if not repo.list_incidents():
        repo.add_incident(
            service_name="notification-service",
            severity="SEV2",
            title="Elevated Kafka lag causing delayed notifications",
            description="Kafka consumer lag increased during peak load.",
            status="open",
        )
        repo.add_incident(
            service_name="payment-service",
            severity="HIGH",
            title="Intermittent payment timeout spike",
            description="Timeout errors correlate with latency increase.",
            status="open",
        )
finally:
    db.close()

print("Demo data seeded.")
