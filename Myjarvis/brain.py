import os
from google import genai
import time

client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

last_call_time = 0
COOLDOWN = 20  # seconds

def get_ai_response(prompt: str) -> str:
    global last_call_time

    if time.time() - last_call_time < COOLDOWN:
        return "Please wait a moment before asking again."

    last_call_time = time.time()

    try:
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=prompt
        )
        return response.text.strip() if response.text else "I got no response."

    except Exception as e:
        print("Gemini Error:", e)
        return "My AI brain is currently busy. Please try again later."