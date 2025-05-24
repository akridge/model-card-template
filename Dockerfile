# Dockerfile
FROM ghcr.io/quarto-dev/quarto:latest

ENV DEBIAN_FRONTEND=noninteractive \
    TINYTEX_DIR=/root/.TinyTeX \
    PATH=/root/.TinyTeX/bin/x86_64-linux:$PATH

USER root

# Install system dependencies and TinyTeX
RUN apt-get update \
  && apt-get install -y --no-install-recommends \
       fonts-liberation \
       make \
       git \
       perl \
       cpanminus \
  && rm -rf /var/lib/apt/lists/* \
  && cpanm --no-wget File::Find \
  && quarto install tool tinytex --no-prompt \
  && tlmgr update --self \
  && tlmgr install \
       collection-basic \
       collection-latexrecommended

WORKDIR /home/quarto/project
COPY . /home/quarto/project

# Default to rendering PDF
ENTRYPOINT ["quarto", "render"]
CMD ["model_card_modern.qmd", "--to", "pdf"]
