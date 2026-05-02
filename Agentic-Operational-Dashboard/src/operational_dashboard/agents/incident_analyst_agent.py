from operational_dashboard.agents.base import AgentContext, AgentResult


class IncidentAnalystAgent:
    name = "incident_analyst"
    skill_file = "skills/incident_analyst.skill.md"

    async def run(self, context: AgentContext) -> AgentResult:
        high_risk = [
            i for i in context.incidents
            if i["severity"].lower() in {"sev1", "sev2", "high"}
        ]

        risks = [f"{i['severity']}: {i['title']} on {i['service_name']}" for i in high_risk]
        recommendations = [
            "Validate whether current errors correlate with recent deployments.",
            "Prioritize high-severity incidents before release approval.",
            "Create follow-up tasks for services with repeated incident patterns.",
        ]

        return AgentResult(
            self.name,
            f"Found {len(context.incidents)} incidents and {len(high_risk)} high-risk incident(s).",
            risks,
            recommendations,
            {"high_risk_count": len(high_risk)},
        )
