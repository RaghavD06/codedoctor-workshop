# CodeDoctor

**VS Code + Streamlit:** [CodeDoctor.ipynb](CodeDoctor.ipynb) is the complete-file copy guide. Every block includes imports; replace the entire destination file. Run the finished app from the terminal, not by executing guide cells.

**Run directly in Colab:** [Open the separate Colab lesson](https://colab.research.google.com/github/RaghavD06/codedoctor-workshop/blob/main/CodeDoctor_Colab.ipynb). Run its cells in order; do not paste those shared-state cells into separate files.

The Python files now contain the finished implementation, following the notebook stages.

| Stage | File |
|---|---|
| 0: Gemini connection | `agent/model.py` |
| Patient | `examples/patient.py` |
| 1: plain model call | `agent/brain_in_a_jar.py` |
| 2: tools | `tools/python_tools.py` |
| 2: manual check | `tests/manual_tool_check.py` |
| 3: loop and prompt | `agent/loop.py`, `agent/instructions.py` |
| 4: Gradio | `app/gradio_app.py` |
| Streamlit deployment | `app/app.py` |

## Deploy on Streamlit

1. Fork this repository. The implementation is included; no copying is required.
2. Open https://share.streamlit.io and choose **Create app**.
3. Select your fork, branch `main`, main file `app/app.py`.
4. In **Advanced settings → Secrets**, enter:

```toml
GEMINI_API_KEY = "your-real-key"
MODEL = "your-available-gemini-model-id"
APP_PASSWORD = "your-private-workshop-password"
```

5. Save and deploy. Open the app, enter the password, and click **Diagnose & fix**.
6. Review the generated tests and final test check. A report alone is not proof of success.

Use your own supported Gemini model ID; availability and free-tier quotas vary. No model or key is hard-coded. Never commit real secrets.

## Run locally

From the repository root:

```sh
python -m pip install -r requirements.txt
```

Copy `.streamlit/secrets.toml.example` to `.streamlit/secrets.toml` and fill it privately. Then:

```sh
python -m streamlit run app/app.py
```

For the notebook's Gradio interface:

```sh
python -m app.gradio_app
```

It prompts privately for your key and asks for the model ID. Add `--share` for a temporary public link; it prompts for a demo password. Keep the process running.

## Check the tools

```sh
python -m tests.manual_tool_check
python -m pytest -q tests
```

The manual check should show the patient's intentional NameError, then `1 passed`.

## How the notebook became modules

The same patient, prompt, tool schemas, and decision/tool/result loop are retained. `create_chat()` takes credentials from the app; the loop receives its model connection and tools explicitly. Each diagnosis has a separate temporary workspace, cleaned afterward, so users do not overwrite one another. The app reruns the generated tests before showing a passing status. Python files contain no notebook `!pip` commands.

## Hosting boundary

This educational app executes submitted Python on its host. Timeouts and a reduced environment are not a security sandbox. Use only trusted participants on a disposable host. The password limits access but does not isolate malicious code. Live Gemini verification requires your own key and selected model; local tests use scripted model responses and do not prove provider compatibility.
