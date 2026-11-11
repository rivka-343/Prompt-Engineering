from __future__ import annotations

import os

import gradio as gr
import pandas as pd

from .agent import build_prompt, generate_command, list_prompt_variants
from .llm_client import LLMClient
from .sandbox import sandbox_execute


def run_prompt(user_input: str, selected_version: str = "v3", use_llm: bool = False) -> str:
    prompt = build_prompt(user_input, version=selected_version)
    if use_llm and os.getenv("OPENAI_API_KEY"):
        client = LLMClient(model="gpt-4o-mini")
        try:
            output = client.generate_command(prompt)
            return output
        except Exception:
            return generate_command(user_input, version=selected_version)
    return generate_command(user_input, version=selected_version)


def evaluate_command(user_input: str, command: str) -> str:
    result = sandbox_execute(command)
    return f"Status: {result['status']} | Reason: {result['reason']}"


def save_evaluation_excel(rows: list[dict], path: str = "evaluation_results.csv") -> str:
    df = pd.DataFrame(rows)
    df.to_csv(path, index=False)
    return path


with gr.Blocks(title="Prompt Engineering CLI Agent") as demo:
    gr.Markdown("## Prompt Engineering CLI Agent")
    gr.Markdown("**Goal:** convert natural-language instructions into a safe Windows CLI command and validate them in a sandbox-style safety layer.")

    with gr.Row():
        with gr.Column(scale=2):
            user_input = gr.Textbox(label="Natural language instruction", lines=3, placeholder="Example: what is the IP address of my computer")
            version = gr.Dropdown(choices=list_prompt_variants(), value="v3", label="Prompt version")
            use_llm = gr.Checkbox(label="Use OpenAI LLM if key is configured", value=False)
            submit = gr.Button("Convert")
        with gr.Column(scale=2):
            output = gr.Textbox(label="Generated command", lines=2)
            sandbox_status = gr.Textbox(label="Sandbox validation", lines=2)

    submit.click(fn=run_prompt, inputs=[user_input, version, use_llm], outputs=output)
    output.change(fn=evaluate_command, inputs=[user_input, output], outputs=sandbox_status)

    gr.Examples(
        examples=[
            ["what is the IP address of my computer", "v3", False],
            ["delete all .tmp files in downloads", "v3", False],
            ["list files by size from largest to smallest", "v3", False],
            ["which processes are running right now", "v3", False],
        ],
        inputs=[user_input, version, use_llm],
    )


if __name__ == "__main__":
    demo.launch(debug=True)
