from operational_dashboard.agents.base import AgentContext, AgentResult


class TestStabilityAgent:
    name = "test_stability"
    skill_file = "skills/test_stability.skill.md"

    async def run(self, context: AgentContext) -> AgentResult:
        flaky_total = sum(r["flaky_tests"] for r in context.test_runs)
        failed_total = sum(r["failed_tests"] for r in context.test_runs)

        risks = []
        if flaky_total > 0:
            risks.append(f"{flaky_total} flaky tests detected across recent pipelines.")
        if failed_total > 0:
            risks.append(f"{failed_total} failed tests detected across recent pipelines.")

        return AgentResult(
            self.name,
            f"Test stability score is {context.scores.get('test_stability_score', 0)}.",
            risks,
            [
                "Quarantine repeat flaky tests and open defect tickets.",
                "Prioritize failures linked to critical user journeys.",
                "Block release if critical regression failures remain unresolved.",
            ],
            {"flaky_total": flaky_total, "failed_total": failed_total},
        )
