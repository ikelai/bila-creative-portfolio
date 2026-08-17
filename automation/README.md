# BILA Website automation contract

GitHub is the shared handoff layer for project `P-2026-0005`.

- ChatGPT issues one task JSON that conforms to `task.schema.json`.
- Hermes works only on an `agent/*` branch and never pushes directly to `main`.
- Hermes returns one result JSON that conforms to `result.schema.json`, then opens a pull request.
- CI must pass before ChatGPT accepts or merges the result.
- NAS originals remain read-only. Only curated, website-approved exports may enter this repository.
- Secrets, local absolute paths, quotation data, costs and client approval records never enter this public repository.

Sensitive task state belongs in a separate private operations repository. This public directory contains only the protocol needed by workers and CI.
