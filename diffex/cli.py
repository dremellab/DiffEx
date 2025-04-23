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
    params_path = outdir / "params.yaml"
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

    # print("✅ Parsed params:", parsed["params"])
    # exit(0)
    if not match:
        raise ValueError("❌ Could not find `params:` block in the .qmd file")

    params_yaml = "params:\n" + match.group(1)
    parsed = yaml.safe_load(params_yaml)
    return parsed.get("params", {})

def run_quarto(
    params: Dict[str, Any],
    qmd_file: str,
    params_path: Path,
    outdir: Path
):
    outdir.mkdir(parents=True, exist_ok=True)

    # Copy the QMD file to the output folder
    qmd_name = Path(qmd_file).name
    qmd_in_outdir = outdir / qmd_name
    shutil.copy2(qmd_file, qmd_in_outdir)

    command = [
        "quarto", "render", qmd_name,
        "--to", "html",
        "--no-cache",
        "--self-contained",
        "--execute-params", str(params_path.name)    ]

    print(f"🚀 Running Quarto in: {outdir}")
    subprocess.run(command, check=True, cwd=outdir.resolve())


def build_dynamic_render_command():
    qmd_file = get_qmd_path()
    param_defaults = parse_qmd_params(qmd_file)

    def render(outdir: str = "results", **kwargs):
        outdir_path = Path(outdir)

        final_params = {
            key: kwargs.get(key, default)
            for key, default in param_defaults.items()
            if key != "outdir"
        }

        # # Redirect output paths to outdir
        # final_params = normalize_paths(final_params, outdir_path)

        # Write params.yaml into the output directory
        params_path = write_params_yaml(final_params, outdir_path)

        # Run Quarto from the current working directory, reading the qmd
        run_quarto(
            params=final_params,
            qmd_file=qmd_file,
            params_path=params_path,
            outdir=outdir_path
        )


    # 🔁 Dynamically build CLI signature
    parameters = [
    Parameter(
        name="outdir",
        kind=Parameter.KEYWORD_ONLY,
        default=typer.Option("results", help="Directory to store all outputs"),
        annotation=str
    )
    ]
    for key, default in param_defaults.items():
        param_type = type(default)
        parameters.append(
            Parameter(
                name=key,
                kind=Parameter.KEYWORD_ONLY,
                default=typer.Option(
                    default,
                    help=f"Quarto param: `{key}`",
                    show_default=True
                ),
                annotation=param_type  # 👈 this tells Typer to use float/int/etc
            )
        )

    render.__signature__ = Signature(parameters)
    return render


# Register dynamic command AFTER assigning signature
app.command(name="render")(build_dynamic_render_command())

def main():
    app()

if __name__ == "__main__":
    main()
