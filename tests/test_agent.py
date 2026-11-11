import pytest

from prompt_engineering_lab.agent import build_prompt, generate_command, list_prompt_variants


def test_build_prompt_includes_instruction_to_return_single_command():
    prompt = build_prompt("show running processes", version="v3")
    assert "single command" in prompt.lower()
    assert "windows" in prompt.lower()


def test_generate_command_detects_common_windows_commands():
    cases = {
        "what is the IP address of my computer": "ipconfig",
        "delete all .tmp files in downloads": "del downloads\\*.tmp",
        "list files by size from largest to smallest": "dir /o-s",
        "show current running processes": "tasklist",
    }
    for user_text, expected in cases.items():
        result = generate_command(user_text)
        assert result == expected


def test_prompt_variants_are_available():
    variants = list_prompt_variants()
    assert "v1" in variants
    assert "v2" in variants
    assert "v3" in variants
