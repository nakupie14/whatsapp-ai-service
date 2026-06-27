from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional
from models.lead_model import load_model, predict_score

router = APIRouter(prefix='/api', tags=['Lead Scoring'])

# Load ML model once at startup
ml_model = load_model()


class LeadInput(BaseModel):
    lead_id: int
    name: str
    message: str
    source: Optional[str] = 'website'


@router.post('/score-lead')
def score_lead(lead: LeadInput):
    result = predict_score(lead.message, ml_model)

    return {
        'lead_id': lead.lead_id,
        'score': result['score'],
        'reason': result['reason'],
        'confidence': result['confidence'],
        'model': result['model']
    }