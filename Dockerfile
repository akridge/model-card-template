# Dockerfile
FROM ghcr.io/quarto-dev/quarto:latest

# 1) Make sure we install required system tools
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

# 2) Install TinyTeX via Quarto and add it to the PATH
RUN quarto install tool tinytex --no-prompt --update-path

# 3) Now tlmgr is on PATH—update itself and install core collections
RUN tlmgr update --self --all \
  && tlmgr install \
       collection-basic \
       collection-latexrecommended

# 4) Copy in your project
WORKDIR /home/quarto/project
COPY . /home/quarto/project

# 5) Default: render your QMD → PDF
ENTRYPOINT ["quarto", "render"]
CMD ["model_card_modern.qmd", "--to", "pdf"]
