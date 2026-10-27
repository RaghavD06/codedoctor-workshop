"""Stage 1: a plain model answer, with no tools or execution."""
def ask(prompt, chat_fn):
    r = chat_fn(messages=[{"role": "user", "content": prompt}])
    return r.choices[0].message.content
