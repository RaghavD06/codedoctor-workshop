"""Stage 4 alternative: python -m app.gradio_app [--share]."""
import argparse
import os
import getpass
import gradio as gr
from agent.model import create_chat
from agent.loop import run_agent
from agent.instructions import DOCTOR_PROMPT, make_task
from examples.patient import BUGGY_CODE
from tools.python_tools import Workspace

def build_demo(chat_fn):
    def codedoctor_app(buggy_code):
        with Workspace() as workspace:
            logs = []
            report = run_agent(make_task(buggy_code), DOCTOR_PROMPT,
                               chat_fn=chat_fn, tools=workspace.tools, log=logs.append)
            return "\n".join(logs), workspace.read_file("solution.py"), workspace.read_file("test_solution.py"), report
    return gr.Interface(fn=codedoctor_app,
        inputs=gr.Code(value=BUGGY_CODE, language="python", label="Broken Python code"),
        outputs=[gr.Textbox(label="Tool activity", lines=15), gr.Code(language="python", label="Fixed code"), gr.Code(language="python", label="Tests"), gr.Markdown(label="Report")],
        title="CodeDoctor", description="Trusted workshop inputs only. Code runs on the host.")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--share", action="store_true")
    args = parser.parse_args()
    key = os.environ.get("GEMINI_API_KEY") or getpass.getpass("Gemini API key (hidden): ")
    model = os.environ.get("MODEL") or input("Gemini model ID: ").strip()
    password = os.environ.get("APP_PASSWORD")
    if args.share and not password:
        password = getpass.getpass("Choose a password for your public demo: ")
        if not password:
            raise SystemExit("A password is required for this public demo.")
    build_demo(create_chat(key, model)).launch(share=args.share, auth=("student", password) if password else None)

if __name__ == "__main__":
    main()
