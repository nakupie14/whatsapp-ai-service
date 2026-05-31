from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional

router = APIRouter(prefix='/api', tags=['Lead Scoring'])


# This defines what data we receive from Laravel
class LeadInput(BaseModel):
    lead_id: int
    name: str
    message: str
    source: Optional[str] = 'website'


# Keywords that mean the lead is ready to buy
HOT_WORDS = [
    'urgent', 'urgently', 'immediately', 'asap',
    'bulk', 'wholesale', 'large order', 'units',
    'buy now', 'price', 'pricing', 'cost', 'how much', 'quote',
    'purchase', 'order', 'demo', 'trial', 'sign up'
]

# Keywords that mean the lead is NOT ready
COLD_WORDS = [
    'just checking', 'just browsing', 'browsing',
    'maybe', 'later', 'not sure', 'someday',
    'no budget', 'expensive'
]


@router.post('/score-lead')
def score_lead(lead: LeadInput):
    # Convert message to lowercase so matching works
    msg = lead.message.lower()

    # Count how many hot and cold words appear
    hot_count = sum(1 for word in HOT_WORDS if word in msg)
    cold_count = sum(1 for word in COLD_WORDS if word in msg)

    # Decide score based on counts
    if cold_count >= 1 and hot_count == 0:
        score = 'Cold'
        reason = 'Low intent signals in message'

    elif hot_count >= 2:
        score = 'Hot'
        reason = 'Multiple urgency or buying signals detected'

    elif hot_count == 1:
        score = 'Warm'
        reason = 'Some buying interest detected'

    else:
        score = 'Warm'
        reason = 'No strong signals — needs follow up'

    # Return result — lead_id must be included in response
    return {
        'lead_id': lead.lead_id,
        'score': score,
        'reason': reason
    }