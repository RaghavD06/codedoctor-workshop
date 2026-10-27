"""Streamlit entrypoint: python -m streamlit run app/app.py"""
from pathlib import Path
import sys
import hmac

# Streamlit launches this file from app/; expose the repository packages.
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import streamlit as st
from agent.model import create_chat
from agent.loop import run_agent
from agent.instructions import DOCTOR_PROMPT, make_task
from examples.patient import BUGGY_CODE
from tools.python_tools import Workspace

st.set_page_config(page_title="CodeDoctor", page_icon="🩺")
st.title("🩺 CodeDoctor")
st.caption("Run broken Python, diagnose bugs, write fixes, and check them with tests.")

try:
    api_key = st.secrets.get("GEMINI_API_KEY", "")
    model = st.secrets.get("MODEL", "")
    app_password = st.secrets.get("APP_PASSWORD", "")
except st.errors.StreamlitSecretNotFoundError:
    api_key = model = app_password = ""

if not api_key or not model or api_key == "PASTE_YOUR_KEY_HERE" or model == "PASTE_CURRENT_FLASH_MODEL_ID":
    st.info("Add GEMINI_API_KEY and MODEL in Streamlit Settings → Secrets, then rerun. For local use, create .streamlit/secrets.toml in the repository root.")
    st.stop()

# A password limits who can use the host's API quota. It is not a sandbox.
if app_password:
    supplied = st.text_input("Workshop password", type="password")
    if not hmac.compare_digest(supplied.encode(), str(app_password).encode()):
        st.stop()

st.warning("Trusted workshop use only: submitted Python runs on this server. Share only with trusted participants.")
code = st.text_area("Paste your broken Python code", value=BUGGY_CODE, height=350)
if st.button("Diagnose & fix", type="primary"):
    st.session_state.pop("diagnosis", None)
    if not code.strip():
        st.warning("Paste some Python code first.")
    else:
        logs = []
        with st.status("CodeDoctor is working...", expanded=True) as status:
            def log(line):
                logs.append(line)
                st.text(line)
            try:
                # Never share/reset a global folder across concurrent visitors.
                with Workspace() as workspace:
                    report = run_agent(make_task(code), DOCTOR_PROMPT,
                                       chat_fn=create_chat(api_key, model),
                                       tools=workspace.tools, log=log)
                    solution = workspace.read_file("solution.py")
                    tests = workspace.read_file("test_solution.py")
                    verification = workspace.run_tests() if tests else "FAILED: no test_solution.py was saved."
                    # Capture everything before the temporary folder is cleaned.
                    st.session_state.diagnosis = (solution, tests, report, verification, logs)
                passed = verification.startswith("OK\n") and not report.startswith("Stopped:") and bool(solution)
                status.update(label="Tests passed - review the result" if passed else "Run finished - review needed", state="complete" if passed else "error")
            except Exception:
                status.update(label="Could not finish the run", state="error")
                st.error("Check your Gemini key, model ID, and quota, then try again. If this continues, check tool-call compatibility for your selected model. Your key is not shown here.")

if "diagnosis" in st.session_state:
    solution, tests, report, verification, logs = st.session_state.diagnosis
    st.subheader("Fixed code")
    st.code(solution or "# No solution was saved.", language="python")
    st.subheader("Tests it wrote")
    st.code(tests or "# No tests were saved.", language="python")
    st.subheader("Final test check")
    st.code(verification, language="text")
    st.subheader("Report")
    st.markdown(report)
    with st.expander("Tool activity"):
        st.text("\n".join(logs))
