import typer
import yaml
import shutil
import shlex
import os
import subprocess
from pathlib import Path
from typing import Dict, Any
from inspect import Parameter, Signature
import re
import importlib.resources as pkg_resources
from typing import Optional
from importlib.resources import files as pkg_files

## Hidden functions

def _echo(cmd: list[str]) -> None:
    typer.echo(f"[cmd] {shlex.join(cmd)}")

def _ensure_exists(path: Path, what: str = "file") -> None:
    if not path.exists():
        typer.secho(f"❌ {what.capitalize()} not found: {path}", fg=typer.colors.RED)
        raise typer.Exit(code=2)

def _default_gsea_qmd() -> Path:
    """
    Resolve the packaged gsea.qmd inside the diffex package.
    Expected layout: diffex/gsea.qmd (ship this file in MANIFEST.in / pyproject)
    """
    try:
        qmd = pkg_files("diffex") / "gsea.qmd"
        return Path(str(qmd))
    except Exception:
        # Fallback relative to this file if resources aren't packaged
        return Path(__file__).resolve().parent / "gsea.qmd"

def _run_quarto_render(
    qmd_path: Path,
    outdir: Path,
    rnk: Path,
    min_gs_size: int,
    max_gs_size: int,
    pvalue_cutoff: float,
    quarto: Optional[str] = None,
    extra_args: Optional[list[str]] = None,
) -> None:
    """
    Invoke `quarto render` on the GSEA QMD, passing params via -P.
    Ensures HTML is written to the same outdir and then lets the QMD post-process.
    """
    exe = quarto or shutil.which("quarto")
    if not exe:
        typer.secho("❌ Quarto not found on PATH. Install from https://quarto.org/", fg=typer.colors.RED)
        raise typer.Exit(code=2)

    _ensure_exists(qmd_path, "gsea qmd")
    outdir.mkdir(parents=True, exist_ok=True)
    _ensure_exists(rnk, "RNK file")

    cmd = [
        exe, "render", str(qmd_path),
        "--to", "html",
        "--output-dir", str(outdir),
        # Pass parameters into the QMD:
        "-P", f"rnk={rnk}",
        "-P", f"outdir={outdir}",
        "-P", f"minGSSize={min_gs_size}",
        "-P", f"maxGSSize={max_gs_size}",
        "-P", f"pvalueCutoff={pvalue_cutoff}",
    ]
    if extra_args:
        cmd.extend(extra_args)

    _echo(cmd)
    try:
        subprocess.run(cmd, check=True)
    except subprocess.CalledProcessError as e:
        typer.secho(f"❌ Quarto render failed (exit {e.returncode})", fg=typer.colors.RED)
        raise typer.Exit(code=e.returncode)

app = typer.Typer()

# --------------------------------------------------------------------------------------
# GSEA
# --------------------------------------------------------------------------------------

@app.command("gsea")
def gsea(
    rnk: Path = typer.Option(..., "--rnk", help="Path to .rnk (gene\\tscore) file"),
    outdir: Path = typer.Option(..., "--outdir", "-o", help="Output directory for results & HTML"),
    min_gs_size: int = typer.Option(15, "--min-gs-size", help="Minimum gene set size"),
    max_gs_size: int = typer.Option(500, "--max-gs-size", help="Maximum gene set size"),
    pvalue_cutoff: float = typer.Option(0.05, "--pvalue-cutoff", help="P-value cutoff for filtered results"),
    qmd: Optional[Path] = typer.Option(None, "--qmd", help="Path to gsea.qmd (defaults to packaged one)"),
    quarto: Optional[str] = typer.Option(None, "--quarto", help="Path to Quarto executable (default: auto-detect)"),
    pass_args: Optional[str] = typer.Option(None, "--pass-args", help='Extra args for `quarto render` (e.g. "--no-execute")'),
):
    """
    Run the GSEA Quarto report (gsea.qmd) and expose key params at the CLI.

    Example:
        diffex gsea --rnk path/to/limma_gsea.rnk \\
                    --outdir results/gsea \\
                    --min-gs-size 15 --max-gs-size 500 --pvalue-cutoff 0.05
    """
    qmd_path = Path(qmd) if qmd else _default_gsea_qmd()
    extras = shlex.split(pass_args) if pass_args else None

    _run_quarto_render(
        qmd_path=qmd_path,
        outdir=outdir,
        rnk=rnk,
        min_gs_size=min_gs_size,
        max_gs_size=max_gs_size,
        pvalue_cutoff=pvalue_cutoff,
        quarto=quarto,
        extra_args=extras,
    )
    typer.secho(f"✅ GSEA report written to: {outdir}", fg=typer.colors.GREEN)

@app.command(name="version")
def version():
    """Show the version of DiffEx."""
    try:
        from diffex import __version__
        print(f"DiffEx version: {__version__}")
    except ImportError:
        print("DiffEx version: Unknown")

@app.command(name="help")
def help():
    """Show help message."""
    print("DiffEx CLI Help:")
    print("  - Use `diffex run` to run the Quarto report.")
    print("  - Use `diffex version` to check the version.")
    print("  - Use `diffex help` to see this message.")

def main():
    app()

if __name__ == "__main__":
    main()
