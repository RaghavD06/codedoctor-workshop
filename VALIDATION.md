# Validation and handoff

Checked on 27 October 2026 on Windows with Python 3.12. No `GEMINI_API_KEY` or model ID was available in the session. **This kit has not been verified end to end against Gemini.** Do not interpret the scripted-response checks below as evidence that the model diagnosed the patient.

## Completed

| Check | Result |
|---|---|
| Notebook JSON and nbformat 4 schema | Pass using nbformat.validate |
| All code cells have preceding explanations/checkpoints | Pass |
| All outputs cleared and execution counts null | Pass |
| All code cells parse after excluding Colab's pip command | Pass |
| Main cells match supplied code except documented Windows repair | Pass |
| Catch-up A/B/C contain the corresponding complete source | Pass, structural comparison; not live-executed independently |
| App function definitions match notebook | Pass, AST comparison |
| Stage 2 subprocess execution | Expected NameError, then `1 passed` |
| Timeout behavior | Pass, deliberately slow child process timed out |
| Agent loop with scripted SDK responses | Pass: multiple tool calls, real file writes, pytest, result messages, final answer, max-steps guard |
| Gradio | Exact Interface constructed and launched on localhost; HTTP 200; server closed afterward |
| Streamlit | AppTest exercised password rejection/acceptance, button, real tools and pytest, output panes and report with scripted SDK responses |
| `streamlit run` | Local server started; health endpoint returned `ok`; server stopped afterward |
| Deck | 16 slides; all speaker notes match supplied text verbatim |
| Slide rendering | 16 PNGs rendered from generated PPTX using artifact-tool; visually inspected, no visible text overflow |

LibreOffice was unavailable. PowerPoint COM failed with “Server execution failed”, so the deck was not visually checked in PowerPoint itself. The rendered PNGs are alternative-renderer previews; check the final deck on the presentation laptop before the session.

## Code change proved necessary by a test

The supplied `SAFE_ENV` contains only `PATH` and `HOME`. On Windows, the Stage 2 pytest process failed while importing its networking dependencies with `OSError: [WinError 10106]`. Added immediately after the original assignment:

```python
# Windows needs SYSTEMROOT for Python networking dependencies used by pytest.
if os.name == "nt":
    SAFE_ENV["SYSTEMROOT"] = os.environ.get("SYSTEMROOT", r"C:\Windows")
```

The same test then returned `1 passed`. This repair appears in the notebook's tools cell, every catch-up cell, and `app/app.py`. It has no effect on Linux/Colab. No other supplied runtime logic changed. The Streamlit secrets, sample-name, workspace, imports, and password-gate differences are those requested in the brief. In the Windows test harness only, the Colab `/content/...` workspace was redirected to a local scratch directory.

The assistant-message append remains `msg.model_dump(exclude_none=True)`. No Gemini thought-signature fix was made because no authenticated call was possible and no such error was observed.

## Required live rehearsal

1. Select a currently available Gemini Flash model that supports tool calling. Read a real key from `GEMINI_API_KEY` in a private test harness only; substitute it and the model ID in memory, keeping the delivered notebook placeholders unchanged. Do not print the key or save it in logs.
2. In Colab, run every main notebook cell. Confirm Stage 2 prints NameError then `1 passed`; Stage 3 shows actual passing tests and a numbered five-bug report. Inspect the tests, rather than relying on the report alone.
3. Confirm the fixed program prints Asha 91.7 (A), Ravi 70.0 (C), Meera 84.7 (B), Kabir None (N/A), `Topper: Asha`, and `Class average: 82.11`.
4. Launch the actual `share=True` Gradio cell, open its link on a phone, and submit a trusted example. Public tunnel creation and the Gemini callback were not tested here.
5. Run catch-up A, B, and C separately in fresh runtimes. Each needs its own key/model substitutions.
6. Configure Streamlit Secrets and use the app with the same real model. Confirm the complete sample diagnosis, tests, fixed output, and password gate. The local server/UI smoke tests here do not replace this step.
7. If Gemini rejects a tool-result turn, retain the full error without credentials, repair message serialization based on that reproduced error, apply it equally to notebook/catch-up/app, and rerun. Do not remove provider metadata speculatively.
8. Clear all outputs, remove test credentials, and keep a separate key-redacted successful run for the presenter's fallback.

## Text clarification

The supplied brief says Gradio links last up to 72 hours. Its current [sharing guide](https://www.gradio.app/guides/sharing-your-app) says one week, while its [share-link guide](https://www.gradio.app/guides/understanding-gradio-share-links) still refers to 72 hours. The notebook notes this discrepancy and explains that the Colab runtime must remain active. Speaker notes remain verbatim.

## Fill in before publishing

- `<USER>/<REPO>` in the Colab badge and notebook's Streamlit source link.
- Published notebook URL, short link, and setup QR on slide 8 and in setup email.
- Verified model ID in the notebook, slide 8, and deployment Secrets.
- Private Gemini key and optional app password in local/hosted Secrets, never the repository.
- CodeLens screenshot on slide 14; rehearse the live demo or prepare a recording.
- LinkedIn, GitHub, feedback-form URL and QR on slide 16.

## Deliverable inventory

```text
codedoctor-workshop/
  .gitignore
  CodeDoctor.ipynb
  FACILITATOR_GUIDE.md
  README.md
  VALIDATION.md
  app/
    app.py
    requirements.txt
    .streamlit/secrets.toml.example
  slides/
    build_slides.py
    requirements.txt
    speaker_notes.json
    CodeDoctor_Slides.pptx
    rendered/slide-01.png through slide-16.png
```

`speaker_notes.json` is a build dependency. Keep it beside `build_slides.py`. The ZIP contains this full directory, including all 16 PNG previews.
