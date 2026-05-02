import json

from operational_dashboard.agents.base import AgentContext
from operational_dashboard.agents.capacity_cost_agent import CapacityCostAgent
from operational_dashboard.agents.executive_summary_agent import ExecutiveSummaryAgent
from operational_dashboard.agents.incident_analyst_agent import IncidentAnalystAgent
from operational_dashboard.agents.release_readiness_agent import ReleaseReadinessAgent
from operational_dashboard.agents.test_stability_agent import TestStabilityAgent
from operational_dashboard.connectors.mock_connectors import (
    DynatraceMockConnector,
    JenkinsMockConnector,
    SplunkMockConnector,
)
from operational_dashboard.llm.client import LLMClient
from operational_dashboard.scoring.score_engine import OperationalScoreEngine


class OperationalOrchestrator:
    def __init__(self, repository):
        self.repository = repository
        self.llm = LLMClient()
        self.score_engine = OperationalScoreEngine()
        self.agents = [
            IncidentAnalystAgent(),
            TestStabilityAgent(),
            ReleaseReadinessAgent(),
            CapacityCostAgent(),
            ExecutiveSummaryAgent(),
        ]

    async def analyze(self, prompt: str) -> dict:
        metrics = [
            {
                "service_name": m.service_name,
                "availability": m.availability,
                "latency_p95_ms": m.latency_p95_ms,
                "error_rate_pct": m.error_rate_pct,
                "cpu_pct": m.cpu_pct,
                "memory_pct": m.memory_pct,
                "kafka_lag": m.kafka_lag,
            }
            for m in self.repository.list_metrics()
        ]

        test_runs = [
            {
                "pipeline_name": t.pipeline_name,
                "total_tests": t.total_tests,
                "passed_tests": t.passed_tests,
                "failed_tests": t.failed_tests,
                "flaky_tests": t.flaky_tests,
                "duration_minutes": t.duration_minutes,
            }
            for t in self.repository.list_test_runs()
        ]

        incidents = [
            {
                "service_name": i.service_name,
                "severity": i.severity,
                "title": i.title,
                "description": i.description,
                "status": i.status,
            }
            for i in self.repository.list_incidents()
        ]

        connector_signals = {
            "splunk": SplunkMockConnector().fetch_error_signal(),
            "dynatrace": DynatraceMockConnector().fetch_health_signal(self.repository),
            "jenkins": JenkinsMockConnector().fetch_pipeline_signal(self.repository),
        }

        health_score = self.score_engine.calculate_health_score(metrics)
        test_score = self.score_engine.calculate_test_stability_score(test_runs)
        open_incidents = len([i for i in incidents if i["status"] == "open"])
        readiness_score = self.score_engine.calculate_release_readiness(
            health_score, test_score, open_incidents
        )

        scores = {
            "health_score": health_score,
            "test_stability_score": test_score,
            "release_readiness_score": readiness_score,
        }

        context = AgentContext(
            prompt=prompt,
            metrics=metrics,
            test_runs=test_runs,
            incidents=incidents,
            connector_signals=connector_signals,
            scores=scores,
        )

        agent_results = []
        for agent in self.agents:
            result = await agent.run(context)
            agent_results.append(result)

        final_summary = await self.llm.complete(
            system_prompt=(
                "You are an operational intelligence assistant for engineering leaders. "
                "Create a concise executive summary with risks, likely causes, and next actions."
            ),
            user_prompt=json.dumps(
                {
                    "prompt": prompt,
                    "scores": scores,
                    "agent_results": [r.__dict__ for r in agent_results],
                    "connector_signals": connector_signals,
                },
                indent=2,
            ),
        )

        analysis = self.repository.add_analysis(prompt, health_score, readiness_score, final_summary)

        return {
            "analysis_id": analysis.id,
            "scores": scores,
            "summary": final_summary,
            "agent_results": [r.__dict__ for r in agent_results],
            "metrics": metrics,
            "test_runs": test_runs,
            "incidents": incidents,
        }
