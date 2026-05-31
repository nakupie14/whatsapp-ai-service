from fastapi import FastAPI
from routers import lead_scoring, reply_suggest, sentiment, followup, campaign

app = FastAPI(title='WhatsApp AI Service', version='1.0')

app.include_router(lead_scoring.router)
app.include_router(reply_suggest.router)
app.include_router(sentiment.router)
app.include_router(followup.router)
app.include_router(campaign.router)


@app.get('/')
def health_check():
    return {'status': 'AI Service is running'}