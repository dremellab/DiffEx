# Project Instructions

## General Working Principles

Before making changes, recommendations, or implementing analysis code:

1. Understand the biological and statistical question.
2. Inspect the existing project structure, code, metadata, and configuration.
3. Prefer established project conventions over introducing unnecessary new approaches.
4. Verify statistical and package-specific behavior against the local reference documentation when relevant.
5. Do not invent package functions, arguments, defaults, statistical recommendations, or undocumented behavior.
6. Explain important methodological choices and assumptions.

---

# Reference Documentation

Authoritative technical and methodological documentation is stored in:

`reference_docs/`

Before performing RNA-seq, differential-expression, normalization, or related statistical work, inspect the relevant documents in this directory.

The presence of local documentation means you should prefer these references over relying solely on memory.

## Available References

### DESeq2

`reference_docs/DESeq2.pdf`

Consult for:

- DESeq2 workflows
- count matrix requirements
- `DESeqDataSet`
- design formulas
- size-factor estimation
- normalization
- dispersion estimation
- Wald tests
- likelihood-ratio tests
- contrasts and coefficients
- interactions
- batch covariates
- paired designs
- log2 fold-change shrinkage
- independent filtering
- transformations such as VST and rlog
- PCA and visualization
- multiple-testing correction

---

### edgeR

`reference_docs/edgeRUsersGuide.pdf`

Consult for:

- `DGEList`
- `filterByExpr`
- TMM normalization
- normalization factors
- dispersion estimation
- GLM workflows
- quasi-likelihood workflows
- `glmQLFit`
- `glmQLFTest`
- likelihood-ratio testing
- design matrices
- contrasts
- blocking and batch variables
- complex experimental designs
- differential-expression analysis

---

### limma / voom

`reference_docs/limmaUsersGuide.pdf`

Consult for:

- linear modeling
- design matrices
- contrasts
- `lmFit`
- `contrasts.fit`
- empirical Bayes methods
- `eBayes`
- `voom`
- `voomWithQualityWeights`
- observational weights
- blocking
- `duplicateCorrelation`
- batch effects
- complex experimental designs
- RNA-seq analysis using limma-voom

---

# ERCC Spike-In References

ERCC-specific documentation and methodological literature are also stored in `reference_docs/`.

### ERCC User Guide

`reference_docs/ERCC_User_Guide.pdf`

Consult for:

- composition of ERCC spike-in mixes
- expected concentrations
- Mix 1 / Mix 2 relationships
- recommended spike-in usage
- dilution
- experimental setup
- interpretation of ERCC controls

---

### Jiang et al. 2011

`reference_docs/Jiang_2011_ERCC.pdf`

Consult for:

- original ERCC RNA-seq benchmarking framework
- dynamic range
- sensitivity
- detection limits
- expected versus observed ERCC abundance
- technical bias
- ERCC behavior in sequencing experiments

---

### Risso et al. 2014

`reference_docs/Risso_2014_RUV.pdf`

Consult for:

- normalization using control genes
- ERCC controls
- unwanted technical variation
- RUV methodology
- limitations of simple ERCC scaling
- factor-analysis approaches to normalization
- distinguishing technical from biological variation

---

### RUVSeq

`reference_docs/RUVSeq_Vignette.pdf`

Consult for:

- `RUVg`
- `RUVs`
- `RUVr`
- using ERCCs as negative controls
- estimating unwanted variation
- integration with differential-expression workflows
- incorporating unwanted-variation factors into statistical models

---

### SEQC / MAQC-III

`reference_docs/SEQC_MAQCIII_2014.pdf`

Consult for:

- RNA-seq reproducibility
- technical performance
- cross-platform behavior
- differential-expression benchmarking
- sensitivity and specificity
- best-practice considerations for RNA-seq experiments

---

### ERCC Dashboard / Munro et al.

`reference_docs/Munro_2014_ERCC_Dashboard.pdf`

Consult for:

- ERCC-based RNA-seq QC
- dynamic range
- detection limits
- expected versus observed fold changes
- abundance-dependent bias
- technical performance metrics
- ERCC response curves
- diagnostic interpretation of spike-in behavior

---

# RNA-seq Analysis Rules

For RNA-seq analysis, begin with raw integer counts unless the relevant method explicitly requires another representation.

Do not feed TPM, FPKM, CPM, normalized counts, or transformed expression values into DESeq2 or count-based edgeR differential-expression models unless there is a documented and justified reason.

Before differential-expression analysis, identify:

- biological condition
- experimental unit
- biological replicates
- technical replicates
- paired or repeated measurements
- batch variables
- donor or subject variables
- treatment variables
- interactions
- confounders
- sequencing/library preparation design

Construct the statistical design from the experimental design, not merely from column names available in the metadata.

---

# Choosing DESeq2, edgeR, or limma-voom

Do not choose a differential-expression framework arbitrarily.

When modifying an existing analysis, prefer the framework already used unless there is a documented reason to change it.

When designing a new analysis, consider:

- experimental design
- sample size
- count distribution
- need for observational weights
- repeated measurements
- complex contrasts
- existing project conventions
- downstream requirements

Use the corresponding local user guide before implementing unfamiliar or complex functionality.

---

# ERCC Spike-In Analysis

ERCC spike-ins require special consideration.

The presence of ERCC reads does **not** automatically mean ERCCs should be used as library-size normalization factors.

Before recommending ERCC-based normalization, determine:

1. Why were ERCCs included?
2. At what experimental stage were they added?
3. What amount of ERCC was added to each sample?
4. What biological quantity was held constant?
5. Were equal numbers of cells used?
6. Was equal tissue mass used?
7. Was equal total RNA mass used?
8. Were ERCCs added before or after RNA extraction?
9. Were the same ERCC mix and dilution used across samples?
10. Is a global shift in endogenous RNA abundance biologically expected?

These details determine what conclusions can legitimately be drawn from ERCC counts.

---

## Distinguish Three Uses of ERCCs

Always distinguish between:

### 1. ERCCs as technical QC controls

Use ERCCs to examine:

- detection sensitivity
- dynamic range
- expected versus observed concentration
- technical reproducibility
- abundance-dependent bias
- fold-change accuracy
- sequencing/library preparation performance

In this situation, endogenous RNA can still use standard DESeq2, edgeR, or limma-voom normalization.

---

### 2. ERCCs as negative-control genes

ERCCs may be used to estimate unwanted technical variation.

When appropriate, consult:

- `Risso_2014_RUV.pdf`
- `RUVSeq_Vignette.pdf`

Consider RUV approaches rather than reducing ERCC information to a single scaling factor.

---

### 3. ERCCs as external scaling controls

ERCC-based scaling may be appropriate when the biological question requires retaining global changes in RNA abundance that compositional normalization could remove.

This requires careful examination of how ERCCs were added.

Do not implement ERCC scaling solely because spike-ins are available.

---

# Standard Normalization vs ERCC Normalization

For conventional bulk RNA-seq where most genes are not expected to change globally, first consider standard methods such as:

- DESeq2 median-ratio size factors
- edgeR TMM normalization
- limma-voom with appropriate normalization factors

For experiments where treatment may cause widespread/global transcriptional changes, investigate whether conventional compositional normalization could normalize away the biological effect.

In that situation, evaluate ERCC-based approaches using the local ERCC references before choosing a strategy.

---

# ERCC QC Before Normalization

Before using ERCC-derived normalization factors, evaluate ERCC technical performance.

At minimum, examine per sample:

- total ERCC counts
- ERCC fraction of mapped reads
- number of detected ERCC transcripts
- expected ERCC concentration versus observed counts
- log10 expected concentration versus log10 observed counts
- regression slope
- regression intercept
- R²
- abundance-dependent residuals
- potential outlier ERCC transcripts
- sample-to-sample ERCC consistency

When Mix 1 and Mix 2 or known expected fold-change groups are available, also evaluate:

- expected versus observed fold change
- fold-change accuracy by abundance
- detection limits
- deviation from expected ERCC ratios

Do not use an ERCC normalization method when ERCC QC indicates substantial unexplained technical problems without investigating those problems first.

---

# ERCC Regression Interpretation

When evaluating:

`log10(expected concentration)`

versus:

`log10(observed counts)`

do not use R² alone.

Also inspect:

- slope
- intercept
- residual structure
- low-abundance behavior
- high-abundance saturation
- outliers

A high R² does not guarantee absence of systematic bias.

A slope substantially different from the expected relationship can indicate abundance-dependent technical effects.

Consult:

- `ERCC_User_Guide.pdf`
- `Jiang_2011_ERCC.pdf`
- `Munro_2014_ERCC_Dashboard.pdf`

before interpreting these diagnostics.

---

# DESeq2 With ERCCs

If considering ERCCs for DESeq2 size-factor estimation, verify the proposed approach against `DESeq2.pdf`.

DESeq2 supports estimating size factors using specified control genes.

However, do not automatically treat ERCC genes as control genes.

First determine whether ERCC-based scaling represents the intended biological quantity.

If ERCC-derived size factors are used, retain raw endogenous gene counts and supply the appropriate size factors through the DESeq2 framework rather than manually transforming the count matrix unless the documentation explicitly recommends otherwise.

---

# ERCCs and Global Expression Changes

Be particularly cautious when the experimental condition may alter total RNA production per cell.

Standard compositional normalization generally estimates relative abundance.

Consequently, a biological condition that increases or decreases most transcripts together may appear much smaller after standard library normalization.

External spike-ins may allow global changes to be retained if the experiment was designed appropriately.

Before claiming an absolute or per-cell global transcriptional change, verify that the spike-in design supports that interpretation.

For example, distinguish carefully between:

- equal ERCC per cell
- equal ERCC per tissue amount
- equal ERCC per total RNA mass

These normalization anchors answer different biological questions.

---

# Statistical Modeling

Do not use normalization to compensate for variables that belong in the statistical design.

When appropriate, include known covariates such as:

- batch
- donor
- sex
- treatment
- time point
- sequencing run
- library preparation batch

in the model rather than attempting to remove them through ad hoc preprocessing.

Check for confounding before fitting the model.

Do not include variables that are perfectly confounded with the biological condition and then interpret the resulting model as if the effects were independently estimable.

---

# Contrasts and Coefficients

For DESeq2, edgeR, and limma:

Before constructing a contrast:

1. Inspect factor levels.
2. Inspect the design matrix.
3. Determine the reference level.
4. Determine the exact biological comparison.
5. Verify the coefficient or contrast mathematically.
6. Check interactions when present.

Do not guess contrast syntax.

For complex designs, consult the relevant user guide before implementing the contrast.

---

# Repeated Measures and Paired Designs

When samples originate from the same individual, animal, donor, cell line, or other experimental unit across conditions, determine whether a blocking or paired design is required.

Do not treat repeated measurements as independent biological replicates.

Consult:

- `DESeq2.pdf`
- `edgeRUsersGuide.pdf`
- `limmaUsersGuide.pdf`

for method-specific handling.

---

# Batch Effects

Do not automatically remove batch effects from the count matrix before differential-expression testing.

When batch is known and the design permits it, preferentially account for batch in the statistical model.

Methods such as batch correction of transformed expression values may be appropriate for visualization or specific downstream analyses but should not automatically replace correct modeling of raw counts.

---

# Transformations

Clearly distinguish between data used for statistical testing and data used for visualization.

For example:

- raw counts → differential-expression models
- VST/rlog → visualization, clustering, PCA
- voom-transformed values → limma modeling where appropriate

Do not run differential-expression tests on transformed DESeq2 visualization matrices unless specifically supported by the method being used.

---

# Multiple Testing

Use appropriate false-discovery-rate correction for genome-wide differential-expression testing.

Do not report nominal p-values as the primary significance criterion when thousands of genes are tested.

Report or retain:

- effect size
- log2 fold change
- adjusted p-value / FDR
- relevant uncertainty/statistical information

where appropriate.

---

# Documentation and Reproducibility

For important analysis decisions, state the rationale.

When local documentation informs a methodological choice, mention the relevant reference, for example:

> Based on the DESeq2 user guide...

or:

> The RUVSeq vignette recommends...

Do not fabricate quotations or page numbers.

If a conclusion depends on a specific detail from a reference, inspect that document rather than relying solely on remembered behavior.

Record important assumptions in the analysis code or associated documentation.

Prefer reproducible scripted analyses over manual processing.

---

# Reference Priority

For RNA-seq methodological questions, use the following priority:

1. Local package/user documentation in `reference_docs/`
2. Local primary methodological papers in `reference_docs/`
3. Current official package documentation
4. Primary peer-reviewed literature
5. Established community practice
6. Model memory

When documentation disagrees with remembered behavior, verify the installed package version and follow the documentation appropriate to that version.

---

# Critical Rule

For RNA-seq or ERCC-related work:

**Do not make a methodological recommendation solely from memory when the relevant documentation exists in `reference_docs/`.**

Inspect the appropriate reference first, then make the recommendation based on the experimental design, statistical question, and documented behavior of the analysis method.