# -----------------------------------------------
# Base OS
# -----------------------------------------------
FROM debian:bookworm

LABEL maintainer="SeqInfOmics <cud2td@virginia.edu>" \
      description="Quarto + R(4.4.3/Bioc 3.20) + Python env for DiffEx QMDs"

# -----------------------------------------------
# System dependencies (headers & tools + locale)
# -----------------------------------------------
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl wget git unzip ca-certificates \
    pandoc \
    build-essential gfortran pkg-config cmake make \
    libcurl4-openssl-dev libssl-dev libxml2-dev \
    zlib1g-dev libbz2-dev liblzma-dev libzstd-dev libpcre2-dev \
    libcairo2-dev libpng-dev libjpeg-dev libtiff5-dev \
    libfreetype6-dev libfontconfig1-dev libharfbuzz-dev libfribidi-dev \
    libglpk40 libglpk-dev locales \
 && sed -i '/en_US.UTF-8/s/^# //g' /etc/locale.gen \
 && locale-gen en_US.UTF-8 \
 && update-locale LANG=en_US.UTF-8 \
 && rm -rf /var/lib/apt/lists/* && update-ca-certificates

ENV LANG=en_US.UTF-8
ENV LC_ALL=en_US.UTF-8

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
# Micromamba (conda-compatible)
# -----------------------------------------------
SHELL ["/bin/bash", "-lc"]
ENV MAMBA_ROOT_PREFIX=/opt/micromamba
RUN curl -Ls https://micro.mamba.pm/api/micromamba/linux-64/latest | tar -xvj -C /usr/local/bin bin/micromamba --strip-components=1

# -----------------------------------------------
# Environment setup
# -----------------------------------------------
WORKDIR /app
COPY environment.yaml /app/environment.yaml

# Create the conda env
RUN micromamba create -y -n diffex-env -f /app/environment.yaml && \
    micromamba clean -a -y
ENV PATH=/opt/micromamba/envs/diffex-env/bin:$PATH

# -----------------------------------------------
# Install R + key system-independent pkgs via conda
# -----------------------------------------------
RUN micromamba install -y -n diffex-env -c conda-forge \
    r-base=4.4.3 r-biocmanager r-renv r-devtools \
    r-rlang r-glue r-dplyr \
    compilers pkg-config \
    zlib bzip2 xz zstd lz4-c freetype fontconfig harfbuzz fribidi \
    libxml2 libcurl openssl && \
    micromamba clean -a -y

# -----------------------------------------------
# Clone and install DiffEx
# -----------------------------------------------
RUN git clone --branch main --single-branch https://github.com/dremellab/DiffEx.git /app/DiffEx && \
    micromamba run -n diffex-env pip install -e /app/DiffEx

WORKDIR /app/DiffEx

# -----------------------------------------------
# Install R dependencies (choose ONE method)
# -----------------------------------------------
# Option 1: If install_R_packages.R already installs everything needed, use it:
# COPY diffex/install_R_packages.R /opt/install_R_packages.R
# RUN micromamba run -n diffex-env Rscript /opt/install_R_packages.R

# Option 2: (better) Use renv to reproduce exactly your local R environment:
RUN micromamba run -n diffex-env Rscript -e 'renv::restore(prompt = FALSE)'
RUN micromamba run -n diffex-env Rscript -e 'renv::repair(); renv::snapshot(prompt = FALSE)'
# -----------------------------------------------
# Final environment settings
# -----------------------------------------------
ENV RENV_CONFIG_INSTALL_FROM_SOURCE=true \
    RENV_CONFIG_USE_CACHE=false

CMD ["/bin/bash"]
