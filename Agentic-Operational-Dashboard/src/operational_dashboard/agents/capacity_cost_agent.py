from operational_dashboard.agents.base import AgentContext, AgentResult


class CapacityCostAgent:
    name = "capacity_cost"
    skill_file = "skills/capacity_cost.skill.md"

    async def run(self, context: AgentContext) -> AgentResult:
        risks = []
        for metric in context.metrics:
            if metric["cpu_pct"] > 85:
                risks.append(f"{metric['service_name']} CPU is high at {metric['cpu_pct']}%.")
            if metric["memory_pct"] > 88:
                risks.append(f"{metric['service_name']} memory is high at {metric['memory_pct']}%.")
            if metric["kafka_lag"] > 5000:
                risks.append(f"{metric['service_name']} Kafka lag is high at {metric['kafka_lag']}.")

        return AgentResult(
            self.name,
            "Reviewed capacity and cost-related operational signals.",
            risks,
            [
                "Scale services with sustained high CPU or memory.",
                "Investigate Kafka consumer lag before peak traffic.",
                "Add capacity guardrails to release readiness criteria.",
            ],
            {},
        )
