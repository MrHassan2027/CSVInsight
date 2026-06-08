import click
import json
from rich.console import Console
from rich.table import Table
from .analyzer import analyze

console = Console()


@click.command()
@click.argument("path")
@click.option("--output", "-o", default=None, help="Save HTML report to file")
@click.option("--open", "open_browser", is_flag=True, help="Open report in browser")
@click.option("--json", "as_json", is_flag=True, help="Output raw JSON")
def main(path: str, output: str | None, open_browser: bool, as_json: bool):
    """Analyze a CSV/TSV/Excel file and generate a statistical report."""
    console.print(f"[dim]Analyzing {path}...[/dim]")
    report = analyze(path)

    if as_json:
        import dataclasses
        print(json.dumps(dataclasses.asdict(report), indent=2))
        return

    console.print(f"\n[bold]Overview[/bold]")
    console.print(f"  Rows:       {report.rows:,}")
    console.print(f"  Columns:    {report.columns}")
    console.print(f"  Duplicates: {report.duplicate_rows:,}")
    console.print(f"  Memory:     {report.memory_mb} MB\n")

    t = Table(title="Column Profiles", show_lines=True)
    t.add_column("Column", style="cyan")
    t.add_column("Type")
    t.add_column("Nulls %", justify="right")
    t.add_column("Unique", justify="right")
    t.add_column("Mean", justify="right")
    t.add_column("Std", justify="right")
    t.add_column("Outliers", justify="right", style="yellow")

    for p in report.profiles:
        t.add_row(
            p.name,
            p.dtype,
            f"{p.null_pct}%",
            str(p.unique_count),
            str(p.mean) if p.mean is not None else "—",
            str(p.std)  if p.std  is not None else "—",
            str(p.outlier_count) if p.outlier_count else "—",
        )
    console.print(t)

    if output:
        from .report import render_html
        html = render_html(report)
        with open(output, "w") as f:
            f.write(html)
        console.print(f"\n[green]Report saved to {output}[/green]")
        if open_browser:
            import webbrowser
            webbrowser.open(output)


if __name__ == "__main__":
    main()
