"""Stage 2 manual check. From the repo root: python -m tests.manual_tool_check"""
from examples.patient import BUGGY_CODE
from tools.python_tools import Workspace

def main():
    with Workspace() as workspace:
        print(workspace.run_code(BUGGY_CODE))
        print(workspace.save_file("hello.py", "def add(a, b):\n    return a + b\n"))
        print(workspace.save_file("test_hello.py", "from hello import add\n\ndef test_add():\n    assert add(2, 3) == 5\n"))
        print(workspace.run_tests())

if __name__ == "__main__":
    main()
