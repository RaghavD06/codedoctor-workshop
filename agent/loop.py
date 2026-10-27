"""Stage 3: model -> tool -> result -> repeat, just like the notebook."""
import json
from tools.python_tools import tool_specs

def run_agent(task, system_prompt, max_steps=15, log=print, *, chat_fn, tools):
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": task},
    ]
    for step in range(1, max_steps + 1):
        msg = chat_fn(messages=messages, tools=tool_specs).choices[0].message

        if not msg.tool_calls:                     # agent decided it's done
            return msg.content or "The model returned no final report."

        if msg.content:
            log(f"💭 {msg.content}")
        messages.append(msg.model_dump(exclude_none=True))

        for call in msg.tool_calls:
            args = json.loads(call.function.arguments or "{}")
            detail = f" → {args['filename']}" if "filename" in args else ""
            log(f"\n🔧 Step {step}: {call.function.name}{detail}")

            result = tools[call.function.name](**args)
            icon = "❌" if result.startswith("FAILED") else "✅"
            log(f"{icon} {result[:600]}")
            messages.append({"role": "tool", "tool_call_id": call.id, "content": result})

    return "Stopped: hit max steps without finishing."
