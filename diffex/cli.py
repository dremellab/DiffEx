import typer
import yaml
import shutil
import os
import subprocess
from pathlib import Path
from typing import Dict, Any
from inspect import Parameter, Signature
import re
import importlib.resources as pkg_resources

app = typer.Typer()

def normalize_paths(params: dict, outdir: Path) -> dict:
    """Redirect output files to outdir; do not touch input files."""
    output_keys = {
        "normalized_counts_file",
        "deg_results_file",
    }

    for key in output_keys:
        if key in params and isinstance(params[key], str):
            params[key] = str(outdir / Path(params[key]).name)

    return params

def write_params_yaml(params: dict, outdir: Path) -> Path:
    outdir.mkdir(parents=True, exist_ok=True)
    params_path = outdir / "params_sent.yaml"
    with open(params_path, "w") as f:
        yaml.safe_dump(params, f)
    print(f"📝 params.yaml written to: {params_path}")
    return params_path

def get_qmd_path() -> str:
    with pkg_resources.path("diffex", "DiffEx.qmd") as path:
        return str(path)

def parse_qmd_params(qmd_path: str) -> Dict[str, Any]:
    """Parse YAML `params:` block from a Quarto .qmd file."""
    with open(qmd_path, "r") as f:
        content = f.read()

    match = re.search(r"^params:\n((?:\s{2,}.*\n)+)", content, re.MULTILINE)
    if not match:
        raise ValueError("Could not extract `params:` block")

    params_block = "params:\n" + match.group(1)
    parsed = yaml.safe_load(params_block)
    return parsed.get("params", {})

def run_quarto(
    params: Dict[str, Any],
    qmd_file: str,
    params_path: Path,
    outdir: Path
):
    outdir.mkdir(parents=True, exist_ok=True)

    qmd_name = Path(qmd_file).name
    qmd_in_outdir = outdir / qmd_name
    shutil.copy2(qmd_file, qmd_in_outdir)

    command = [
        "quarto", "render", qmd_name,
        "--to", "html",
        "--no-cache",
        "--self-contained",
        "--execute-params", str(params_path.name)
    ]

    print(f"🚀 Running Quarto in: {outdir}")
    subprocess.run(command, check=True, cwd=outdir.resolve())

@app.command(name="run")
def build_dynamic_render_command():
    qmd_file = get_qmd_path()
    param_defaults = parse_qmd_params(qmd_file)

    def render(**kwargs):
        """Run DEG analysis and generate Quarto report."""
        outdir = kwargs.get("outdir", "results")
        outdir_path = Path(outdir)
        outdir_path = outdir_path.expanduser().resolve()

        final_params = {
            key: kwargs.get(key, default)
            for key, default in param_defaults.items()
        }
        final_params["outdir"] = str(outdir_path)  # Add outdir explicitly to params

        params_path = write_params_yaml(final_params, outdir_path)

        run_quarto(
            params=final_params,
            qmd_file=qmd_file,
            params_path=params_path,
            outdir=outdir_path
        )

    parameters = [
        Parameter(
            name="outdir",
            kind=Parameter.KEYWORD_ONLY,
            default=typer.Option("results", help="Directory to store all outputs"),
            annotation=str
        )
    ]

    for key, default in param_defaults.items():
        if key == "outdir":
            continue  # prevent duplicate
        param_type = type(default)
        default_value = default
        if key == "counts_file" or key == "samplesheet":
            default_value = str(Path(default_value).expanduser().resolve())
        parameters.append(
            Parameter(
                name=key,
                kind=Parameter.KEYWORD_ONLY,
                default=typer.Option(
                    default_value,
                    help=f"Quarto param: `{key}`",
                    show_default=True
                ),
                annotation=param_type
            )
        )

    render.__signature__ = Signature(parameters)
    return render

app.command(name="run")(build_dynamic_render_command())
app.command(name="dummy")(lambda: print("Dummy command executed!"))

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
