from operational_dashboard.scoring.score_engine import OperationalScoreEngine


def test_scores_are_bounded():
    engine = OperationalScoreEngine()
    score = engine.calculate_health_score([
        {
            "error_rate_pct": 1,
            "latency_p95_ms": 300,
            "cpu_pct": 60,
            "memory_pct": 70,
            "kafka_lag": 0,
        }
    ])
    assert 0 <= score <= 100


def test_release_readiness_penalizes_incidents():
    engine = OperationalScoreEngine()
    score = engine.calculate_release_readiness(90, 90, 3)
    assert score < 90
