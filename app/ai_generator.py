import os
from google import genai
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY not found. Check your .env file.")

client = genai.Client(api_key=api_key)


SYSTEM_INSTRUCTION = """
You are a professional corporate email assistant.

Your task:
- Generate clear, concise, formal business emails.
- Avoid casual tone.
- No emojis.
- No unnecessary fluff.
- Keep it structured and professional.

STRICT OUTPUT FORMAT:

Subject: <clear subject line>

Greeting: Dear <Receiver Name>,

Body:
<Well-structured paragraphs>

Closing:
Sincerely,
<Sender Name>
"""


def generate_email(receiver_name, sender_name, user_prompt):
    full_prompt = f"""
{SYSTEM_INSTRUCTION}

Receiver Name: {receiver_name}
Sender Name: {sender_name}
Email Context: {user_prompt}

Generate the email now.
"""

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=full_prompt,
    )

    if not response.text:
        raise ValueError("Model returned empty response")

    return response.text.strip()
