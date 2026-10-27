"""Stage 0: connect to Gemini. Credentials are supplied by the app."""
import time
from openai import OpenAI, RateLimitError

def create_chat(api_key, model):
    """Create a separate model connection for this app run."""
    client = OpenAI(api_key=api_key, base_url="https://generativelanguage.googleapis.com/v1beta/openai/")
    def chat(**kwargs):
        for attempt in range(4):
            try:
                return client.chat.completions.create(model=model, **kwargs)
            except RateLimitError:
                if attempt == 3:
                    raise
                time.sleep(20)
    return chat
