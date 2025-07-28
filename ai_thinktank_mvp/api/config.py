import os
from dotenv import load_dotenv

load_dotenv()

# 统一使用小爱的OpenAI接口
OPENAI_API_BASE = os.getenv("OPENAI_API_BASE", "https://xiaoai.plus/v1")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "sk-xxx")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-3.5-turbo") 