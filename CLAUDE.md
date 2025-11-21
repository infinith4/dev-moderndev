# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Overview

This is a DevContainer-based development environment template optimized for documentation work, particularly markdown editing and PDF generation with Japanese font support. The environment runs in a containerized Ubuntu 24.04 setup with Python, Node.js, Docker-in-Docker, and Git/GitHub CLI.

## DevContainer Configuration System

This repository uses a dynamic configuration system where DevContainer and Docker Compose settings are managed via environment variables.

### Configuration Files

- `.env.devcontainer` - Central configuration file containing:
  - `DEVCONTAINER_NAME` - DevContainer display name
  - `SERVICE_NAME` - Docker Compose service name
  - `CONTAINER_NAME` - Docker container name

- `setup-devcontainer.ps1` - PowerShell script that applies environment variables to:
  - `.devcontainer/devcontainer.json` (name and service fields)
  - `docker-compose.yml` (service name and container_name)

### Applying Configuration Changes

To update DevContainer settings:

```powershell
./setup-devcontainer.ps1
```

After running the script, rebuild the DevContainer in VSCode:
- Command Palette → "Dev Containers: Rebuild Container"

### Custom file paths (if needed):

```powershell
./setup-devcontainer.ps1 `
    -EnvFile ".env.devcontainer" `
    -DevContainerPath ".devcontainer/devcontainer.json" `
    -DockerComposePath "docker-compose.yml"
```

## Container Architecture

**Base Image:** `mcr.microsoft.com/devcontainers/base:ubuntu-24.04`

**Key Dependencies:**
- Graphviz - For diagram generation
- Chromium/Google Chrome - For markdown-preview-enhanced PDF export
- Japanese fonts (fonts-ipafont, fonts-noto-cjk) - For PDF generation with Japanese text
- OpenJDK 21 - Java runtime
- Python, Node.js (via DevContainer features)

**Container Setup:**
- Workspace mounted at `/src` in container
- Runs as `vscode` user
- Timezone: Asia/Tokyo
- Post-creation script: `.devcontainer/setup.sh` (installs Google Chrome and Japanese fonts)

## VSCode Extensions

Pre-installed extensions:
- `ms-python.python` / `ms-python.pylint` - Python development
- `shd101wyy.markdown-preview-enhanced` - Advanced markdown preview with PDF export
- `yzhang.markdown-all-in-one` - Markdown editing utilities
- `mitchdenny.ecdc` - EditorConfig support
- `ms-azuretools.vscode-containers` / `ms-azuretools.vscode-docker` - Container management
- `Anthropic.claude-code` - Claude Code integration

## Markdown Preview Configuration

The repository is configured for markdown-preview-enhanced with:
- Chromium as PDF rendering engine
- GitHub Light theme for previews
- Print background enabled for PDF export
- Japanese font support via Noto CJK fonts
- Puppeteer arguments configured for headless rendering in container

## Project Structure

```
.
├── .devcontainer/          # DevContainer configuration
│   ├── devcontainer.json   # Container settings (managed by setup script)
│   └── setup.sh            # Post-create setup script
├── .env.devcontainer       # Environment variables for DevContainer config
├── docker-compose.yml      # Docker Compose service definition (managed by setup script)
├── Dockerfile              # Container image definition
├── setup-devcontainer.ps1  # Configuration management script
├── docs/                   # Documentation directory
├── PROJECT_V1/             # Project-specific tasks and documentation
└── README_DEVCONTAINER.md  # DevContainer configuration guide (Japanese)
```

## Important Notes

- The service name in `docker-compose.yml` must match the service name in `devcontainer.json`
- Always use the PowerShell script to update configuration - manual edits may be overwritten
- The container includes Docker-in-Docker capability for nested container operations
- Font rendering in PDFs requires the Noto CJK fonts to be properly cached (`fc-cache -fv`)
