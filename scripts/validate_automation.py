#!/usr/bin/env python3
"""Validate the public ChatGPT/Hermes handoff queue without third-party packages."""

from __future__ import annotations

import json
import re
import sys
from datetime import datetime
from pathlib import Path
from urllib.parse import urlparse


ROOT = Path(__file__).resolve().parents[1]
TASKS = ROOT / "automation" / "tasks"
RESULTS = ROOT / "automation" / "results"
TASK_ID = re.compile(r"^BW-[0-9]{4}-[0-9]{4}$")
COMMIT = re.compile(r"^[0-9a-f]{7,40}$")
BRANCH = re.compile(r"^agent/[A-Za-z0-9._/-]+$")
ABSOLUTE = re.compile(r"^(?:/|~(?:/|$)|file://|[A-Za-z]:[\\/])")
TASK_STATUSES = {"READY", "CLAIMED", "BLOCKED", "SUBMITTED", "ACCEPTED", "REJECTED"}
RESULT_STATUSES = {"BLOCKED", "SUBMITTED"}
INPUT_KINDS = {"GITHUB", "CURATED_LIBRARY", "WIX", "DECISION"}
ACCESS = {"READ_ONLY", "READ_WRITE"}


def error(errors: list[str], path: Path, message: str) -> None:
    errors.append(f"{path.relative_to(ROOT)}: {message}")


def load(path: Path, errors: list[str]) -> dict | None:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        error(errors, path, f"invalid JSON: {exc}")
        return None
    if not isinstance(value, dict):
        error(errors, path, "top level must be an object")
        return None
    return value


def strings(value: object):
    if isinstance(value, str):
        yield value
    elif isinstance(value, dict):
        for item in value.values():
            yield from strings(item)
    elif isinstance(value, list):
        for item in value:
            yield from strings(item)


def common(path: Path, value: dict, errors: list[str]) -> None:
    for item in strings(value):
        if ABSOLUTE.match(item):
            error(errors, path, f"must not contain local absolute paths: {item!r}")


def valid_datetime(value: object) -> bool:
    if not isinstance(value, str):
        return False
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return False
    return parsed.tzinfo is not None


def validate_task(path: Path, task: dict, errors: list[str]) -> str | None:
    required = {"task_id", "project_id", "issued_at", "status", "scope", "inputs", "acceptance", "safety"}
    if set(task) != required:
        error(errors, path, f"fields must be exactly: {', '.join(sorted(required))}")
    task_id = task.get("task_id")
    if not isinstance(task_id, str) or not TASK_ID.fullmatch(task_id):
        error(errors, path, "invalid task_id")
        return None
    if path.stem != task_id:
        error(errors, path, "filename must match task_id")
    if task.get("project_id") != "P-2026-0005":
        error(errors, path, "project_id must be P-2026-0005")
    if not valid_datetime(task.get("issued_at")):
        error(errors, path, "issued_at must be a timezone-aware ISO datetime")
    if task.get("status") not in TASK_STATUSES:
        error(errors, path, "invalid task status")
    if not isinstance(task.get("scope"), str) or len(task["scope"]) < 10:
        error(errors, path, "scope must contain at least 10 characters")
    inputs = task.get("inputs")
    if not isinstance(inputs, list):
        error(errors, path, "inputs must be an array")
    else:
        for index, item in enumerate(inputs):
            if not isinstance(item, dict) or set(item) != {"kind", "location", "access"}:
                error(errors, path, f"inputs[{index}] has invalid fields")
                continue
            if item.get("kind") not in INPUT_KINDS or item.get("access") not in ACCESS:
                error(errors, path, f"inputs[{index}] has invalid kind or access")
            if not isinstance(item.get("location"), str) or not item["location"]:
                error(errors, path, f"inputs[{index}] location is required")
    acceptance = task.get("acceptance")
    if not isinstance(acceptance, list) or not acceptance or not all(isinstance(x, str) and len(x) >= 3 for x in acceptance):
        error(errors, path, "acceptance must be a non-empty string array")
    if task.get("safety") != {"nas_originals": "READ_ONLY", "direct_main_push": False, "secrets_in_repo": False}:
        error(errors, path, "safety policy is invalid")
    common(path, task, errors)
    return task_id


def validate_result(path: Path, result: dict, errors: list[str]) -> str | None:
    required = {"task_id", "completed_at", "status", "branch", "commit", "checks", "artifacts", "notes"}
    allowed = required | {"pull_request"}
    if not required.issubset(result) or not set(result).issubset(allowed):
        error(errors, path, "missing required fields or contains unknown fields")
    task_id = result.get("task_id")
    if not isinstance(task_id, str) or not TASK_ID.fullmatch(task_id):
        error(errors, path, "invalid task_id")
        return None
    if path.stem != task_id:
        error(errors, path, "filename must match task_id")
    if not valid_datetime(result.get("completed_at")):
        error(errors, path, "completed_at must be a timezone-aware ISO datetime")
    if result.get("status") not in RESULT_STATUSES:
        error(errors, path, "invalid result status")
    if not isinstance(result.get("branch"), str) or not BRANCH.fullmatch(result["branch"]):
        error(errors, path, "branch must begin with agent/")
    if not isinstance(result.get("commit"), str) or not COMMIT.fullmatch(result["commit"]):
        error(errors, path, "commit must be a 7-40 character lowercase SHA")
    pull_request = result.get("pull_request")
    if pull_request is not None:
        parsed = urlparse(pull_request) if isinstance(pull_request, str) else None
        if not parsed or parsed.scheme != "https" or parsed.netloc != "github.com":
            error(errors, path, "pull_request must be a GitHub HTTPS URL or null")
    checks = result.get("checks")
    if not isinstance(checks, list) or not all(
        isinstance(item, dict)
        and set(item) == {"name", "passed"}
        and isinstance(item["name"], str)
        and isinstance(item["passed"], bool)
        for item in checks
    ):
        error(errors, path, "checks must contain only name/passed objects")
    for field in ("artifacts", "notes"):
        if not isinstance(result.get(field), list) or not all(isinstance(item, str) for item in result[field]):
            error(errors, path, f"{field} must be a string array")
    common(path, result, errors)
    return task_id


def main() -> int:
    errors: list[str] = []
    task_ids: set[str] = set()
    result_ids: set[str] = set()
    for path in sorted(TASKS.glob("*.json")):
        value = load(path, errors)
        if value is not None:
            task_id = validate_task(path, value, errors)
            if task_id:
                if task_id in task_ids:
                    error(errors, path, "duplicate task_id")
                task_ids.add(task_id)
    for path in sorted(RESULTS.glob("*.json")):
        value = load(path, errors)
        if value is not None:
            task_id = validate_result(path, value, errors)
            if task_id:
                if task_id in result_ids:
                    error(errors, path, "duplicate result task_id")
                result_ids.add(task_id)
    for unknown in sorted(result_ids - task_ids):
        errors.append(f"automation/results/{unknown}.json: result has no matching task")
    if errors:
        print("Automation contract validation failed:")
        for message in errors:
            print(f"- {message}")
        return 1
    print(f"Automation contract validation passed: {len(task_ids)} task(s), {len(result_ids)} result(s)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
