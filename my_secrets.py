import os
from dotenv import load_dotenv

load_dotenv()


gemini_api_key = os.getenv("GEMINI_API_KEY")
if gemini_api_key is None:
    raise ValueError("GEMINI_API_KEY is not set in the environment variables.")

gemini_model = os.getenv("GEMINI_MODEL")
if gemini_model is None:
    raise ValueError("GEMINI_MODEL is not set in the environment variables.")
openrouter_api_key = os.getenv("OPENROUTER_API_KEY")
openrouter_api_url = os.getenv("OPENROUTER_API_URL")
openrouter_gemini_model = os.getenv("OPENROUTER_GEMINI_MODEL")
openrouter_deepseek_model = os.getenv("OPENROUTER_DEEPSEEK_MODEL")


class Secrets:
    def __init__(self):
        self.gemini_api_key = gemini_api_key
        self.gemini_model = gemini_model
        self.openrouter_api_key = openrouter_api_key
        self.openrouter_api_url = openrouter_api_url
        self.openrouter_gemini_model = openrouter_gemini_model
        self.openrouter_deepseek_model = openrouter_deepseek_model
