# dev version

# v0.2.0

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

