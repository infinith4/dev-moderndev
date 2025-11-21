FROM mcr.microsoft.com/devcontainers/base:ubuntu-24.04

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        graphviz \
        fonts-ipafont \
        ca-certificates \
        curl \
        unzip \
        fonts-noto-cjk \
        fonts-noto-cjk-extra \
        fontconfig \
        chromium \
        libgbm1 \
        libnss3 \
        libatk-bridge2.0-0 \
        libgtk-3-0 \
        libxss1 \
    && fc-cache -fv \
    && apt install -y openjdk-21-jdk \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*
