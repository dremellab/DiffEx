import typer
from diffex.core import run_quarto_report

app = typer.Typer()

@app.command()
def render(
    qmd: str = typer.Option("DiffEx.qmd", help="Path to the Quarto .qmd file"),
    params: str = typer.Option("params.yaml", help="Path to the parameters YAML")
):
    """Run differential expression report rendering via Quarto."""
    run_quarto_report(qmd_path=qmd, params_file=params)

def main():
    app()

if __name__ == "__main__":
    main()
