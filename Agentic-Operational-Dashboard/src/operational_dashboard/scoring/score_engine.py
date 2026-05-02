class OperationalScoreEngine:
    def calculate_health_score(self, metrics: list[dict]) -> float:
        if not metrics:
            return 0.0

        scores = []
        for metric in metrics:
            score = 100.0
            score -= max(metric["error_rate_pct"] * 8, 0)
            score -= max((metric["latency_p95_ms"] - 300) / 20, 0)
            score -= max((metric["cpu_pct"] - 75) * 0.8, 0)
            score -= max((metric["memory_pct"] - 80) * 0.8, 0)
            score -= max(metric["kafka_lag"] / 1000, 0)
            score = max(min(score, 100), 0)
            scores.append(score)

        return round(sum(scores) / len(scores), 2)

    def calculate_test_stability_score(self, test_runs: list[dict]) -> float:
        if not test_runs:
            return 0.0

        scores = []
        for run in test_runs:
            pass_rate = run["passed_tests"] / max(run["total_tests"], 1)
            flaky_penalty = run["flaky_tests"] / max(run["total_tests"], 1)
            score = (pass_rate * 100) - (flaky_penalty * 50)
            scores.append(max(min(score, 100), 0))

        return round(sum(scores) / len(scores), 2)

    def calculate_release_readiness(self, health_score: float, test_score: float, open_incidents: int) -> float:
        score = (health_score * 0.5) + (test_score * 0.4) - (open_incidents * 5)
        return round(max(min(score, 100), 0), 2)
