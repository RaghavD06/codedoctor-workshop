# 🩺 CodeDoctor workshop
Build your first AI agent in Google Colab with Raghav. CodeDoctor runs broken Python, fixes it, writes tests, and repeats until they pass.  
No agent framework: **Agent = LLM + Tools + Loop**.

[![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/RaghavD06/codedoctor-workshop/blob/main/CodeDoctor.ipynb)

## Run the workshop
1. Open the notebook using the **Open in Colab** badge and choose **File → Save a copy in Drive**.
2. Get a personal [Gemini API key](https://aistudio.google.com/apikey), paste it privately into Stage 0, and enter the presenter's verified Flash model ID. Do not show or share your key.
3. Run cells from top to bottom. Use one catch-up cell if behind. Follow [the facilitator guide](FACILITATOR_GUIDE.md) for the 45-minute session and helpers' plan.

## Make it yours: fork this repository
1. Sign in to GitHub and click **Fork** at the top of this repository, then **Create fork**. Your fork is your own copy of the workshop files.
2. Open [CodeDoctor.ipynb](CodeDoctor.ipynb) in your fork. To run that copy in Colab, use `https://colab.research.google.com/github/YOUR_USERNAME/codedoctor-workshop/blob/main/CodeDoctor.ipynb`, replacing `YOUR_USERNAME` with your GitHub username. If you renamed the fork, also replace `codedoctor-workshop`.
3. Build and experiment in Colab. To save changes to your fork, use **File → Save a copy in GitHub**, choose your fork and branch, and save the notebook as `CodeDoctor.ipynb`.

Before saving to GitHub, replace your key with `PASTE_YOUR_KEY_HERE` in every cell where you entered it and clear the outputs. Use your own API key; never commit a real key or `secrets.toml`.

The Colab badge in a new fork initially points to the original workshop. Update its GitHub owner in your fork's README if you want it to open your version.

## Deploy permanently on Streamlit Community Cloud
1. Push this folder as a GitHub repository.
2. In [Streamlit Community Cloud](https://share.streamlit.io), choose **New app** (or **Create app**, depending on the interface), select the repo/branch, and set the entrypoint to `app/app.py`.
3. In advanced settings → **Secrets**, add `GEMINI_API_KEY`, `MODEL`, and optionally `APP_PASSWORD`, using [the example](app/.streamlit/secrets.toml.example). A password is strongly recommended for hosted use.
4. Choose **Deploy**, then verify the sample end to end. Permanent deployment means a hosted URL; availability still depends on the host and API quotas.

The app runs submitted Python. Its timeout and reduced environment are not a security sandbox. Host this educational version for trusted users on a disposable environment. A password limits access; it does not make arbitrary code safe.

## Run Streamlit locally
From this repository:
```sh
cd app
python -m pip install -r requirements.txt
# Copy .streamlit/secrets.toml.example to .streamlit/secrets.toml
# and replace the placeholders privately.
python -m streamlit run app.py
```
Keep `.streamlit/secrets.toml` out of Git. The app creates a distinct temporary workspace for each script run; restart/recycle the host to clean up old workspaces. Its “Done!” status means the loop returned, so check the actual test results and report for failures or the max-steps message.

## Build the slides
```sh
python -m pip install -r slides/requirements.txt
python slides/build_slides.py
```
The script reads `slides/speaker_notes.json`, embeds the supplied speaker notes verbatim, and creates `slides/CodeDoctor_Slides.pptx`. Edit placeholders in the script and rebuild. A 16-slide PNG preview is included in `slides/rendered/`.

## Before presenting
Fill in the published notebook URL and QR, short link, verified model ID, LinkedIn/GitHub links, feedback QR, and CodeLens screenshot. Read [VALIDATION.md](VALIDATION.md) for completed checks and the live checks still needed.

Core sample code is preserved except for a tested Windows-only `SYSTEMROOT` addition to the subprocess environment (see VALIDATION.md). Student code deliberately contains five bugs. No real key is included. Catch-up cells repeat the same source so they work independently.

## Current service references
- [Gemini OpenAI compatibility](https://ai.google.dev/gemini-api/docs/openai)
- [Gemini API keys](https://ai.google.dev/gemini-api/docs/api-key)
- [Gradio sharing](https://www.gradio.app/guides/sharing-your-app)
- [Streamlit deployment](https://docs.streamlit.io/deploy/streamlit-community-cloud/deploy-your-app)
