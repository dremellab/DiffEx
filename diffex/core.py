import subprocess
from pathlib import Path

def run_quarto_report(qmd_path="DiffEx.qmd", params_file="params.yaml"):
    if not Path(qmd_path).exists():
        raise FileNotFoundError(f"❌ Quarto file not found: {qmd_path}")
    if not Path(params_file).exists():
        raise FileNotFoundError(f"❌ Params file not found: {params_file}")

    command = [
        "quarto", "render",
        qmd_path,
        "--to", "html",
        "--no-cache",
        "--self-contained",
        "--execute-params", params_file
    ]

    print("🚀 Running Quarto:")
    print(" ".join(command))
    subprocess.run(command, check=True)
