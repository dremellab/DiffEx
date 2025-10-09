# dev version

# v0.5.1

**Release date:** October 9, 2025

### 🔧 Build & Environment

* Refactored **Dockerfile**:

  * Added locale configuration (`en_US.UTF-8`) for consistent Quarto rendering.
  * Simplified `micromamba` install commands (added `libxml2-devel` to the micromamba environment ... required for properly installl `clusterProfiler` and `sva` Biocondunctor packages).
  * Explicitly disabled renv auto-loader via `RENV_CONFIG_AUTOLOADER_ENABLED=FALSE` ... not using `renv` for package installations.
  * Added `DIFFEX_COMMIT` build arg and support for pinning specific commits ... tags can also be parsed
  * Included docker helper scripts: `build_docker.sh` and `push_docker.sh`.

### 📦 R Environment & Dependency Fixes

* Introduced `.Renviron` with pinned CRAN snapshot:
  `https://packagemanager.posit.co/cran/__linux__/bookworm/2025-09-01` ... This pins down specific repo instead of using "latest".
* Updated `.Rprofile` to include micromamba R library in `.libPaths()` ... To include path in the mamba environment.
* Enhanced `install_R_packages.R`:

  * Added explicit `.libPaths()` initialization.
  * Switched CRAN source from cloud to pinned snapshot.
  * Added new helper/plotting packages (`rmarkdown`, `stringr`, `purrr`, `RColorBrewer`, `viridis`, `pheatmap`, `cowplot`, `patchwork`).
  * Improved Bioconductor detection, install messaging, and final status reporting.

### 🧬 Code Fixes & Features

* Added normalization helper in `normalize.qmd` to clean column names (replacing hyphens, prefixing digits).
* Addressed renv and CRAN version conflicts (reverted `ggplot2` 4.0.0 → 3.5.2).
* Updated `renv.lock` to use pinned CRAN URLs (replaced `/latest` with snapshot URLs).

### 🧰 Project & Metadata

* Added new RStudio project file `DiffEx.Rproj`.
* Updated `.gitignore` to include `build.log`.

# v0.5.0

### Added

- `normalize` subcommand to generated normalized counts matrix with all samples

### Changed

- logic to select rows and columns from raw counts matrix using "species" column in the input counts matrix if present
- minor bug fixes

# v0.4.1

### Changed

- CLI now shows --help when run without a command (diffex no longer errors with Missing command).
- Added -h as a shortcut for --help.

### Added

- New utility functions _ensure_readable and _ensure_writable for consistent file and folder checks.
- New _caller_func_name and _prepare_qmd helpers to auto-detect the subcommand name and copy the correct packaged QMD file into the output directory.

### Fixed

- Output QMD files (deg.qmd, gsea.qmd) are now always overwritten in the output directory for consistent runs.
- Improved error messages when input files or output directories are missing or not accessible.

# v0.4.0

### ✨ New Features

- **new `deg` and `gsea` subcommands**
  
  `run` command is replaced with `deg` and new `gsea` subcommand is added. Parameter parsing from python package to R/Qmd scripts is refactored completely. `gsea` subcommand takes `.rnk` file and runs `gsea` with _msigdb_ genesets using _clusterprofiler_.

- **version help**
  
  `--version` and `--help` works with both command and subcommands.

- **docker support**
  
  new `Dockerfile` added. Docker is built and available on [dockerhub](https://hub.docker.com/repository/docker/seqinfomics/diffex/general). 

# v0.3.0



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

