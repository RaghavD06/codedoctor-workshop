"""Stage 2: notebook tools, isolated into a temporary folder per run.
These subprocesses are not a security sandbox. Use trusted inputs only.
"""
import os, sys, shutil, subprocess, tempfile
from pathlib import Path

SAFE_ENV = {"PATH": os.environ.get("PATH", ""), "HOME": "/tmp", "PYTHONIOENCODING": "utf-8", "PYTEST_DISABLE_PLUGIN_AUTOLOAD": "1"}
if os.name == "nt":
    SAFE_ENV["SYSTEMROOT"] = os.environ.get("SYSTEMROOT", r"C:\Windows")

class Workspace:
    def __init__(self):
        self._temp = tempfile.TemporaryDirectory(prefix="codedoctor_")
        self.workdir = Path(self._temp.name)
        self.tools = {"run_code": self.run_code, "save_file": self.save_file, "run_tests": self.run_tests}

    def __enter__(self):
        return self

    def __exit__(self, *exc):
        self._temp.cleanup()

    def reset_workspace(self):
        shutil.rmtree(self.workdir, ignore_errors=True)
        self.workdir.mkdir(parents=True)

    def _run(self, cmd, timeout):
        try:
            p = subprocess.run(cmd, cwd=self.workdir, capture_output=True, text=True, encoding="utf-8", errors="replace",
                               timeout=timeout, env=SAFE_ENV)
            output = (p.stdout + p.stderr).strip() or "(no output)"
            status = "OK" if p.returncode == 0 else f"FAILED (exit code {p.returncode})"
            return f"{status}\n{output[-3000:]}"
        except subprocess.TimeoutExpired:
            return f"FAILED: timed out after {timeout}s (infinite loop?)"

    def run_code(self, code):
        """Run a Python snippet in a separate process and return its output."""
        return self._run([sys.executable, "-c", code], timeout=10)

    def save_file(self, filename, content):
        """Save a file into the workspace (e.g. solution.py or test_solution.py)."""
        path = self.workdir / Path(filename).name
        path.write_text(content, encoding="utf-8")
        return f"Saved {path.name} ({len(content.splitlines())} lines)"

    def run_tests(self, test_file=""):
        """Run pytest in the workspace (all tests, or one test file)."""
        target = [Path(test_file).name] if test_file else []
        return self._run([sys.executable, "-m", "pytest", "-q", "--tb=short",
                     "-p", "no:cacheprovider", *target], timeout=60)

    def read_file(self, filename):
        path = self.workdir / Path(filename).name
        return path.read_text(encoding="utf-8") if path.exists() else ""


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
