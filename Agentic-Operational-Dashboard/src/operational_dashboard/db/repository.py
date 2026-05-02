from sqlalchemy.orm import Session

from operational_dashboard.db.models import AgentAnalysis, Incident, MetricSnapshot, TestRun


class Repository:
    def __init__(self, db: Session):
        self.db = db

    def add_metric(self, **kwargs):
        item = MetricSnapshot(**kwargs)
        self.db.add(item)
        self.db.commit()
        self.db.refresh(item)
        return item

    def list_metrics(self):
        return self.db.query(MetricSnapshot).order_by(MetricSnapshot.created_at.desc()).limit(200).all()

    def add_test_run(self, **kwargs):
        item = TestRun(**kwargs)
        self.db.add(item)
        self.db.commit()
        self.db.refresh(item)
        return item

    def list_test_runs(self):
        return self.db.query(TestRun).order_by(TestRun.created_at.desc()).limit(100).all()

    def add_incident(self, **kwargs):
        item = Incident(**kwargs)
        self.db.add(item)
        self.db.commit()
        self.db.refresh(item)
        return item

    def list_incidents(self):
        return self.db.query(Incident).order_by(Incident.created_at.desc()).limit(100).all()

    def add_analysis(self, user_prompt: str, health_score: float, readiness_score: float, summary: str):
        item = AgentAnalysis(
            user_prompt=user_prompt,
            health_score=health_score,
            readiness_score=readiness_score,
            summary=summary,
        )
        self.db.add(item)
        self.db.commit()
        self.db.refresh(item)
        return item
