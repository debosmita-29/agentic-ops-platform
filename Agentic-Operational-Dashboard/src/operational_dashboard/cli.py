import asyncio

import typer
from rich import print

from operational_dashboard.db.base import Base, SessionLocal, engine
from operational_dashboard.db.repository import Repository
from operational_dashboard.orchestration.engine import OperationalOrchestrator

app = typer.Typer(help="Agentic Operational Dashboard CLI")


@app.command()
def analyze(prompt: str):
    Base.metadata.create_all(bind=engine)

    async def _run():
        db = SessionLocal()
        try:
            result = await OperationalOrchestrator(Repository(db)).analyze(prompt)
            print("[bold green]Scores[/bold green]", result["scores"])
            print("[bold blue]Summary[/bold blue]", result["summary"])
        finally:
            db.close()

    asyncio.run(_run())


if __name__ == "__main__":
    app()
