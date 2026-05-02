from operational_dashboard.agents.base import AgentContext, AgentResult


class ExecutiveSummaryAgent:
    name = "executive_summary"
    skill_file = "skills/executive_summary.skill.md"

    async def run(self, context: AgentContext) -> AgentResult:
        readiness = context.scores.get("release_readiness_score", 0)
        health = context.scores.get("health_score", 0)
        test = context.scores.get("test_stability_score", 0)

        summary = (
            f"Operational health is {health}, test stability is {test}, "
            f"and release readiness is {readiness}."
        )

        return AgentResult(
            self.name,
            summary,
            [],
            [
                "Share leadership update with risk score and mitigation plan.",
                "Align engineering, QA, and SRE on top three blockers.",
                "Reassess readiness after incidents and flaky tests are resolved.",
            ],
            {"executive_summary": summary},
        )
