import os
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_BASE = os.getenv("OPENAI_API_BASE", "https://api.openai-proxy.com/v1")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "sk-xxx") 