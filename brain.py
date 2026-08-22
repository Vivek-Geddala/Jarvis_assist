import os

from google import genai
from dotenv import load_dotenv


MODEL_NAME = "gemini-2.0-flash"
load_dotenv()
client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))


def get_ai_response(prompt: str) -> str:
    try:
        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=prompt,
        )
        return response.text.strip() if response.text else "I got no response."
    except Exception as e:
        error_text = str(e)
        print("Gemini Error:", e)

        if "RESOURCE_EXHAUSTED" in error_text or "quota" in error_text.lower():
            return "My Gemini quota is exhausted right now. Please check billing or try again later."

        if "API key" in error_text or "authentication" in error_text.lower():
            return "My Gemini API key is invalid or missing."

        return "My AI brain is currently busy. Please try again later."
