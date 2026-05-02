# AGENTS.md

This dashboard uses a specialist-agent model for operational intelligence.

## Agent Inventory

| Agent | Purpose |
|---|---|
| IncidentAnalystAgent | Detects incident patterns and root-cause hypotheses |
| TestStabilityAgent | Analyzes flaky tests, regression health, and failure clusters |
| ReleaseReadinessAgent | Scores release readiness from quality and operational signals |
| CapacityCostAgent | Reviews CPU, memory, storage, Kafka lag, and cost signals |
| ExecutiveSummaryAgent | Converts technical signals into leadership-ready updates |

## Agent Principles

1. Use evidence from metrics before generating recommendations.
2. Clearly separate facts, assumptions, and hypotheses.
3. Prefer concise operational actions.
4. Escalate high-risk signals.
5. Generate executive summaries without hiding technical risks.

## Production Extensions

- Replace mock connectors with Splunk, Dynatrace, Jenkins, GitHub Actions, ServiceNow, Jira, Rally, or PagerDuty connectors.
- Store historical time series in Postgres/TimescaleDB.
- Add RBAC and audit trails.
- Add model evaluation and hallucination checks.
