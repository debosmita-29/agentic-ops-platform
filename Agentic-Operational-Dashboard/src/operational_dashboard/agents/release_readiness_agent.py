from operational_dashboard.agents.base import AgentContext, AgentResult


class ReleaseReadinessAgent:
    name = "release_readiness"
    skill_file = "skills/release_readiness.skill.md"

    async def run(self, context: AgentContext) -> AgentResult:
        readiness = context.scores.get("release_readiness_score", 0)
        risks = []

        if readiness < 70:
            risks.append("Release readiness is below recommended threshold.")
        if context.scores.get("health_score", 0) < 80:
            risks.append("Operational health score indicates elevated production risk.")
        if context.scores.get("test_stability_score", 0) < 85:
            risks.append("Test stability does not support a confident release decision.")

        return AgentResult(
            self.name,
            f"Release readiness score is {readiness}.",
            risks,
            [
                "Review open Sev1/Sev2 incidents.",
                "Confirm regression stability before release.",
                "Validate top service health metrics for release-critical services.",
            ],
            {"readiness_score": readiness},
        )
