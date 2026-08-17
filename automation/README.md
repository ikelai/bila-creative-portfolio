# BILA Website automation contract

GitHub is the shared handoff layer for project `P-2026-0005`.

## Queue layout

- `tasks/BW-YYYY-NNNN.json`: public, non-sensitive work issued by ChatGPT.
- `results/BW-YYYY-NNNN.json`: machine-readable Hermes result for the matching task.
- `task.schema.json` and `result.schema.json`: canonical field contracts.
- `scripts/validate_automation.py`: dependency-free CI enforcement for queue files.

## Worker flow

1. Read `automation/tasks/` and select the oldest task with `status: READY`.
2. Work only on `agent/<task-id>-<description>`; never push directly to `main`.
3. Respect every acceptance and safety rule in the task.
4. Write exactly one matching result file under `automation/results/`.
5. Run the website and automation validators, then open a pull request.
6. ChatGPT reviews CI and the artifacts before accepting or merging the result.

The first queue item is deliberately a read-only repository health check. It proves the handoff path without requiring NAS, Wix, LINE, credentials, or unpublished client material.

## Safety boundary

- NAS originals remain read-only. Only curated, website-approved exports may enter this repository.
- Secrets, local absolute paths, quotation data, costs and client approval records never enter this public repository.
- Sensitive task state belongs in a separate private operations repository.
- A worker must report `BLOCKED` instead of expanding permissions or scope.
