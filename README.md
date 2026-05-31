# WhatsApp AI Service
**One Step Marketing — Jaipur**
Python AI Microservice | Built by Nakul Soni

---

## What This Service Does

| # | Feature | Endpoint | Status |
|---|---|---|---|
| 1 | Lead Scoring | `POST /api/score-lead` | ✅ Week 1 |
| 2 | AI Reply Suggestion | `POST /api/suggest-reply` | ✅ Week 2 |
| 3 | Sentiment Analysis | `POST /api/analyse-sentiment` | ✅ Week 2 |
| 4 | Smart Follow-up Timing | `POST /api/followup-timing` | ✅ Week 3-4 |
| 5 | Campaign Generator | `POST /api/generate-campaign` | ✅ Week 3-4 |

---

## Setup (Follow in Order)

### Step 1 — Clone the Repo
```bash
git clone https://github.com/YOUR_USERNAME/whatsapp-ai-service.git
cd whatsapp-ai-service
```

### Step 2 — Create Virtual Environment
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Mac / Linux
source venv/bin/activate
```

You will see `(venv)` at the start of your terminal. Always activate before working.

### Step 3 — Install Packages
```bash
# Week 1 only (minimum install)
pip install fastapi uvicorn pydantic python-dotenv requests httpx pytest

# Week 2 onwards (add these)
pip install openai transformers torch

# Week 3-4 onwards (add these)
pip install scikit-learn pandas numpy
```

### Step 4 — Set Up API Keys
```bash
# Copy the example file
cp .env.example .env

# Open .env and add your real keys
OPENAI_API_KEY=sk-your-real-key-here
```

Get your OpenAI key from: https://platform.openai.com

### Step 5 — Run the Server
```bash
uvicorn main:app --reload --port 8001
```

Server runs at: **http://localhost:8001**

Auto-generated docs: **http://localhost:8001/docs** ← Share this screenshot with your developer

---

## Testing with Postman

### Feature 1 — Lead Scoring

```
Method: POST
URL:    http://localhost:8001/api/score-lead
Body (raw JSON):
```

```json
{
  "lead_id": 1,
  "name": "Rahul Sharma",
  "message": "I need 10 AC units urgently for my office building",
  "source": "website"
}
```

Expected response:
```json
{
  "lead_id": 1,
  "score": "Hot",
  "reason": "Multiple urgency or buying signals detected"
}
```

### Feature 2 — Suggest Reply

```
Method: POST
URL:    http://localhost:8001/api/suggest-reply
```
```json
{
  "lead_name": "Rahul",
  "business_type": "AC Service",
  "customer_message": "I need AC installation for my office urgently"
}
```

### Feature 3 — Sentiment Analysis

```
Method: POST
URL:    http://localhost:8001/api/analyse-sentiment
```
```json
{
  "lead_id": 1,
  "message": "Excellent service, very happy with everything"
}
```

### Feature 4 — Follow-up Timing

```
Method: POST
URL:    http://localhost:8001/api/followup-timing
```
```json
{
  "lead_id": 1,
  "score": "Hot",
  "created_at": "2025-05-01 10:00:00",
  "last_contacted": "2025-05-01 10:00:00"
}
```

### Feature 5 — Campaign Generator

```
Method: POST
URL:    http://localhost:8001/api/generate-campaign
```
```json
{
  "business_type": "AC Service",
  "offer": "20% off on all services this summer",
  "tone": "casual"
}
```

---

## Run Tests

```bash
pytest tests/ -v
```

---

## How Laravel Connects to This Service

Laravel runs on `localhost:8000`
This Python service runs on `localhost:8001`

Laravel calls this service like:
```
POST http://localhost:8001/api/score-lead
POST http://localhost:8001/api/suggest-reply
POST http://localhost:8001/api/analyse-sentiment
POST http://localhost:8001/api/followup-timing
POST http://localhost:8001/api/generate-campaign
```

---

## Project Structure

```
whatsapp-ai-service/
├── main.py                    ← FastAPI entry point
├── requirements.txt
├── Dockerfile
├── .env                       ← Your API keys (never commit this)
├── .env.example               ← Template (safe to commit)
├── .gitignore
├── README.md
├── routers/
│   ├── lead_scoring.py        ← Feature 1
│   ├── reply_suggest.py       ← Feature 2
│   ├── sentiment.py           ← Feature 3
│   ├── followup.py            ← Feature 4
│   └── campaign.py            ← Feature 5
├── utils/
│   └── openai_helper.py       ← OpenAI API calls
└── tests/
    └── test_all_features.py   ← All tests
```

---

## Daily Git Commands

```bash
git add .
git commit -m "your message here"
git push origin main
```

Commit every day before stopping work.
