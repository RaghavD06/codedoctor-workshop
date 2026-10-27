# Facilitator guide · Raghav

## 1. Session goal
Every student builds CodeDoctor, an agent that runs, fixes, and tests Python code.  
They leave knowing **Agent = LLM + Tools + Loop**, and that code that runs is not the same as code that works.

## 2. Run of show
| Time | Activity | Slides |
|---|---|---|
| 0:00–0:06 | Theory | 1–6 |
| 0:06–0:09 | Setup check | 7–8 |
| 0:09–0:13 | Stage 1: brain in a jar | 9 |
| 0:13–0:20 | Stage 2: tools | 10 |
| 0:20–0:32 | Stage 3: the loop + run CodeDoctor | 11–12 |
| 0:32–0:40 | Stage 4: deploy + fix your own bug | 13 |
| 0:40–0:43 | CodeLens demo + where next | 14–15 |
| 0:43–0:45 | Q&A | 16 |

**If behind, shorten Stage 4's “your own bug” part. Never cut Stage 3.**

## 3. Full script

### Slide 1

Thank you! Quick show of hands. Who used ChatGPT, Gemini, or Claude this week?
Keep it up if you've ever BUILT something with one. That's the gap we close tonight. In
45 minutes, every person here builds a working AI agent.

[Show slide 1. Ask for hands. Keep your API-key cell collapsed throughout screen sharing.]

### Slide 2

Ask a chatbot 'does this code work?' and it guesses. An agent runs it and finds out.

[Show slide 2. Contrast suggesting a fix with observing a real execution.]

### Slide 3

An LLM is a brilliant brain in a jar. It can reason but can't touch anything.
Tools give it hands. The loop gives it persistence. It keeps going until the job is done.

[Point to each box: brain, hands, persistence.]

### Slide 4

If you remember one line from tonight, remember this.

[Pause and have the room say the formula once.]

### Slide 5

We never write the steps. The model plans them. That's what makes it agentic.

[Trace the arrows, including the return from Read result to Think. Answer is the exit.]

### Slide 6

LangGraph, CrewAI, agent SDKs: all built on this loop. Tonight we build the loop by
hand so the frameworks stop feeling like magic.

[Define workflow and delegation briefly. Switch to the notebook after the next two slides.]

### Slide 7

CodeDoctor debugs code like a real developer. Runs it, reads the error, fixes it,
writes tests to prove it, and loops until everything passes.

[Preview the debugging cycle. Do not fix the patient by hand.]

### Slide 8

Green sticky on your laptop lid when done, red if stuck and a helper will come.
Fall behind? The catch-up section at the bottom gets you back in one cell.

[Display the published notebook URL and verified model ID. Run “Stage 0: Setup”, then “The patient”. Announce catch-up A/B/C. Wait for about 80% green.]

### Slide 9

It sounds sure. But did it run the code? Did it test anything? Would you merge a
pull request nobody ever ran?

[Run “Stage 1: The brain in a jar”. Let the room read its confident answer. Ask what evidence it produced.]

### Slide 10

The model never runs code. It reads these descriptions and asks us to. And notice:
errors come back as text, not crashes. That's what lets the agent read them and fix them.

[Run “Stage 2: Giving CodeDoctor hands”, then “Try the tools by hand”. Point out NameError and 1 passed. Explain that reset_workspace clears the practice files.]

### Slide 11

Walk through slowly. Each time around: send everything to the model. Did it ask for
a tool? No: done. Yes: run it, send back the result, go again. max_steps is a guardrail.

[Run “Stage 3: The agent loop”. Walk through messages, tool calls, and results. Run “Stage 3: Run CodeDoctor”. Call out a live red error as useful evidence.]

### Slide 12

First it crashes. Fix that, it crashes again. Fix that, it runs, and says the class
average is 184 out of 100. Running code isn't working code. That's why CodeDoctor writes
tests, and why it's not allowed to claim success until they pass.

[Continue the agent run. Inspect pytest output, then run “Stage 3: See the cure”. Check Asha and 82.11. The model may discover bugs in a different order.]

### Slide 13

Gradio turns any Python function into a web app. One line, public link. Open it on
your phone, paste your own buggy code. Security note: it runs on your machine with your
key, share with friends only.

[Run “Stage 4: Ship it”. Open the link on your phone. Use a password for sharing. If time permits, enable one “Your own bug” example. Otherwise demo this stage yourself.]

### Slide 14

Here's where this goes. CodeLens is something I built. Same loop you wrote tonight,
but the tools read and analyze an entire codebase: explain files, find bugs, generate
tests, map the architecture.

[Live demo, 2–3 minutes. Open your prepared CodeLens project. Explain a file, show one bug/test result, then show its architecture view. Switch to a prepared recording or screenshot if the demo fails.]

### Slide 15

Every framework wraps this loop. MCP is a standard way to plug tools in.
Multi-agent? Make run_agent a tool for another agent. Same loop, nothing new.

[Return to slide 15. Point to the Streamlit app link in the notebook wrap-up and README.]

### Slide 16

The notebook is yours to keep. Fill the feedback form, it really helps. A couple
of minutes for questions.

[Show your LinkedIn/GitHub links and feedback QR. Take collected questions. Remind attendees to remove their keys before sharing notebooks.]

## 4. The five planted bugs
The order below is typical, not guaranteed. The agent may find several bugs at once by reading the code. Narrate whatever it does. If a ❌ appears live, call it out: it is the best moment.

| Order | Bug and repair | Narration |
|---|---|---|
| 1 | `len(score)` → `len(scores)` | “NameError: the program refers to a name that doesn't exist. This is a crash bug.” |
| 2 | Kabir has no scores: dividing by zero | “An empty list needs its promised `(None, "N/A")` result before division.” |
| 3 | `class_average` divides by students, not individual scores | “739 divided by 4 is 184.75. It runs, but it is wrong. Divide by 9 scores to get 82.11.” |
| 4 | Topper uses the grade string rather than numeric average | “Alphabetically, F and N/A beat A. Select the highest actual average and skip students without scores.” |
| 5 | `score > 70` excludes exactly 70 | “The docstring promises 70–79 is C. A boundary test catches what the successful run can hide.” |

Expected correct output:
```text
Asha: 91.7 (A)
Ravi: 70.0 (C)
Meera: 84.7 (B)
Kabir: None (N/A)
Topper: Asha
Class average: 82.11
```

Ask students to inspect tests for 69/70/79/80/89/90, no-score students, unequal numbers of scores, and correct topper selection. The docstrings do not define ties, a completely empty class, or a class with no scores at all. Agree a policy before treating one answer as a bug. Passing self-written tests is useful evidence, not a guarantee of correctness.

## 5. Room checkpoints
Move on at about **80% green sticky notes**. Helpers catch up the remaining students.

| Stage | Visible checkpoint | Recovery |
|---|---|---|
| Setup | Packages installed, private key and model pasted, patient printed | Catch-up A |
| 1 | A confident answer, with no execution evidence | Watch the screen if waiting on quota |
| 2 | NameError, then `1 passed` | Catch-up A, then normal Stage 3 |
| 3 | Tool trace, passing tests, numbered report, Asha and 82.11 | Catch-up B |
| 4 | Gradio link opens on a phone | Catch-up C or presenter demo |

## 6. Running it for 100+ people
- Send setup email two days before and again that morning: save a copy, get an API key, run cell 1. Tell attendees to bring a laptop and charger.
- Ask for personal Gmail accounts. College/work policies may block Colab or AI Studio; check eligibility before the event.
- Everyone uses their OWN key. Shared keys hit rate limits quickly. Keep 5–10 authorized spare keys, shared privately by helpers, never on screen. Multiple keys on one project can share quotas, so they are not a quota workaround. Rotate spares after the event.
- Open a setup desk at the entrance 30 minutes before the session.
- Recruit 6–8 helpers, around one per 15 people. Hold a 20-minute briefing in which they run the full notebook, locate catch-up cells, and rehearse rate-limit recovery.
- Put green and red sticky notes on every seat. Assign helpers to room zones.
- Copy-paste cells only. Do not live-type long code.
- Announce catch-up cells at the start. These reset files and require a key and model ID again.
- Zoom Colab to 150% or more and check visibility from the back row.
- Bring a mobile hotspot and keep a fully-run, key-redacted notebook in a separate fallback tab. The attendee notebook stays cleared.
- Pair attendees who do not have laptops.
- Collect questions via Slido or a form and answer them during the wrap-up.

### Setup email (send twice)
Subject: Before CodeDoctor: three quick setup steps

Bring your laptop and charger. Open https://colab.research.google.com/github/RaghavD06/codedoctor-workshop/blob/main/CodeDoctor.ipynb, save a copy in Drive, create your own Gemini API key at https://aistudio.google.com/apikey, and run the setup cell using [MODEL_ID]. Use a personal Google account. Keep the key private and do not email it to us. If anything fails, arrive 30 minutes early for the setup desk. You can also pair with another attendee.

## 7. Backup lines
- Demo fails: “Real agents fail too. Here's one I ran earlier.” Switch to the pre-run, key-redacted tab.
- Wi-Fi dies: “The loop is still the same. Let's trace this saved run together.” Use the hotspot for the presenter and show the saved trace while helpers reconnect the room.
- Room behind: “Jump to catch-up, watch my screen for this part.” Choose A, B, or C based on the stage.
- Running out of time: “I'll show the public app now. Your notebook has everything to try after the session.” Do Stage 4 as an on-screen demo only.

## 8. Troubleshooting
| Problem | Fix |
|---|---|
| 401 / “API key not valid” | Re-copy the key from AI Studio and check for spaces. |
| 404 / “model not found” | Use the model ID on the presenter's screen. |
| 429 / rate limit | The code waits automatically. If it keeps failing, wait a minute. |
| NameError in a notebook cell | An earlier cell wasn't run: Runtime → Run all. The patient's first NameError is intentional. |
| Agent says “Stopped: hit max steps” | Rerun the cell. Agents aren't deterministic: identical inputs can produce different runs. |
| Gradio link not showing | Rerun the deploy cell and wait 10–20 seconds. |
| Colab won't open | Use a personal Gmail account, not a college/work account. |

If a tool-call or thought-signature error occurs, save the error without credentials and use the fallback. The loop preserves `msg.model_dump(exclude_none=True)` exactly as supplied; do not strip provider metadata from assistant messages. Rehearse with the exact model and SDK versions you will use live.

## 9. Day-before and day-of checklists
### Day before
- [ ] Replace GitHub/Colab links, short link, model ID, setup QR, feedback QR, LinkedIn, GitHub, and CodeLens screenshot placeholders.
- [ ] Run the full notebook with a real key and selected model. Verify the five bugs, tests, Asha, 82.11, and the phone link.
- [ ] Run catch-up A, B, C independently in fresh runtimes.
- [ ] Test Streamlit end to end with private secrets and the password gate.
- [ ] Save a key-redacted successful run and a short CodeLens recording. Do not publish credentials.
- [ ] Brief all helpers, send reminders, print sticky-note instructions, and charge the hotspot.
- [ ] Check the current Gemini quota/model availability and Gradio link lifetime.
### Day of
- [ ] Open setup desk 30 minutes early; test venue Wi-Fi from an attendee laptop.
- [ ] Put sticky notes on seats; position helpers; prepare pair seating.
- [ ] Check projector contrast and 150%+ Colab zoom from the back row.
- [ ] Collapse the key cell before sharing; keep spare keys off-screen.
- [ ] Open slides, live notebook, fallback notebook, CodeLens, and feedback form in order.
- [ ] Recheck one real API call and one tool-using agent run on the chosen model.
- [ ] Afterward: close Gradio, rotate spare credentials, and remove keys from shared notebooks.

## Hosting boundary
The supplied subprocess tools have timeouts and a reduced environment, but do not isolate files, network access, or host credentials from submitted Python. Use the Streamlit version only with trusted participants on a disposable host and a password. Public untrusted execution requires a separate hardened sandbox. The sample app also allocates temporary workspaces on reruns; recycle the host periodically.
