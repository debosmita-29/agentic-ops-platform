from operational_dashboard.db.repository import Repository


class SplunkMockConnector:
    def fetch_error_signal(self):
        return {
            "source": "splunk",
            "top_errors": [
                "TimeoutException in payment-service",
                "Kafka consumer lag in notification-service",
                "NullPointerException in account-service",
            ],
        }


class DynatraceMockConnector:
    def fetch_health_signal(self, repository: Repository):
        metrics = repository.list_metrics()
        return {
            "source": "dynatrace",
            "services": [
                {
                    "service_name": m.service_name,
                    "availability": m.availability,
                    "latency_p95_ms": m.latency_p95_ms,
                    "error_rate_pct": m.error_rate_pct,
                    "cpu_pct": m.cpu_pct,
                    "memory_pct": m.memory_pct,
                    "kafka_lag": m.kafka_lag,
                }
                for m in metrics
            ],
        }


class JenkinsMockConnector:
    def fetch_pipeline_signal(self, repository: Repository):
        runs = repository.list_test_runs()
        return {
            "source": "jenkins",
            "pipelines": [
                {
                    "pipeline_name": r.pipeline_name,
                    "total_tests": r.total_tests,
                    "passed_tests": r.passed_tests,
                    "failed_tests": r.failed_tests,
                    "flaky_tests": r.flaky_tests,
                    "duration_minutes": r.duration_minutes,
                }
                for r in runs
            ],
        }
