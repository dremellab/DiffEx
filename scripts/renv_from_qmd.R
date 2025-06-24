# ----------------------------
# R Script: init_renv_from_qmd.R
# ----------------------------
Sys.setenv(CC = "clang")
Sys.setenv(CXX = "clang++")

# Path to your Quarto .qmd file
qmd_file <- "diffex/DiffEx.qmd"

# Initialize renv (bare = TRUE avoids automatic snapshot)
if (!requireNamespace("renv", quietly = TRUE)) install.packages("renv")
renv::init(bare = TRUE)

# Read and extract package names from library() calls
lines <- readLines(qmd_file)
library_lines <- grep("library\\(", lines, value = TRUE)
pkgs <- unique(gsub(".*library\\(([^)]+)\\).*", "\\1", library_lines))
pkgs <- trimws(pkgs)  # Remove leading/trailing whitespace

# Ensure BiocManager is installed
if (!requireNamespace("BiocManager", quietly = TRUE)) install.packages("BiocManager")

# Split packages into CRAN vs Bioconductor
cran_pkgs <- character()
bioc_pkgs <- character()

for (pkg in pkgs) {
  available <- tryCatch({
    available.packages()[pkg, ]
  }, error = function(e) NULL)

  if (!is.null(available)) {
    cran_pkgs <- c(cran_pkgs, pkg)
  } else {
    bioc_pkgs <- c(bioc_pkgs, pkg)
  }
}

# Install CRAN packages
if (length(cran_pkgs)) {
  message("🔧 Installing CRAN packages: ", paste(cran_pkgs, collapse = ", "))
  install.packages(cran_pkgs)
}

# Install Bioconductor packages
if (length(bioc_pkgs)) {
  message("🧬 Installing Bioconductor packages: ", paste(bioc_pkgs, collapse = ", "))
  BiocManager::install(bioc_pkgs, ask = FALSE, update = FALSE)
}

install.packages("knitr")
install.packages("rmarkdown")

# Snapshot environment
renv::snapshot()

message("✅ renv.lock created. You're ready to go!")

