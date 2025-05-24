# Dockerfile
FROM ghcr.io/quarto-dev/quarto:latest

# 1) Install system dependencies
USER root
RUN apt-get update \
  && apt-get install -y --no-install-recommends \
       fonts-liberation \
       make \
       git \
       perl \
       curl \
       xz-utils \
  && rm -rf /var/lib/apt/lists/*

# 2) Install TinyTeX via Quarto and update/install core TeX Live collections
RUN quarto install tool tinytex --no-prompt \
  && tlmgr update --self --all \
  && tlmgr install \
       collection-basic \
       collection-latexrecommended

# 3) Copy your project in and set working dir
WORKDIR /home/quarto/project
COPY . /home/quarto/project

# 4) Default entrypoint to render PDF
ENTRYPOINT ["quarto", "render"]
CMD ["model_card_modern.qmd", "--to", "pdf"]
