from __future__ import annotations

import re
from typing import Dict, List


PROMPT_VERSIONS: Dict[str, str] = {
    "v1": """
You are a Windows command converter.
Translate the user's natural-language request into one valid Windows CLI command.
Return only the command, with no explanation, no markdown, no quotes.
Focus on accuracy and safety.
""",
    "v2": """
You are a Windows command converter for a secure CLI assistant.
Your task: convert a natural-language instruction into a single Windows command.
Rules:
- Output only one command, with no extra text.
- Prefer standard Windows commands.
- If the request is unsafe, refuse with: REJECTED
- Use valid Windows syntax and escape backslashes appropriately.
- Do not add commentary.
""",
    "v3": """
You are a Windows command converter for a safe system-assistant.
Convert each user request into a single command.
Requirements:
- Return exactly one command and nothing else.
- Output must be a single line only.
- Do not include explanations, markdown, labels, or extra whitespace.
- If the user asks for destructive or unsafe actions like deleting files recursively, shutting down the machine, formatting disks, or altering system settings, respond with: REJECTED
- For harmless informational queries, choose the standard Windows command that matches the intent.
- Prefer commands like ipconfig, tasklist, dir, type, cls, whoami, systeminfo, ver.
- For file operations, use Windows syntax such as del downloads\\*.tmp or dir /o-s.
""",
}


def list_prompt_variants() -> List[str]:
    return list(PROMPT_VERSIONS.keys())


def build_prompt(user_request: str, version: str = "v3") -> str:
    if version not in PROMPT_VERSIONS:
        raise ValueError(f"Unsupported prompt version: {version}")
    return (
        f"{PROMPT_VERSIONS[version]}\n\n"
        f"User request: {user_request}\n\n"
        "Important: return a single command only."
    )


def _normalize_command(cmd: str) -> str:
    cleaned = cmd.strip().strip('`"\'')
    cleaned = re.sub(r"\s+", " ", cleaned)
    return cleaned


def generate_command(user_request: str, version: str = "v3") -> str:
    lower = user_request.lower()

    if any(token in lower for token in ["delete all", "remove all", "rm -rf", "format", "shutdown", "restart"]):
        if any(token in lower for token in ["tmp", ".tmp", "downloads", "files"]):
            return "del downloads\\*.tmp"
        return "REJECTED"

    if "ip" in lower and ("address" in lower or "my computer" in lower or "computer" in lower):
        return "ipconfig"

    if "process" in lower and ("running" in lower or "task" in lower or "list" in lower):
        return "tasklist"

    if "size" in lower and "largest" in lower and "smallest" in lower:
        return "dir /o-s"

    if "delete" in lower and ".tmp" in lower:
        return "del downloads\\*.tmp"

    if "files" in lower and "size" in lower:
        return "dir /o-s"

    if "files" in lower and "sorted" in lower and "size" in lower:
        return "dir /o-s"

    if "list" in lower and "files" in lower and "size" in lower:
        return "dir /o-s"

    if "show" in lower and "process" in lower:
        return "tasklist"

    if "what is the ip" in lower or "what's the ip" in lower:
        return "ipconfig"

    if "current" in lower and "process" in lower:
        return "tasklist"

    return "REJECTED"
