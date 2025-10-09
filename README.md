# 🧬 DiffEx — Differential Expression Analysis with (edgeR + DESeq2 + limma) using Quarto

![diffex logo](https://img.shields.io/badge/Differential%20Expression-Reproducible-success?style=flat-square\&logo=r)
[![Docker Image](https://img.shields.io/badge/Docker-Available-blue?logo=docker)](https://hub.docker.com/r/seqinfomics/diffex)
[![R version](https://img.shields.io/badge/R-4.4.3-blue?logo=r)](https://www.r-project.org/)
[![Bioconductor](https://img.shields.io/badge/Bioconductor-3.20-blue?logo=bioconductor)](https://bioconductor.org/)

---

**DiffEx** is a reproducible and portable tool for differential gene expression (DGE) analysis using **edgeR**, **DESeq2**, and **limma**.
It generates **interactive Quarto HTML reports** 📊 — publication-ready or exploratory.

Built with ❤️ for users of the **HAROLD RNA-seq** pipeline, DiffEx consumes `counts_matrix.tsv` and `samplesheet.tsv` to produce richly visualized, interpretation-ready DEG reports.

---

## 🚀 Features

* ✅ Accepts **count matrix** and **sample metadata** from HAROLD RNA-seq
* 🧪 Supports **edgeR**, **DESeq2**, and **limma**
* 📊 Produces **interactive Quarto HTML** reports
* 🌋 Includes **volcano plots**, **PCA**, **box/violin plots**, **UpSet plots**, and **summary tables**
* 🔍 Configurable via YAML or command-line parameters
* 🐳 **Dockerized** and **Apptainer-ready**
* 📦 Uses **renv** and **pinned CRAN snapshots** for version-stable R environments

---

## 🧰 Requirements

| Component              | Version                  |
| ---------------------- | ------------------------ |
| **R**                  | ≥ 4.4.3                  |
| **Quarto**             | ≥ 1.4.550                |
| **micromamba**         | ≥ 1.5                    |
| **Docker / Apptainer** | optional but recommended |

---

## ⚙️ Installation

### 🐳 **Using Docker**

```bash
# clone the repo
git clone https://github.com/dremellab/DiffEx.git
cd DiffEx

# build the image (v0.5.1)
docker buildx build --build-arg DIFFEX_COMMIT=v0.5.1 -t dremellab/diffex:0.5.1 .
```

### 🧫 **Using Apptainer/Singularity**

```bash
apptainer build diffex.sif docker-daemon://dremellab/diffex:0.5.1
apptainer exec diffex.sif quarto render diffex/diffex.qmd
```

---

## 🧬 Local (Developer) Setup

```bash
# 1️⃣ Create micromamba environment
micromamba create -n diffex-env -f environment.yaml
micromamba activate diffex-env

# 2️⃣ Install R packages (pinned snapshot)
Rscript diffex/install_R_packages.R

# 3️⃣ Disable renv autoloader for Quarto
export RENV_CONFIG_AUTOLOADER_ENABLED=FALSE

# 4️⃣ Render a Quarto report
quarto render diffex/diffex.qmd
```

All packages are pinned to:

```
https://packagemanager.posit.co/cran/__linux__/bookworm/2025-09-01
```

for full reproducibility.

---

## 🧩 Command help

```bash
diffex --help

 Usage: diffex [OPTIONS] COMMAND [ARGS]...

 DiffEx: Differential Expression Analysis Reports


╭─ Options ────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --version  -V,-v        Show version and exit.                                                           │
│ --help     -h           Show this message and exit.                                                      │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Commands ───────────────────────────────────────────────────────────────────────────────────────────────╮
│ gsea        Run the GSEA Quarto report (gsea.qmd)                                                        │
│ deg         Run the DEG Quarto report (deg.qmd)                                                          │
│ normalize   Run the normalization Quarto report (normalize.qmd) and output normalized counts only.       │
│ version     Show the version of DiffEx.                                                                  │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────╯

```

### deg

```bash
 diffex deg --help

 Usage: diffex deg [OPTIONS]

 Run the DEG Quarto report (deg.qmd)

 Example:     diffex deg --counts-file counts.tsv --samplesheet samples.tsv --group1 KOS --group2 Uninf -o
 results/deg

╭─ Options ────────────────────────────────────────────────────────────────────────────────────────────────╮
│ *  --counts-file                      -c      PATH     Counts matrix file (TSV) [default: None]          │
│                                                        [required]                                        │
│ *  --samplesheet                      -s      PATH     Sample sheet TSV/CSV [default: None] [required]   │
│    --use-ercc                                          Whether to use ERCC spike-ins                     │
│    --ercc-mix                                 INTEGER  ERCC mix (1 or 2) [default: 1]                    │
│ *  --group1                                   TEXT     First group name [default: None] [required]       │
│ *  --group2                                   TEXT     Second group name [default: None] [required]      │
│    --sample-column                            TEXT     Column in sample sheet for sample IDs             │
│                                                        [default: sampleName]                             │
│    --group-column                             TEXT     Column for grouping factor [default: groupName]   │
│    --use-batch                                         Whether to use batch as covariate                 │
│    --batch-column                             TEXT     Column for batch information [default: batch]     │
│ *  --outdir                           -o      PATH     Output directory [default: None] [required]       │
│    --host                                     TEXT     Host species: "Hs" or "Mm" [default: Hs]          │
│    --genes-selection                          TEXT     Filter genes: "host", "virus", or "both"          │
│                                                        [default: both]                                   │
│    --log2fc-threshold                         FLOAT    Log2 fold-change threshold [default: 1.0]         │
│    --pvalue-threshold                         FLOAT    Raw p-value cutoff [default: 0.05]                │
│    --fdr-threshold                            FLOAT    FDR cutoff [default: 0.05]                        │
│    --edger-cpm-cutoff                         FLOAT    edgeR CPM cutoff [default: 0.1]                   │
│    --edger-cpm-group-fraction                 FLOAT    edgeR CPM group fraction [default: 0.5]           │
│    --deseq2-low-count-cutoff                  INTEGER  DESeq2 low-count cutoff [default: 2]              │
│    --deseq2-low-count-group-fraction          FLOAT    DESeq2 low-count group fraction [default: 0.5]    │
│    --pass-args                                TEXT     Extra args for `quarto render` [default: None]    │
│    --version                                           Show version and exit.                            │
│    --help                             -h               Show this message and exit.                       │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

### normalize

```bash
diffex normalize --help

 Usage: diffex normalize [OPTIONS]

 Run the normalization Quarto report (normalize.qmd) and output normalized counts only.

 Example:     diffex normalize --counts-file counts.tsv --samplesheet samples.tsv -o results/norm

╭─ Options ────────────────────────────────────────────────────────────────────────────────────────────────╮
│ *  --counts-file                      -c      PATH     Counts matrix file (TSV) [default: None]          │
│                                                        [required]                                        │
│ *  --samplesheet                      -s      PATH     Sample sheet TSV/CSV [default: None] [required]   │
│    --use-ercc                                          Whether to use ERCC spike-ins                     │
│    --ercc-mix                                 INTEGER  ERCC mix (1 or 2) [default: 1]                    │
│    --sample-column                            TEXT     Column in sample sheet for sample IDs             │
│                                                        [default: sampleName]                             │
│    --group-column                             TEXT     Column for grouping factor [default: groupName]   │
│    --use-batch                                         Whether to use batch as covariate                 │
│    --batch-column                             TEXT     Column for batch information [default: batch]     │
│ *  --outdir                           -o      PATH     Output directory [default: None] [required]       │
│    --host                                     TEXT     Host species: "Hs" or "Mm" [default: Hs]          │
│    --genes-selection                          TEXT     Filter genes: "host", "virus", or "both"          │
│                                                        [default: host]                                   │
│    --edger-cpm-cutoff                         FLOAT    edgeR CPM cutoff [default: 0.1]                   │
│    --edger-cpm-group-fraction                 FLOAT    edgeR CPM group fraction [default: 0.5]           │
│    --deseq2-low-count-cutoff                  INTEGER  DESeq2 low-count cutoff [default: 2]              │
│    --deseq2-low-count-group-fraction          FLOAT    DESeq2 low-count group fraction [default: 0.5]    │
│    --pass-args                                TEXT     Extra args for `quarto render` [default: None]    │
│    --version                                           Show version and exit.                            │
│    --help                             -h               Show this message and exit.                       │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

### gsea

```bash
diffex gsea --help

 Usage: diffex gsea [OPTIONS]

 Run the GSEA Quarto report (gsea.qmd)

 Example:     diffex gsea --rnk path/to/limma_gsea.rnk \                 --outdir results/gsea \
 --min-gs-size 15 --max-gs-size 500 --pvalue-cutoff 0.05

╭─ Options ────────────────────────────────────────────────────────────────────────────────────────────────╮
│ *  --rnk                    PATH     Path to .rnk (gene\tscore) file [default: None] [required]          │
│ *  --outdir         -o      PATH     Output directory for results Excel & HTML [default: None]           │
│                                      [required]                                                          │
│    --min-gs-size            INTEGER  Minimum gene set size [default: 15]                                 │
│    --max-gs-size            INTEGER  Maximum gene set size [default: 500]                                │
│    --pvalue-cutoff          FLOAT    P-value cutoff for filtered results [default: 0.05]                 │
│    --pass-args              TEXT     Extra args for `quarto render` (e.g. "--no-execute")                │
│                                      [default: None]                                                     │
│    --version                         Show version and exit.                                              │
│    --help           -h               Show this message and exit.                                         │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

---

## ✨ Happy diffex-ing!

> “Reproducible science is beautiful science.” 💡
