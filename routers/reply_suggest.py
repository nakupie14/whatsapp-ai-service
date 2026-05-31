from fastapi import APIRouter
from pydantic import BaseModel
from utils.openai_helper import get_ai_reply

router = APIRouter(prefix='/api', tags=['Reply Suggestion'])


# Data we receive from Laravel
class ReplyInput(BaseModel):
    lead_name: str
    business_type: str      # e.g. 'AC Service', 'Coaching Center'
    customer_message: str


@router.post('/suggest-reply')
async def suggest_reply(data: ReplyInput):
    reply = await get_ai_reply(
        name=data.lead_name,
        business=data.business_type,
        message=data.customer_message
    )
    return {'suggested_reply': reply}