#!/usr/bin/env python3
"""Dependency-free integrity checks for the BILA static website."""

from __future__ import annotations

import csv
import json
import re
import sys
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit


ROOT = Path(__file__).resolve().parents[1]
GENERATED_CASES = ROOT / "data" / "cases.json"
MANIFEST = ROOT / "images" / "IMAGE_MANIFEST.csv"
EXTERNAL_SCHEMES = ("http", "https", "mailto", "tel", "data", "javascript")
REQUIRED_CASE_FIELDS = {"name", "zh", "kicker", "role", "hero", "summary", "meta", "gallery", "credit"}
REQUIRED_META_FIELDS = {"Client", "Scope", "Scale"}
LEGACY_CLASSES = {"top-bar", "hero", "hero-content", "section", "work-grid", "work-card", "cta-band", "site-foot", "manifesto"}


class DocumentParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.references: list[tuple[str, str]] = []
        self.classes: set[str] = set()
        self.images_without_alt = 0
        self.title_depth = 0
        self.title_text: list[str] = []
        self.description = False

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        values = dict(attrs)
        for attr in ("href", "src"):
            if values.get(attr):
                self.references.append((attr, values[attr] or ""))
        self.classes.update((values.get("class") or "").split())
        if tag == "img" and "alt" not in values:
            self.images_without_alt += 1
        if tag == "title":
            self.title_depth += 1
        if tag == "meta" and (values.get("name") or "").lower() == "description" and values.get("content"):
            self.description = True

    def handle_endtag(self, tag: str) -> None:
        if tag == "title":
            self.title_depth = max(0, self.title_depth - 1)

    def handle_data(self, data: str) -> None:
        if self.title_depth:
            self.title_text.append(data.strip())


def fail(errors: list[str], message: str) -> None:
    errors.append(message)


def resolve_reference(document: Path, value: str) -> Path | None:
    parsed = urlsplit(value)
    if parsed.scheme.lower() in EXTERNAL_SCHEMES or value.startswith("//"):
        return None
    clean = unquote(parsed.path)
    if not clean:
        return None
    return (document.parent / clean).resolve()


def check_cases(errors: list[str]) -> dict[str, dict]:
    try:
        cases = json.loads(GENERATED_CASES.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        fail(errors, f"data/cases.json cannot be read: {exc}")
        return {}

    if not isinstance(cases, dict) or not cases:
        fail(errors, "data/cases.json must be a non-empty object")
        return {}

    for slug, case in cases.items():
        if not re.fullmatch(r"[a-z0-9-]+", slug):
            fail(errors, f"case slug is unsafe: {slug!r}")
        if not isinstance(case, dict):
            fail(errors, f"case {slug} must be an object")
            continue
        missing = sorted(REQUIRED_CASE_FIELDS - set(case))
        if missing:
            fail(errors, f"case {slug} missing fields: {', '.join(missing)}")
        meta = case.get("meta", {})
        if not isinstance(meta, dict) or REQUIRED_META_FIELDS - set(meta):
            fail(errors, f"case {slug} meta must contain Client, Scope and Scale")
        galleries = list(case.get("gallery") or [])
        for section in case.get("brand_sections") or []:
            galleries.extend(section.get("images") or section.get("gallery") or [])
        for label, image in [("hero", case.get("hero")), *[("gallery", item) for item in galleries]]:
            if not isinstance(image, str) or not image.startswith("images/"):
                fail(errors, f"case {slug} has invalid {label} path: {image!r}")
            elif not (ROOT / image).is_file():
                fail(errors, f"case {slug} references missing image: {image}")
        if not (ROOT / "work" / f"{slug}.html").is_file():
            fail(errors, f"case {slug} has no work/{slug}.html page")
    return cases


def check_html(errors: list[str]) -> None:
    styles = (ROOT / "assets" / "style.css").read_text(encoding="utf-8")
    for document in sorted(ROOT.rglob("*.html")):
        parser = DocumentParser()
        parser.feed(document.read_text(encoding="utf-8"))
        rel = document.relative_to(ROOT)
        if not "".join(parser.title_text).strip():
            fail(errors, f"{rel}: missing document title")
        if not parser.description:
            fail(errors, f"{rel}: missing meta description")
        if not any(value.endswith("favicon.svg") for attr, value in parser.references if attr == "href"):
            fail(errors, f"{rel}: missing SVG favicon link")
        if parser.images_without_alt:
            fail(errors, f"{rel}: {parser.images_without_alt} image(s) missing alt attributes")
        for _, value in parser.references:
            target = resolve_reference(document, value)
            if target is not None and (ROOT not in target.parents and target != ROOT):
                fail(errors, f"{rel}: reference escapes repository: {value}")
            elif target is not None and not target.exists():
                fail(errors, f"{rel}: broken local reference: {value}")
        used_legacy = sorted(parser.classes & LEGACY_CLASSES)
        missing_css = [name for name in used_legacy if f".{name}" not in styles]
        if missing_css:
            fail(errors, f"{rel}: uses legacy classes absent from CSS: {', '.join(missing_css)}")


def check_manifest(errors: list[str]) -> None:
    try:
        with MANIFEST.open(encoding="utf-8-sig", newline="") as stream:
            rows = list(csv.DictReader(stream))
    except OSError as exc:
        fail(errors, f"images/IMAGE_MANIFEST.csv cannot be read: {exc}")
        return
    for number, row in enumerate(rows, 2):
        output = row.get("out", "")
        source = row.get("src", "")
        if source:
            fail(errors, f"image manifest row {number} exposes a source path")
        if not output or not (ROOT / output).is_file():
            fail(errors, f"image manifest row {number} references missing output: {output!r}")


def check_repository_safety(errors: list[str]) -> None:
    forbidden = {".ai", ".psd", ".indd", ".zip", ".7z", ".rar"}
    for path in ROOT.rglob("*"):
        if ".git" in path.parts:
            continue
        if path.is_file() and path.suffix.lower() in forbidden:
            fail(errors, f"source/archive file must not be published: {path.relative_to(ROOT)}")
    if not (ROOT / "favicon.svg").is_file():
        fail(errors, "favicon.svg is missing")


def main() -> int:
    errors: list[str] = []
    cases = check_cases(errors)
    check_html(errors)
    check_manifest(errors)
    check_repository_safety(errors)
    if errors:
        print("BILA website validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1
    print(f"BILA website validation passed: {len(cases)} cases, {len(list(ROOT.rglob('*.html')))} HTML pages")
    return 0


if __name__ == "__main__":
    sys.exit(main())
