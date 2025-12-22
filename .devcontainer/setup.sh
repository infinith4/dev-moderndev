#!/bin/bash
set -e

# Update package lists and install dependencies
sudo apt-get update

# Install Google Chrome for Puppeteer (markdown-preview-enhanced)
wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | sudo apt-key add -
sudo sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list'
sudo apt-get update
sudo apt-get install -y google-chrome-stable

# Install Japanese fonts for PDF generation
sudo apt-get install -y fonts-noto-cjk fonts-noto-cjk-extra fontconfig

# Refresh font cache
sudo fc-cache -fv

# Clean up
sudo apt-get clean
sudo rm -rf /var/lib/apt/lists/*

# 2. PlantUMLのJARファイルをダウンロードして配置
# (ここでは /usr/local/bin/plantuml.jar に配置します)
curl -OL https://github.com/plantuml/plantuml/releases/download/v1.2025.7/plantuml-mit-1.2025.7.jar
sudo mv plantuml-mit-1.2025.7.jar /usr/local/bin/plantuml.jar

# 3. Install @openai/codex globally
npm install -g @openai/codex

echo "Dev Container setup completed!"