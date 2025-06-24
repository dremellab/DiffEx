# 🧬 diffex — Differential Expression Analysis with edgeR + DESeq2 + Quarto

![diffex logo](https://img.shields.io/badge/DE-analysis-success?style=flat-square&logo=r)

diffex — Differential Expression Analysis with edgeR + DESeq2 + limma

diffex is a reproducible and portable tool that performs differential gene expression (DGE) analysis using the edgeR package and generates an interactive Quarto HTML report 📊 — ready for publication or exploration.

Built with ❤️ for users of the HAROLD RNA-seq pipeline, diffex takes the output counts_matrix.tsv and samplesheet.tsv and produces beautifully summarized DEG results with visualization-rich reporting.

🚀 Features

- ✅ Accepts count matrix and sample metadata from HAROLD
- 🧪 Uses edgeR and DESeq2 for robust DE testing
- 📊 Produces interactive Quarto HTML reports
- 🌋 Includes volcano plots, PCA, box/violin plots, and summary tables
- 🔍 Easily configurable parameters via CLI or YAML
- 🐳 Dockerized for reproducibility

📝 Requirements

- R>=4.5.0
- quarto>=1.7.23

🛠️ Installation

```bash
# create new conda environment using:
conda env create -f environment.yaml

# inside the conda env create a virtual env
uv venv .venv

# activate the virtual environment
source .venv/bin/activate

# install the diffex package and its dependencies in the virtual env
uv pip install -r uv.lock

# Assuming R and quarto are already available at command line
# install R package dependencies
Rscript -e "renv::restore()"
```


✨ Happy diffex-ing!
