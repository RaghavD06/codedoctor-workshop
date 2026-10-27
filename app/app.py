import tempfile
import streamlit as st

st.set_page_config(page_title="CodeDoctor", page_icon="🩺")

# The app runs submitted code and uses your API key, so a password stops
# strangers burning your quota. This is a trusted-user demo, not a sandbox.
if "APP_PASSWORD" in st.secrets:
    password = st.text_input("Workshop password", type="password")
    if password != st.secrets["APP_PASSWORD"]:
        st.stop()

import json, os, sys, time, shutil, subprocess
from pathlib import Path
from openai import OpenAI, RateLimitError

client = OpenAI(
    api_key=st.secrets["GEMINI_API_KEY"],
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)
MODEL = st.secrets.get("MODEL", "<model id>")

def chat(**kwargs):
    """Calls the model, and waits + retries if we hit the free-tier rate limit."""
    for attempt in range(4):
        try:
            return client.chat.completions.create(model=MODEL, **kwargs)
        except RateLimitError:
            if attempt == 3:
                raise
            print("⏳ Rate limited, waiting 20 seconds...")
            time.sleep(20)

SAMPLE_CODE = '''
def letter_grade(score):
    """Return the letter grade: 90+ is A, 80-89 is B, 70-79 is C, below 70 is F."""
    if score >= 90:
        return "A"
    elif score >= 80:
        return "B"
    elif score > 70:
        return "C"
    else:
        return "F"


def class_report(students):
    """
    students: dict of name -> list of scores.
    Returns (report, topper):
      report: dict of name -> (average rounded to 1 decimal, letter grade).
              Students with no scores get (None, "N/A").
      topper: name of the student with the highest average.
    """
    report = {}
    for name, scores in students.items():
        avg = sum(scores) / len(score)
        report[name] = (round(avg, 1), letter_grade(avg))
    topper = max(report, key=lambda n: report[n][1])
    return report, topper


def class_average(students):
    """Return the average of every individual score in the class."""
    all_scores = [s for scores in students.values() for s in scores]
    return sum(all_scores) / len(students)


students = {
    "Asha": [92, 88, 95],
    "Ravi": [70, 72, 68],
    "Meera": [85, 79, 90],
    "Kabir": [],
}

report, topper = class_report(students)
for name, (avg, grade) in report.items():
    print(f"{name}: {avg} ({grade})")
print("Topper:", topper)
print("Class average:", round(class_average(students), 2))
'''

WORKDIR = Path(tempfile.mkdtemp(prefix="codedoctor_"))
SAFE_ENV = {"PATH": os.environ.get("PATH", ""), "HOME": "/tmp"}
# Windows needs SYSTEMROOT for Python networking dependencies used by pytest.
if os.name == "nt":
    SAFE_ENV["SYSTEMROOT"] = os.environ.get("SYSTEMROOT", r"C:\Windows")

def reset_workspace():
    shutil.rmtree(WORKDIR, ignore_errors=True)
    WORKDIR.mkdir(parents=True)

def _run(cmd, timeout):
    try:
        p = subprocess.run(cmd, cwd=WORKDIR, capture_output=True, text=True,
                           timeout=timeout, env=SAFE_ENV)
        output = (p.stdout + p.stderr).strip() or "(no output)"
        status = "OK" if p.returncode == 0 else f"FAILED (exit code {p.returncode})"
        return f"{status}\n{output[-3000:]}"
    except subprocess.TimeoutExpired:
        return f"FAILED: timed out after {timeout}s (infinite loop?)"

def run_code(code):
    """Run a Python snippet in a separate process and return its output."""
    return _run([sys.executable, "-c", code], timeout=10)

def save_file(filename, content):
    """Save a file into the workspace (e.g. solution.py or test_solution.py)."""
    path = WORKDIR / Path(filename).name
    path.write_text(content)
    return f"Saved {path.name} ({len(content.splitlines())} lines)"

def run_tests(test_file=""):
    """Run pytest in the workspace (all tests, or one test file)."""
    target = [Path(test_file).name] if test_file else []
    return _run([sys.executable, "-m", "pytest", "-q", "--tb=short",
                 "-p", "no:cacheprovider", *target], timeout=60)

def read_file(filename):
    path = WORKDIR / Path(filename).name
    return path.read_text() if path.exists() else ""

reset_workspace()
TOOLS = {"run_code": run_code, "save_file": save_file, "run_tests": run_tests}

tool_specs = [
    {"type": "function", "function": {
        "name": "run_code",
        "description": ("Run Python code in a fresh process and return its output and "
                        "any error. Files saved in the workspace (like solution.py) "
                        "can be imported."),
        "parameters": {"type": "object",
                       "properties": {"code": {"type": "string",
                                               "description": "Python code to run"}},
                       "required": ["code"]}}},
    {"type": "function", "function": {
        "name": "save_file",
        "description": ("Save a file to the workspace. Use solution.py for the fixed "
                        "code and test_solution.py for pytest tests."),
        "parameters": {"type": "object",
                       "properties": {"filename": {"type": "string"},
                                      "content": {"type": "string",
                                                  "description": "Full file contents"}},
                       "required": ["filename", "content"]}}},
    {"type": "function", "function": {
        "name": "run_tests",
        "description": "Run the pytest tests in the workspace and return the results.",
        "parameters": {"type": "object",
                       "properties": {"test_file": {"type": "string",
                                                    "description": "Optional: one test file to run. Leave empty to run all tests."}}}}},
]

def run_agent(task, system_prompt, max_steps=15, log=print):
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": task},
    ]
    for step in range(1, max_steps + 1):
        msg = chat(messages=messages, tools=tool_specs).choices[0].message

        if not msg.tool_calls:                     # agent decided it's done
            return msg.content

        if msg.content:
            log(f"💭 {msg.content}")
        messages.append(msg.model_dump(exclude_none=True))

        for call in msg.tool_calls:
            args = json.loads(call.function.arguments or "{}")
            detail = f" → {args['filename']}" if "filename" in args else ""
            log(f"\n🔧 Step {step}: {call.function.name}{detail}")

            result = TOOLS[call.function.name](**args)
            icon = "❌" if result.startswith("FAILED") else "✅"
            log(f"{icon} {result[:600]}")
            messages.append({"role": "tool", "tool_call_id": call.id, "content": result})

    return "Stopped: hit max steps without finishing."

DOCTOR_PROMPT = """You are CodeDoctor, an expert Python debugger. Follow this process:
1. Run the original code with run_code to see what actually happens.
2. Read every error carefully and find the root cause. Also look for LOGIC bugs:
   compare what the code does with what its docstrings promise.
3. Save the fully fixed code as solution.py using save_file. Put any demo/print
   code under if __name__ == "__main__": so tests can import it cleanly.
4. Write pytest tests in test_solution.py that check every promise in the
   docstrings, including edge cases. Import functions from solution.
5. Run run_tests. If a test fails, decide whether the code or the test is wrong,
   fix it, and run the tests again.
6. Never claim success until you have seen all tests pass.
Finish with a short report: a numbered list of each bug (what was wrong and how
you fixed it), then the final test result."""

def make_task(code):
    return ("Here is some broken Python code. Diagnose it, fix it, and prove "
            "the fix with tests.\n\n" + code)

st.title("🩺 CodeDoctor")
st.caption("An AI agent that runs your code, finds the bugs, fixes them, "
           "and proves the fix with tests.")
code = st.text_area("Paste your broken Python code", value=SAMPLE_CODE, height=350)
if st.button("Diagnose & fix", type="primary"):
    reset_workspace()
    with st.status("CodeDoctor is working...", expanded=True) as status:
        report = run_agent(make_task(code), DOCTOR_PROMPT, log=st.text)
        status.update(label="Done!", state="complete")
    st.subheader("✅ Fixed code")
    st.code(read_file("solution.py"), language="python")
    st.subheader("🧪 Tests it wrote")
    st.code(read_file("test_solution.py"), language="python")
    st.subheader("🩺 Report")
    st.markdown(report)
