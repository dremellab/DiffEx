# First, activate renv
source("renv/activate.R")

# Then, override repository URLs *after* renv/BiocManager load
setHook(
  packageEvent("renv", "onLoad"),
  function(...) {
    options(repos = BiocManager::repositories(
      replace = TRUE,
      CRAN = "https://packagemanager.posit.co/cran/__linux__/bookworm/2025-09-01"
    ))
  }
)

