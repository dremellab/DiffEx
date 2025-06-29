# dev version

# v0.3.0

### ✨ New Features

- **Limma Support Added**  
  DiffEx now supports differential expression analysis using the `limma` package, expanding beyond `edgeR` and `DESeq2`.

- **Quarto Compatibility Enhancements**  
  - Quarto `.qmd` workflows now initialize R environments via `renv` more reliably.
  - Enhanced interactivity and reproducibility of reports.

- **Reproducible Environments**
  - Added `renv.lock`, `uv.lock`, and `environment.yaml` to support reproducible pipelines in R, Python, and Quarto.
  - Added `.Rprofile` and `renv/activate.R` for seamless `renv` bootstrapping.

- **Version Synchronization Tools**
  - New utility `scripts/sync_version.py` syncs version between `pyproject.toml` and `__init__.py`.

- **Cross-Platform CLI Support**
  - Improved `Path.expanduser()` logic ensures user home directories work across operating systems.

### 🛠 Improvements

- Updated `.gitignore` to exclude:
  - `renv/`, `python/`, `staging/`, `.mypy_cache/`, and `.pytest_cache/`.

- Enhanced `README.md` with:
  - Conda + `uv` setup instructions.
  - Announcements for `limma` support.
  - Clarified multi-language (R and Python) usage.

### 🧪 Technical Updates
.
- Scripts and config files added to unify environments across R, Python, and Quarto.
- Improved automation for environment setup and versioning.

# v0.2.x

## Highlights

### 🔍 DESeq2 & edgeR Enhancements
- Added low-count filtering for DESeq2.
- ERCC rows removed from DGE and DDS objects prior to DEG contrast.
- Default values for:
  - `log2FC_threshold` set to `1.0` (float).
  - `edgeR_cpm_cutoff` set to `1.0` (float).
- Added:
  - **BCV plot** for edgeR.
  - **MA plot** and **dispersion plot** for DESeq2.

### ⚖️ Normalization Improvements
- Added **conditional voom normalization** when `useERCC = FALSE`.
- Automatically switches between **ERCC-based** and **voom** workflows.
- Output files and visualizations dynamically adapt to the normalization method used.

### ✨ New Features
- **GSEA rank score** (`sign(log2FC) * -log10(pval)`) added to all DEG result tables.
- Sample-wise **ERCC counts** now displayed.
- **Venn diagram** summarizing DEG overlaps added.

### 🛠 Usability & Structure
- Separated parameter YAML files:
  - `params_sent.yaml`: generated from Python.
  - `params_received.yaml`: used by R.
- Ignoring all folders beginning with `results*`.
- Included ERCC reference assets from:
  - https://github.com/mschertzer/ercc_analysis

### 🧼 CLI and Code Improvements
- CLI now resolves all input/output paths to **absolute paths**.
- Cleaned and refactored parameter logic and naming conventions for clarity.

