import os
from dotenv import load_dotenv

load_dotenv()


async def get_ai_reply(name: str, business: str, message: str) -> str:
    try:
        from groq import Groq

        client = Groq(api_key=os.getenv('GROQ_API_KEY'))

        prompt = f"""
You are a helpful assistant for a {business} business in India.
A customer named {name} sent this WhatsApp message: '{message}'
Write a short, polite, professional reply in 2-3 sentences.
Keep it friendly. Do not use complex English.
"""
        response = client.chat.completions.create(
            model='llama-3.3-70b-versatile',
            messages=[{'role': 'user', 'content': prompt}],
            max_tokens=150
        )
        return response.choices[0].message.content.strip()

    except Exception as e:
        print(f'Groq error: {e}')
        return (
            f"Hi {name}, thank you for contacting us! "
            f"We will respond to your query very soon."
        )


async def get_campaign_message(business: str, offer: str, tone: str) -> str:
    try:
        from groq import Groq

        client = Groq(api_key=os.getenv('GROQ_API_KEY'))

        prompt = f"""
Write a WhatsApp marketing message for a {business} business in India.
Offer: {offer}
Tone: {tone}
Rules:
- Maximum 160 characters
- End with a clear call to action like Reply YES or Call now
- No ALL CAPS
- Sound human, not like a robot
"""
        response = client.chat.completions.create(
            model='llama-3.3-70b-versatile',
            messages=[{'role': 'user', 'content': prompt}],
            max_tokens=100
        )
        return response.choices[0].message.content.strip()

    except Exception as e:
        print(f'Groq error: {e}')
        return (
            f"{business} Special Offer! {offer}. Reply YES to know more."
        )