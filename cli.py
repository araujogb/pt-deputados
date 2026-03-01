import typer
import asyncio
from scraper import main as run_scraper

app = typer.Typer(
    name="deputados",
    help="Portuguese Deputies Scraper",
    invoke_without_command=True
)

@app.callback(invoke_without_command=True)
def main(ctx: typer.Context):
    """Portuguese Deputies Scraper"""
    if ctx.invoked_subcommand is None:
        typer.echo("Use 'deputados fetch' to start scraping")
        raise typer.Exit()

@app.command()
def fetch():
    """Download list + all biographies and save Parquet/JSONL"""
    typer.echo("🚀 Starting full scrape...")
    asyncio.run(run_scraper())

if __name__ == "__main__":
    app()
