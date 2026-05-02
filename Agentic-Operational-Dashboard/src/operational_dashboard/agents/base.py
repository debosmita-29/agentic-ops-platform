from dataclasses import dataclass, field
from typing import Any


@dataclass
class AgentContext:
    prompt: str
    metrics: list[dict] = field(default_factory=list)
    test_runs: list[dict] = field(default_factory=list)
    incidents: list[dict] = field(default_factory=list)
    connector_signals: dict[str, Any] = field(default_factory=dict)
    scores: dict[str, float] = field(default_factory=dict)


@dataclass
class AgentResult:
    agent_name: str
    summary: str
    risks: list[str]
    recommendations: list[str]
    data: dict[str, Any] = field(default_factory=dict)
