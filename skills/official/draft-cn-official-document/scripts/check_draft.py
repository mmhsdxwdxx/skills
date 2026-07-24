#!/usr/bin/env python3
"""Content preflight for a drafted Chinese official-document JSON.

Checks structure deterministically: schema shape, document-type validity,
document-number brackets, direction rules (请示 single principal recipient;
报告 must not embed a request), date zero-padding, heading-level order, and
required metadata. Jurisdiction, policy currency, and consultation completeness
are not checkable here—walk the §5 checklist in references/ for those.

Usage: python scripts/check_draft.py draft.json [--strict]
Exit code: 0 when no errors (warnings alone pass unless --strict).
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any

FORMATS = {"general", "upward", "letter", "order", "minutes"}
TYPES = {
    "决议", "决定", "命令（令）", "命令", "令", "公报", "公告", "通告",
    "意见", "通知", "通报", "报告", "请示", "批复", "议案", "函", "纪要",
}
# Phrases that ask for approval/instruction; a 报告 must not contain them.
REQUEST_PHRASES = [
    "请批示", "请批复", "请予批准", "请审批", "请研究批复",
    "妥否，请", "妥否,请", "恳请", "请求批准", "请予审批",
]
LEVEL = {"h1": 1, "h2": 2, "h3": 3, "h4": 4}


def text_of(body: Any) -> str:
    if isinstance(body, str):
        return body
    out: list[str] = []
    if isinstance(body, list):
        for block in body:
            if isinstance(block, dict):
                out.append(str(block.get("text", "")))
            else:
                out.append(str(block))
    return "\n".join(out)


def principal_recipient_count(recipients: str) -> int:
    # Top-level recipient bodies separated by ， or 、 ; nested collectives count once.
    return len([r for r in re.split(r"[，、]", recipients) if r.strip()])


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("draft", type=Path, help="Drafted JSON file")
    parser.add_argument("--strict", action="store_true", help="Treat warnings as errors")
    parser.add_argument("--report", type=Path, help="Write the JSON report to a file")
    args = parser.parse_args()

    errors: list[str] = []
    warnings: list[str] = []

    try:
        data = json.loads(args.draft.read_text(encoding="utf-8"))
    except FileNotFoundError:
        print(f"error: file not found: {args.draft}", file=sys.stderr)
        return 2
    except json.JSONDecodeError as exc:
        print(f"error: invalid JSON in {args.draft}: {exc}", file=sys.stderr)
        return 2
    if not isinstance(data, dict):
        print(f"error: top-level JSON must be an object, got {type(data).__name__}", file=sys.stderr)
        return 2

    fmt = str(data.get("format", "")).lower()
    if not fmt:
        warnings.append("Missing 'format'; the renderer defaults to 'general'.")
    elif fmt not in FORMATS:
        errors.append(f"'format' must be one of {sorted(FORMATS)}, got {fmt!r}.")

    doc_type = str(data.get("document_type", "")).strip()
    if doc_type and doc_type not in TYPES:
        warnings.append(f"'document_type' {doc_type!r} is not one of the fifteen official types.")

    title = str(data.get("title", "")).strip()
    if not title:
        warnings.append("Missing 'title'.")
    authority = str(data.get("issuing_authority", "")).strip()
    if not authority:
        warnings.append("Missing 'issuing_authority'.")

    number = str(data.get("document_number", "")).strip()
    if number:
        if "〔" not in number or "〕" not in number:
            warnings.append(f"'document_number' should use 〔〕 brackets; got {number!r}.")
        if re.search(r"[\[\]【】]", number):
            warnings.append(f"'document_number' uses non-standard brackets; use 〔〕: {number!r}.")
        if "第" in number:
            warnings.append("'document_number' should not contain '第'; the sequence is not zero-padded.")

    # Direction rules.
    is_request = doc_type == "请示" or "请示" in title
    is_report = doc_type == "报告" or ("报告" in title and not is_request)
    recipients = str(data.get("recipients", "")).strip()
    if fmt == "upward" and not (data.get("signers") or []):
        warnings.append("Upward documents require signer name(s) ('signers').")
    if is_request:
        if not recipients:
            warnings.append("A 请示 needs a principal recipient ('recipients').")
        elif principal_recipient_count(recipients) > 1:
            warnings.append("A 请示 should have one principal recipient; found multiple in 'recipients'.")
    if is_report:
        body_text = text_of(data.get("body"))
        hits = [p for p in REQUEST_PHRASES if p in body_text]
        if hits:
            warnings.append(f"A 报告 must not embed a request for approval, but found: {hits}.")

    # Date zero-padding.
    for field in ("date", "printing_date"):
        value = str(data.get(field, "")).strip()
        if not value:
            continue
        if re.search(r"年0[1-9]月", value) or re.search(r"月0[1-9]日", value):
            warnings.append(f"'{field}' has a zero-padded month or day; use full Arabic without padding: {value!r}.")

    # Heading-level order: deepening must step by exactly one level.
    body = data.get("body")
    if isinstance(body, list):
        prev = 0
        for index, block in enumerate(body, start=1):
            if not isinstance(block, dict):
                continue
            level = LEVEL.get(str(block.get("type", "")).lower())
            if level is None:
                continue
            if prev and level > prev + 1:
                warnings.append(f"Body block {index} jumps from level {prev} to {level}; do not skip a heading level.")
            prev = level
    elif body is not None and not isinstance(body, str):
        warnings.append("'body' should be a string or a list of blocks.")

    # Empty body.
    if not text_of(data.get("body")).strip():
        warnings.append("'body' is empty.")

    result = {
        "draft": str(args.draft),
        "document_type": doc_type or None,
        "format": fmt or None,
        "errors": errors,
        "warnings": warnings,
        "status": "fail" if errors else "pass",
    }
    output = json.dumps(result, ensure_ascii=False, indent=2)
    if args.report:
        args.report.write_text(output, encoding="utf-8")
    print(output)

    if errors or (args.strict and warnings):
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
