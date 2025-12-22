# Repository Guidelines

## Project Structure & Module Organization
- `docs/` hosts the working content: stage guides follow `dev_process_開発工程_<番号>_フェーズ名.md`; tool guides live under `docs/ツール/<カテゴリ>/<ツール名>.md`; `docs/ツール索引.md` is the top-level index.
- `PROJECT_V1/` retains the previous document set for reference; avoid editing unless explicitly migrating content.
- Root Python utilities (`generate_tools_list.py`, `update_tool_links.py`, `migrate_tool_categories.py`) help keep tool indices and paths consistent.
- Dev environment assets sit in `.devcontainer/`, `docker-compose.yml`, and `Dockerfile`; GitHub workflow/PDF helpers are under `.github/`.

## Build, Test, and Development Commands
- Refresh tool listings after adding or moving tool docs: `python3 generate_tools_list.py`.
- Update legacy category links after reorganizing files: `python3 update_tool_links.py`.
- Apply category-wide moves with mapping rules: `python3 migrate_tool_categories.py`.
- Sync DevContainer names/services from `.env.devcontainer`: `./setup-devcontainer.ps1` (PowerShell).

## Coding Style & Naming Conventions
- Markdown only; one `#` title per file that matches the doc purpose. Use `##`/`###` for structure and tables for matrices (工程×ツールなど).
- File naming: keep existing patterns (`dev_process_開発工程_<番号>_...`, `ツール/<カテゴリ>/<Tool>.md`); prefer ASCII for tool filenames and UTF-8 content for Japanese text.
- Links should be relative (e.g., `./docs/ツール/...`), and reuse the shared sections shown in `TASKS.md` (概要→料金→メリデメ→活用工程→公式ドキュメント).
- Keep tone instructional and concise; avoid marketing language.

## Testing Guidelines
- No automated test suite. Validate by opening Markdown previews and checking tables render correctly.
- After restructuring tools, rerun the scripts above and confirm generated files are staged. Spot-check a few links (especially `docs/ツール索引.md` and stage guides) for 404s.
- If producing PDFs via GitHub Actions, ensure diagrams and non-ASCII fonts render (fonts are installed in the provided Dockerfile).

## Commit & Pull Request Guidelines
- Commits: short, imperative, and scoped (e.g., `Add Prometheus tool guide`, `Update 要件定義 links`). Group related doc edits together.
- PRs: include a brief summary, the affected paths, before/after notes for renamed files, and the commands you ran (script outputs if applicable). Link related issues/tasks and attach screenshots for structural layout changes.
- Mention whether `generate_tools_list.py` or other scripts were rerun so reviewers know what is auto-generated.

## Security & Configuration Tips
- Do not commit secrets to `.env.devcontainer` or example snippets; sanitize URLs and API keys in tool guides.
- When adding third-party references, prefer official docs; mark paid features clearly to avoid misleading readers.
