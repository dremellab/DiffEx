---
name: bioinformatics-analysis
description: >
  Use when analyzing or modifying bioinformatics workflows involving
  RNA-seq, differential expression, DESeq2, edgeR, limma, or voom.
---

# Bioinformatics Analysis

Before making methodological recommendations:

1. Inspect the project's `reference_docs/README.md`.
2. Identify the authoritative package documentation.
3. Read the relevant reference documentation.
4. Inspect the existing analysis code and design matrix.
5. Verify statistical assumptions before changing code.

For differential expression:

- DESeq2 → consult `reference_docs/DESeq2.pdf`
- edgeR → consult `reference_docs/edgeRUsersGuide.pdf`
- limma/voom → consult `reference_docs/limmaUsersGuide.pdf`

Never rely solely on remembered package behavior when the corresponding
reference documentation is available.

Pay particular attention to:

- experimental design
- contrasts
- interactions
- repeated measures
- batch variables
- normalization
- filtering
- dispersion
- hypothesis testing
- multiple testing
- effect-size shrinkage

When proposing code, explain the statistical rationale and identify the
relevant reference document.