# Base OS (no conda here)
FROM debian:bookworm

LABEL maintainer="SeqInfOmics <cud2td@virginia.edu>" \
      description="Quarto + R(4.4.3/Bioc 3.20) + Python env for DiffEx QMDs"

# -----------------------------------------------
# System dependencies (headers & tools)
# -----------------------------------------------
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl wget git unzip ca-certificates \
    pandoc \
    build-essential gfortran pkg-config cmake \
    libcurl4-openssl-dev libssl-dev libxml2-dev \
    zlib1g-dev libbz2-dev liblzma-dev libzstd-dev libpcre2-dev \
    libcairo2-dev libpng-dev libjpeg-dev libtiff5-dev \
    libfreetype6-dev libfontconfig1-dev libharfbuzz-dev libfribidi-dev \
    libglpk40 libglpk-dev \
 && rm -rf /var/lib/apt/lists/* && update-ca-certificates

# -----------------------------------------------
# Quarto CLI
# -----------------------------------------------
ENV QUARTO_VERSION=1.4.550
RUN curl -L -o /tmp/quarto.tar.gz \
      https://github.com/quarto-dev/quarto-cli/releases/download/v${QUARTO_VERSION}/quarto-${QUARTO_VERSION}-linux-amd64.tar.gz \
 && tar -xzf /tmp/quarto.tar.gz -C /opt \
 && ln -s /opt/quarto-${QUARTO_VERSION}/bin/quarto /usr/local/bin/quarto \
 && rm /tmp/quarto.tar.gz
RUN quarto --version

# -----------------------------------------------
# Micromamba (conda-compatible) + create env
# -----------------------------------------------
SHELL ["/bin/bash", "-lc"]
ENV MAMBA_ROOT_PREFIX=/opt/micromamba

RUN curl -Ls https://micro.mamba.pm/api/micromamba/linux-64/latest \
  | tar -xvj -C /usr/local/bin bin/micromamba --strip-components=1

WORKDIR /app
COPY environment.yaml /app/environment.yaml

# Create env from your YAML (name should be diffex-env inside the YAML)
RUN rm -f /opt/micromamba/pkgs/*.lock && \
    micromamba create -y -n diffex-env -f /app/environment.yaml && \
    micromamba clean -a -y

# Put env on PATH (no need to "activate" in Docker)
ENV PATH=/opt/micromamba/envs/diffex-env/bin:$PATH

# -----------------------------------------------
# R + key R pkgs via conda-forge inside the env
# (avoid compiling the usual suspects)
# -----------------------------------------------
RUN rm -f /opt/micromamba/pkgs/*.lock && \
    micromamba install -y -n diffex-env -c conda-forge \
        r-base=4.4.3 r-biocmanager r-renv r-devtools \
        compilers make pkg-config \
        zlib bzip2 xz zstd lz4-c \
        freetype fontconfig harfbuzz fribidi \
        libxml2 libcurl openssl \
        r-rlang \
    && micromamba clean -a -y

# -----------------------------------------------
# DiffEx (main) + Python package install
# -----------------------------------------------
RUN git clone --branch main --single-branch https://github.com/dremellab/DiffEx.git /app/DiffEx && \
    micromamba run -n diffex-env pip install -e /app/DiffEx

# Optional environment checks
WORKDIR /app/DiffEx
ENV RENV_CONFIG_INSTALL_FROM_SOURCE=true \
    RENV_CONFIG_USE_CACHE=false

# ---- Add and run R installer script ----
COPY diffex/install_R_packages.R /opt/install_R_packages.R
RUN micromamba run -n diffex-env Rscript /opt/install_R_packages.R
