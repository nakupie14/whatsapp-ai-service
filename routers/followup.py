from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter(prefix='/api', tags=['Follow-up'])


# Data we receive from Laravel
class FollowupInput(BaseModel):
    lead_id: int
    score: str          # Hot / Warm / Cold
    created_at: str     # When lead came in e.g. '2025-05-01 10:00:00'
    last_contacted: str # Last time someone messaged them


@router.post('/followup-timing')
def followup_timing(data: FollowupInput):

    if data.score == 'Hot':
        hours = 1
        message = 'Hot lead — follow up within 1 hour'

    elif data.score == 'Warm':
        hours = 24
        message = 'Warm lead — follow up within 24 hours'

    else:
        hours = 72
        message = 'Cold lead — follow up within 3 days'

    return {
        'lead_id': data.lead_id,
        'follow_up_in_hours': hours,
        'recommendation': message
    }