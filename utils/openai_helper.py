import os
from dotenv import load_dotenv

load_dotenv()


def get_openai_client():
    try:
        import openai
        openai.api_key = os.getenv('OPENAI_API_KEY')
        return openai
    except ImportError:
        return None


async def get_ai_reply(name: str, business: str, message: str) -> str:
    client = get_openai_client()

    if not client or not os.getenv('OPENAI_API_KEY'):
        return (
            f"Hi {name}, thank you for reaching out to us! "
            f"We received your message and will get back to you shortly."
        )

    prompt = f"""
You are a helpful assistant for a {business} business in India.
A customer named {name} sent this WhatsApp message: '{message}'
Write a short, polite, professional reply in 2-3 sentences.
Keep it friendly. Do not use complex English.
"""
    try:
        response = client.chat.completions.create(
            model='gpt-4o-mini',
            messages=[{'role': 'user', 'content': prompt}],
            max_tokens=150
        )
        return response.choices[0].message.content.strip()

    except Exception as e:
        print(f'OpenAI error: {e}')
        return (
            f"Hi {name}, thank you for contacting us! "
            f"We will respond to your query very soon."
        )


async def get_campaign_message(business: str, offer: str, tone: str) -> str:
    client = get_openai_client()

    if not client or not os.getenv('OPENAI_API_KEY'):
        return (
            f"Special offer from {business}! {offer}. "
            f"Contact us today on WhatsApp. Limited time only!"
        )

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
    try:
        response = client.chat.completions.create(
            model='gpt-4o-mini',
            messages=[{'role': 'user', 'content': prompt}],
            max_tokens=100
        )
        return response.choices[0].message.content.strip()

    except Exception as e:
        print(f'OpenAI error: {e}')
        return f"{business} Special Offer! {offer}. Reply YES to know more."