from fastapi import APIRouter
from pydantic import BaseModel
from utils.openai_helper import get_campaign_message

router = APIRouter(prefix='/api', tags=['Campaign'])


# Data we receive from Laravel
class CampaignInput(BaseModel):
    business_type: str  # e.g. 'AC Service', 'Tyre Shop'
    offer: str          # e.g. '20% off on all services'
    tone: str           # 'formal' or 'casual'


@router.post('/generate-campaign')
async def generate_campaign(data: CampaignInput):
    message = await get_campaign_message(
        business=data.business_type,
        offer=data.offer,
        tone=data.tone
    )
    return {'campaign_message': message}