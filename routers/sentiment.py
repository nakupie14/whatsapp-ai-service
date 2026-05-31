from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter(prefix='/api', tags=['Sentiment'])

# We try to load HuggingFace model at startup
# If not installed yet, fallback to keyword method
sentiment_model = None


def load_huggingface_model():
    global sentiment_model
    try:
        from transformers import pipeline
        sentiment_model = pipeline('sentiment-analysis')
        print('HuggingFace model loaded successfully')
    except Exception as e:
        print(f'HuggingFace not available yet — using keyword fallback. Error: {e}')
        sentiment_model = None


# Run this when service starts
load_huggingface_model()


# Simple keyword-based fallback (works without any install)
POSITIVE_WORDS = [
    'good', 'great', 'excellent', 'happy', 'satisfied', 'perfect',
    'amazing', 'wonderful', 'thanks', 'thank you', 'helpful', 'love',
    'best', 'fantastic', 'superb'
]

NEGATIVE_WORDS = [
    'bad', 'worst', 'terrible', 'angry', 'disappointed', 'horrible',
    'pathetic', 'useless', 'fraud', 'cheat', 'no reply', 'waste',
    'poor', 'awful', 'disgusting'
]


def keyword_sentiment(message: str):
    msg = message.lower()
    pos = sum(1 for w in POSITIVE_WORDS if w in msg)
    neg = sum(1 for w in NEGATIVE_WORDS if w in msg)

    if neg > pos:
        return 'Negative', 0.75
    elif pos > neg:
        return 'Positive', 0.75
    return 'Neutral', 0.60


# Data we receive from Laravel
class SentimentInput(BaseModel):
    lead_id: int
    message: str


@router.post('/analyse-sentiment')
def analyse_sentiment(data: SentimentInput):

    if sentiment_model:
        # Use HuggingFace model if loaded
        result = sentiment_model(data.message)[0]
        label = result['label']    # 'POSITIVE' or 'NEGATIVE'
        score = round(result['score'], 2)

        if label == 'POSITIVE' and score > 0.85:
            sentiment = 'Positive'
        elif label == 'NEGATIVE' and score > 0.85:
            sentiment = 'Negative'
        else:
            sentiment = 'Neutral'

    else:
        # Use keyword fallback
        sentiment, score = keyword_sentiment(data.message)

    return {
        'lead_id': data.lead_id,
        'sentiment': sentiment,
        'confidence': score
    }