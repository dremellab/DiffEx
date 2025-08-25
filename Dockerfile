# Start from a base image with conda (Miniconda3)
FROM continuumio/miniconda3:24.1.2-0

# Metadata
LABEL maintainer="Your Name <you@example.com>" \
      description="Docker image with Quarto CLI and diffex_env"

# Install system deps
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    wget \
    git \
    unzip \
    pandoc \
    && rm -rf /var/lib/apt/lists/*

# --------------------------------------------------
# Install Quarto CLI (pick version you need)
# --------------------------------------------------
ENV QUARTO_VERSION=1.4.550

RUN curl -L -o quarto.tar.gz \
      https://github.com/quarto-dev/quarto-cli/releases/download/v${QUARTO_VERSION}/quarto-${QUARTO_VERSION}-linux-amd64.tar.gz \
    && tar -xvzf quarto.tar.gz \
    && mv quarto-${QUARTO_VERSION} /opt/quarto \
    && ln -s /opt/quarto/bin/quarto /usr/local/bin/quarto \
    && rm quarto.tar.gz

# Verify installation
RUN quarto --version

# --------------------------------------------------
# Create diffex_env from environment.yaml
# (copy your environment.yaml into the container)
# --------------------------------------------------
WORKDIR /app
COPY environment.yaml /app/environment.yaml

RUN conda env create -f environment.yaml && conda clean -afy

# --------------------------------------------------
# Install DiffEx from GitHub source
# --------------------------------------------------
RUN git clone --branch dev --single-branch https://github.com/dremellab/DiffEx.git /app/DiffEx && \
    /opt/conda/envs/diffex-env/bin/pip install -e /app/DiffEx

# Make conda activate work in bash
SHELL ["/bin/bash", "--login", "-c"]

# Activate environment by default
ENV PATH=/opt/conda/envs/diffex-env/bin:$PATH

# --------------------------------------------------
# Set entrypoint
# --------------------------------------------------
ENTRYPOINT ["/bin/bash"]

