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
import importlib.metadata as md

## Hidden functions

def _print_version_and_exit(value: bool):
    if value:
        try:
            from diffex import __version__
            typer.echo(f"DiffEx {__version__}")
        except Exception:
            typer.echo("DiffEx (version unknown)")
        raise typer.Exit()
    
def version_option():
    return typer.Option(
        None,
        "--version",
        help="Show version and exit.",
        callback=_print_version_and_exit,
        is_eager=True,
    )

def _get_version() -> str:
    # Prefer package metadata; fallback to module attribute if present
    try:
        return md.version("diffex")
    except Exception:
        try:
            from diffex import __version__
            return __version__
        except Exception:
            return "unknown"

def _version_callback(value: bool):
    if value:
        typer.echo(f"DiffEx { _get_version() }")
        raise typer.Exit()

def _echo(cmd: list[str]) -> None:
    typer.echo(f"[cmd] {shlex.join(cmd)}")

def _ensure_exists(path: Path, what: str = "file") -> None:
    if not path.exists():
        typer.secho(f"❌ {what.capitalize()} not found: {path}", fg=typer.colors.RED)
        raise typer.Exit(code=2)

def _resolve_qmd(subcommand: str) -> Path:
    """
    Resolve a Quarto file packaged in the diffex module, e.g., gsea.qmd or deg.qmd.
    Looks for 'diffex/{subcommand}.qmd' inside the package or next to cli.py as fallback.
    
    Args:
        subcommand: Name of the subcommand (e.g., 'gsea', 'deg', etc.)

    Returns:
        Absolute Path to the .qmd file.
    """
    filename = f"{subcommand}.qmd"
    try:
        return Path(str(pkg_files("diffex") / filename))
    except Exception:
        # Fallback if not packaged
        return Path(__file__).resolve().parent / filename


def _run_quarto_render(
    qmd_path: Path,
    outhtmldir: Path,
    extra_args: Optional[list[str]] = None,
    execute_yaml: Optional[str] = "gsea.yaml",
    **params
) -> None:
    """
    Generic Quarto renderer that writes all `params` into a YAML file at outdir/execute_yaml
    and invokes `quarto render` with --execute-params.
    """
    exe = shutil.which("quarto")
    if not exe:
        typer.secho("❌ Quarto not found on PATH. Install from https://quarto.org/", fg=typer.colors.RED)
        raise typer.Exit(code=2)

    _ensure_exists(qmd_path, "Quarto file")
    outhtmldir.mkdir(parents=True, exist_ok=True)

    yaml_path = outhtmldir / execute_yaml
    with open(yaml_path, "w") as f:
        yaml.safe_dump(params, f, sort_keys=False)

    cmd = [
        exe, "render", str(qmd_path),
        "--to", "html",
        "--no-cache",
        "--self-contained",
        "--output-dir", str(outhtmldir),
        "--execute-params", str(yaml_path),
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
    outdir: Path = typer.Option(..., "--outdir", "-o", help="Output directory for results Excel & HTML"),
    min_gs_size: int = typer.Option(15, "--min-gs-size", help="Minimum gene set size"),
    max_gs_size: int = typer.Option(500, "--max-gs-size", help="Maximum gene set size"),
    pvalue_cutoff: float = typer.Option(0.05, "--pvalue-cutoff", help="P-value cutoff for filtered results"),
    qmd: Optional[Path] = typer.Option(None, "--qmd", help="Path to gsea.qmd (defaults to packaged one)"),
    quarto: Optional[str] = typer.Option(None, "--quarto", help="Path to Quarto executable (default: auto-detected)"),
    pass_args: Optional[str] = typer.Option(None, "--pass-args", help='Extra args for `quarto render` (e.g. "--no-execute")'),
    version: bool = version_option(),
):
    """
    Run the GSEA Quarto report (gsea.qmd) and expose key params at the CLI.

    Example:
        diffex gsea --rnk path/to/limma_gsea.rnk \\
                    --outdir results/gsea \\
                    --min-gs-size 15 --max-gs-size 500 --pvalue-cutoff 0.05
    """
    qmd_path = Path(qmd) if qmd else _resolve_qmd("gsea")
    extras = shlex.split(pass_args) if pass_args else None

    _run_quarto_render(
        qmd_path=qmd_path,
        outhtmldir=outdir,
        extra_args=extras,
        execute_yaml="gsea.yaml",  # can make configurable if needed
        rnk=str(rnk),
        outdir=str(outdir),
        minGSSize=min_gs_size,
        maxGSSize=max_gs_size,
        pvalueCutoff=pvalue_cutoff,
    )

    typer.secho(f"✅ GSEA report written to: {outdir}", fg=typer.colors.GREEN)


# --------------------------------------------------------------------------------------
# DEG
# --------------------------------------------------------------------------------------

@app.command("deg")
def deg(
    counts_file: Path = typer.Option(..., "--counts-file", "-c", help="Counts matrix file (TSV)"),
    samplesheet: Path = typer.Option(..., "--samplesheet", "-s", help="Sample sheet TSV/CSV"),
    use_ercc: bool = typer.Option(False, "--use-ercc", help="Whether to use ERCC spike-ins"),
    ercc_mix: int = typer.Option(1, "--ercc-mix", help="ERCC mix (1 or 2)"),
    group1: str = typer.Option(..., "--group1", help="First group name"),
    group2: str = typer.Option(..., "--group2", help="Second group name"),
    sample_column: str = typer.Option("sampleName", "--sample-column", help="Column in sample sheet for sample IDs"),
    group_column: str = typer.Option("groupName", "--group-column", help="Column for grouping factor"),
    usebatch: bool = typer.Option(False, "--use-batch", help="Whether to use batch as covariate"),
    batch_column: str = typer.Option("batch", "--batch-column", help="Column for batch information"),
    outdir: Path = typer.Option(..., "--outdir", "-o", help="Output directory"),
    host: str = typer.Option("Hs", "--host", help='Host species: "Hs" or "Mm"'),
    genes_selection: str = typer.Option("host", "--genes-selection", help='Filter genes: "host", "virus", or "both"'),
    log2fc_threshold: float = typer.Option(1.0, "--log2fc-threshold", help="Log2 fold-change threshold"),
    pvalue_threshold: float = typer.Option(0.05, "--pvalue-threshold", help="Raw p-value cutoff"),
    fdr_threshold: float = typer.Option(0.05, "--fdr-threshold", help="FDR cutoff"),
    edger_cpm_cutoff: float = typer.Option(0.1, "--edger-cpm-cutoff", help="edgeR CPM cutoff"),
    edger_cpm_group_fraction: float = typer.Option(0.5, "--edger-cpm-group-fraction", help="edgeR CPM group fraction"),
    deseq2_low_count_cutoff: int = typer.Option(2, "--deseq2-low-count-cutoff", help="DESeq2 low-count cutoff"),
    deseq2_low_count_group_fraction: float = typer.Option(0.5, "--deseq2-low-count-group-fraction", help="DESeq2 low-count group fraction"),
    qmd: Optional[Path] = typer.Option(None, "--qmd", help="Path to deg.qmd (defaults to packaged one)"),
    quarto: Optional[str] = typer.Option(None, "--quarto", help="Path to Quarto executable (default: auto-detected)"),
    pass_args: Optional[str] = typer.Option(None, "--pass-args", help="Extra args for `quarto render`"),
    version: bool = version_option(),
):
    """
    Run the DEG Quarto report (deg.qmd) and expose YAML params at the CLI.

    Example:
        diffex deg --counts-file counts.tsv --samplesheet samples.tsv --group1 KOS --group2 Uninf -o results/deg
    """
    qmd_path = Path(qmd) if qmd else _resolve_qmd("deg")
    extras = shlex.split(pass_args) if pass_args else None

    _run_quarto_render(
        qmd_path=qmd_path,
        outhtmldir=outdir,
        extra_args=extras,
        execute_yaml="deg.yaml",
        counts_file=str(counts_file),
        samplesheet=str(samplesheet),
        useERCC=use_ercc,
        ercc_mix=ercc_mix,
        group1=group1,
        group2=group2,
        sample_column=sample_column,
        group_column=group_column,
        usebatch=usebatch,
        batch_column=batch_column,
        outdir=str(outdir),
        host=host,
        genes_selection=genes_selection,
        log2FC_threshold=log2fc_threshold,
        pvalue_threshold=pvalue_threshold,
        fdr_threshold=fdr_threshold,
        edgeR_cpm_cutoff=edger_cpm_cutoff,
        edgeR_cpm_group_fraction=edger_cpm_group_fraction,
        DESeq2_low_count_cutoff=deseq2_low_count_cutoff,
        DESeq2_low_count_group_fraction=deseq2_low_count_group_fraction,
    )

    typer.secho(f"✅ DEG report written to: {outdir}", fg=typer.colors.GREEN)


# --------------------------------------------------------------------------------------
# version and help
# --------------------------------------------------------------------------------------

@app.command(name="version")
def version():
    """Show the version of DiffEx."""
    # try:
    #     from diffex import __version__
    #     print(f"DiffEx version: {__version__}")
    # except ImportError:
    #     print("DiffEx version: Unknown")
    print(f"DiffEx version: {_get_version()}")

@app.command(name="help")
def help():
    """Show help message."""
    print("DiffEx CLI Help:")
    print("  - Use `diffex run` to run the Quarto report.")
    print("  - Use `diffex version` to check the version.")
    print("  - Use `diffex help` to see this message.")

@app.callback()
def _main_callback(
    version: bool = typer.Option(
        None,
        "--version", "-V", "-v",
        help="Show version and exit.",
        callback=_version_callback,
        is_eager=True,
    ),
):
    # No-op: this callback only exists to host global options
    pass


# --------------------------------------------------------------------------------------
# main
# --------------------------------------------------------------------------------------

def main():
    app()

if __name__ == "__main__":
    main()
