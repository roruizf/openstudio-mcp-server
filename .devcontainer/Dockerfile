# OpenStudio MCP Server Development Container
# Based on Python 3.12 slim with OpenStudio installation

FROM python:3.12-slim

ARG TARGETPLATFORM

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    wget \
    git \
    vim \
    nano \
    build-essential \
    gnupg \
    # X11 libraries for OpenStudio
    libx11-6 \
    libxext6 \
    libxrender1 \
    libxtst6 \
    libxi6 \
    libxrandr2 \
    libxinerama1 \
    libxcursor1 \
    libglu1-mesa \
    # Additional libraries
    libssl-dev \
    libffi-dev \
    graphviz \
    && rm -rf /var/lib/apt/lists/*

# Install Node.js 20 (for MCP Inspector)
RUN curl -fsSL https://deb.nodesource.com/setup_20.x | bash - && \
    apt-get install -y nodejs && \
    rm -rf /var/lib/apt/lists/*

# Install OpenStudio
# Version and SHA can be overridden at build time
ARG OPENSTUDIO_VERSION=3.7.0
ARG OPENSTUDIO_SHA=d5269793f1

# Detect architecture and download appropriate OpenStudio package
RUN if [ "$TARGETPLATFORM" = "linux/arm64" ]; then \
        OPENSTUDIO_ARCH="arm64"; \
    else \
        OPENSTUDIO_ARCH="x86_64"; \
    fi && \
    echo "Installing OpenStudio ${OPENSTUDIO_VERSION} for ${OPENSTUDIO_ARCH}" && \
    wget -q "https://github.com/NREL/OpenStudio/releases/download/v${OPENSTUDIO_VERSION}/OpenStudio-${OPENSTUDIO_VERSION}+${OPENSTUDIO_SHA}-Ubuntu-20.04-${OPENSTUDIO_ARCH}.deb" && \
    dpkg -i OpenStudio-*.deb || apt-get install -f -y && \
    rm OpenStudio-*.deb

# Set OpenStudio environment variables
ENV OPENSTUDIO_VERSION=${OPENSTUDIO_VERSION}
ENV OPENSTUDIO_PATH=/usr/local/openstudio-${OPENSTUDIO_VERSION}
ENV PATH="${OPENSTUDIO_PATH}/bin:${PATH}"
ENV RUBYLIB="${OPENSTUDIO_PATH}/Ruby"
ENV PYTHONPATH="${OPENSTUDIO_PATH}/Python:${PYTHONPATH}"

# Install uv package manager
RUN pip install --no-cache-dir uv

# Install OpenStudio Python bindings
# This is critical for the MCP server tools to work
RUN pip install --no-cache-dir openstudio==${OPENSTUDIO_VERSION}

# Create non-root user for development
RUN useradd -m -s /bin/bash vscode && \
    mkdir -p /workspace && \
    chown -R vscode:vscode /workspace

# Set working directory
WORKDIR /workspace/openstudio-mcp-server

# Switch to non-root user
USER vscode

# Default command
CMD ["/bin/bash"]
