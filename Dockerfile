# Use Quarto's official image as base
FROM ghcr.io/quarto-dev/quarto:latest

# Set environment variables
ENV DEBIAN_FRONTEND=noninteractive
ENV TINYTEX_DIR=/root/.TinyTeX
ENV PATH="${TINYTEX_DIR}/bin/x86_64-linux:${PATH}"

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    fonts-liberation \
    make \
    git \
    perl \
    perl-modules \
    cpanminus \
    && rm -rf /var/lib/apt/lists/*

# Install Perl modules
RUN cpanm --no-wget File::Find

# Install TinyTeX and required packages
RUN quarto install tool tinytex --no-prompt \
    && tlmgr update --self \
    && tlmgr install \
        collection-basic \
        collection-latex \
        collection-fontsrecommended \
        collection-latexrecommended \
        geometry \
        fancyhdr \
        xcolor \
        tcolorbox \
        fontspec

# Install Quarto extensions
RUN quarto install extension quarto-journals/elsevier --no-prompt

# Set working directory
WORKDIR /workspace

# Default command
CMD ["quarto", "render", "--to", "pdf"]
