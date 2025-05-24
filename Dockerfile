# 1) Base image with Quarto pre-installed
FROM ghcr.io/quarto-dev/quarto:latest

ENV DEBIAN_FRONTEND=noninteractive \
    TINYTEX_DIR=/root/.TinyTeX \
    PATH=/root/.TinyTeX/bin/x86_64-linux:$PATH

USER root

# 2) Install system deps + Perl + TinyTeX
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

# 3) Copy your entire project into the container
WORKDIR /home/quarto/project
COPY . /home/quarto/project

# 4) Default command: render your QMD → PDF
ENTRYPOINT ["quarto", "render"]
CMD ["model_card_modern.qmd", "--to", "pdf"]
