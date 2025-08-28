# install_all_pkgs.R

pkgs_raw <- c(
  "limma","edgeR","DESeq2",
  "tibble","readr","dplyr","tidyr","ggplot2","plotly","tidyverse",
  "EnhancedVolcano","knitr","kableExtra",
  "fgsea","clusterProfiler","msigdbr",
  "AnnotationDbi","org.Mm.eg.db","org.Hs.eg.db",
  "openxlsx","ggplotify","ggpubr","ggrepel","glue","DT",
  "ComplexHeatmap",
  "UpSetR","yaml","fs","VennDiagram","grid","sva"
)

pkgs <- unique(pkgs_raw)
base_like <- c("grid")  # ships with base R; don’t install
pkgs <- setdiff(pkgs, base_like)

options(repos = c(CRAN = "https://cloud.r-project.org"))

if (!requireNamespace("BiocManager", quietly = TRUE)) {
  install.packages("BiocManager")
}
message("Bioconductor via BiocManager ", as.character(utils::packageVersion("BiocManager")),
        " (Bioc ", BiocManager::version(), ")")

bioc_avail <- tryCatch(BiocManager::available(), error = function(e) character())
is_bioc <- pkgs %in% bioc_avail

bioc_pkgs <- pkgs[is_bioc]
cran_pkgs <- pkgs[!is_bioc]

installed <- rownames(installed.packages())
need_bioc <- setdiff(bioc_pkgs, installed)
need_cran <- setdiff(cran_pkgs, installed)

if (length(need_cran)) {
  message("Installing CRAN: ", paste(need_cran, collapse = ", "))
  install.packages(need_cran)
} else {
  message("No CRAN packages to install.")
}

if (length(need_bioc)) {
  message("Installing Bioconductor: ", paste(need_bioc, collapse = ", "))
  BiocManager::install(need_bioc, update = FALSE, ask = FALSE)
} else {
  message("No Bioconductor packages to install.")
}

still_missing <- setdiff(pkgs, rownames(installed.packages()))
if (length(still_missing)) {
  message("WARNING: still missing: ", paste(still_missing, collapse = ", "))
}

suppressPackageStartupMessages({
  failed <- character()
  for (p in pkgs) {
    if (!require(p, character.only = TRUE, quietly = TRUE, warn.conflicts = FALSE)) {
      failed <- c(failed, p)
    }
  }
  if (length(failed)) message("NOTE: failed to load -> ", paste(failed, collapse = ", "))
  else message("All requested packages loaded.")
})
