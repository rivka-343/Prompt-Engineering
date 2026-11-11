from __future__ import annotations

import re
from typing import Dict, List

DANGEROUS_PATTERNS = [
    r"\bformat\b",
    r"\bshutdown\b",
    r"\brestart\b",
    r"\bdel\s+.*\\\*",
    r"\brm\s+-rf\b",
    r"\bmd\b",
]

SAFE_ALLOWLIST = [
    "ipconfig",
    "tasklist",
    "dir",
    "whoami",
    "hostname",
    "ver",
    "time",
    "systeminfo",
    "cls",
    "type",
]


def classify_command(command: str) -> str:
    text = command.strip().lower()
    if not text:
        return "empty"
    if any(re.search(pattern, text) for pattern in DANGEROUS_PATTERNS):
        return "blocked"
    if text.startswith(tuple(SAFE_ALLOWLIST)):
        return "safe"
    return "review"


def sandbox_execute(command: str) -> Dict[str, str | bool]:
    cleaned = command.strip()
    if not cleaned:
        return {"status": "rejected", "reason": "empty command"}
    classification = classify_command(cleaned)
    if classification == "blocked":
        return {"status": "rejected", "reason": "blocked by sandbox safety policy"}
    if classification == "review":
        return {"status": "requires_confirmation", "reason": "non-standard command; review before execution"}
    return {"status": "accepted", "reason": "safe code path", "command": cleaned}


def list_risk_examples() -> List[str]:
    return [
        "shutdown /s /t 0",
        "format c:",
        "del downloads\\*.tmp",
        "ipconfig",
        "tasklist",
    ]
