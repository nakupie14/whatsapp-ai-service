import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


# ══════════════════════════════════════════
# HEALTH CHECK
# ══════════════════════════════════════════

def test_health_check():
    response = client.get('/')
    assert response.status_code == 200
    assert response.json()['status'] == 'AI Service is running'


# ══════════════════════════════════════════
# LEAD SCORING TESTS
# ══════════════════════════════════════════

def test_lead_scoring_hot_blueprint_example():
    """This is the exact example from the guide — must return Hot"""
    response = client.post('/api/score-lead', json={
        'lead_id': 1,
        'name': 'Rahul Sharma',
        'message': 'I need 10 AC units urgently for my office building',
        'source': 'website'
    })
    assert response.status_code == 200
    data = response.json()
    assert data['score'] == 'Hot'
    assert data['lead_id'] == 1
    assert 'reason' in data


def test_lead_scoring_hot_bulk_order():
    response = client.post('/api/score-lead', json={
        'lead_id': 2,
        'name': 'Priya',
        'message': 'Need bulk order with pricing urgently',
        'source': 'website'
    })
    assert response.json()['score'] == 'Hot'


def test_lead_scoring_warm():
    response = client.post('/api/score-lead', json={
        'lead_id': 3,
        'name': 'Sara',
        'message': 'I would like to know more about your services',
        'source': 'website'
    })
    assert response.json()['score'] == 'Warm'


def test_lead_scoring_cold_browsing():
    response = client.post('/api/score-lead', json={
        'lead_id': 4,
        'name': 'Ravi',
        'message': 'Just browsing, not sure about this right now',
        'source': 'website'
    })
    assert response.json()['score'] == 'Cold'


def test_lead_scoring_cold_no_budget():
    response = client.post('/api/score-lead', json={
        'lead_id': 5,
        'name': 'Kiran',
        'message': 'Looks good but no budget right now, maybe later',
        'source': 'website'
    })
    assert response.json()['score'] == 'Cold'


def test_lead_scoring_returns_lead_id():
    """Make sure lead_id comes back in response"""
    response = client.post('/api/score-lead', json={
        'lead_id': 99,
        'name': 'Test',
        'message': 'I want to buy urgently',
        'source': 'website'
    })
    assert response.json()['lead_id'] == 99


def test_lead_scoring_missing_lead_id_returns_422():
    """Missing required field should return validation error"""
    response = client.post('/api/score-lead', json={
        'name': 'Test',
        'message': 'hello'
        # lead_id is missing
    })
    assert response.status_code == 422


# ══════════════════════════════════════════
# SENTIMENT TESTS
# ══════════════════════════════════════════

def test_sentiment_positive_message():
    response = client.post('/api/analyse-sentiment', json={
        'lead_id': 1,
        'message': 'Excellent service, very happy with everything, thank you'
    })
    assert response.status_code == 200
    data = response.json()
    assert data['sentiment'] in ['Positive', 'Neutral']
    assert data['lead_id'] == 1


def test_sentiment_negative_message():
    response = client.post('/api/analyse-sentiment', json={
        'lead_id': 2,
        'message': 'Very disappointed, pathetic service, no reply at all'
    })
    assert response.status_code == 200
    assert response.json()['sentiment'] in ['Negative', 'Neutral']


def test_sentiment_has_confidence_score():
    response = client.post('/api/analyse-sentiment', json={
        'lead_id': 3,
        'message': 'okay service'
    })
    data = response.json()
    assert 'confidence' in data
    assert 0.0 <= data['confidence'] <= 1.0


def test_sentiment_returns_lead_id():
    response = client.post('/api/analyse-sentiment', json={
        'lead_id': 55,
        'message': 'good product'
    })
    assert response.json()['lead_id'] == 55


# ══════════════════════════════════════════
# REPLY SUGGESTION TESTS
# ══════════════════════════════════════════

def test_reply_suggestion_returns_string():
    response = client.post('/api/suggest-reply', json={
        'lead_name': 'Rahul',
        'business_type': 'AC Service',
        'customer_message': 'I need AC installation urgently'
    })
    assert response.status_code == 200
    data = response.json()
    assert 'suggested_reply' in data
    assert isinstance(data['suggested_reply'], str)
    assert len(data['suggested_reply']) > 10


def test_reply_suggestion_different_business():
    response = client.post('/api/suggest-reply', json={
        'lead_name': 'Anita',
        'business_type': 'Coaching Center',
        'customer_message': 'What courses do you offer for Class 10?'
    })
    assert response.status_code == 200
    assert 'suggested_reply' in response.json()


# ══════════════════════════════════════════
# FOLLOW-UP TIMING TESTS
# ══════════════════════════════════════════

def test_followup_hot_lead_1_hour():
    response = client.post('/api/followup-timing', json={
        'lead_id': 1,
        'score': 'Hot',
        'created_at': '2025-05-01 10:00:00',
        'last_contacted': '2025-05-01 10:00:00'
    })
    assert response.status_code == 200
    assert response.json()['follow_up_in_hours'] == 1


def test_followup_warm_lead_24_hours():
    response = client.post('/api/followup-timing', json={
        'lead_id': 2,
        'score': 'Warm',
        'created_at': '2025-05-01 10:00:00',
        'last_contacted': '2025-05-01 10:00:00'
    })
    assert response.json()['follow_up_in_hours'] == 24


def test_followup_cold_lead_72_hours():
    response = client.post('/api/followup-timing', json={
        'lead_id': 3,
        'score': 'Cold',
        'created_at': '2025-05-01 10:00:00',
        'last_contacted': '2025-05-01 10:00:00'
    })
    assert response.json()['follow_up_in_hours'] == 72


def test_followup_returns_recommendation():
    response = client.post('/api/followup-timing', json={
        'lead_id': 4,
        'score': 'Hot',
        'created_at': '2025-05-01 10:00:00',
        'last_contacted': '2025-05-01 10:00:00'
    })
    assert 'recommendation' in response.json()


# ══════════════════════════════════════════
# CAMPAIGN GENERATOR TESTS
# ══════════════════════════════════════════

def test_campaign_returns_message():
    response = client.post('/api/generate-campaign', json={
        'business_type': 'AC Service',
        'offer': '20% off on all services this summer',
        'tone': 'casual'
    })
    assert response.status_code == 200
    data = response.json()
    assert 'campaign_message' in data
    assert len(data['campaign_message']) > 10


def test_campaign_formal_tone():
    response = client.post('/api/generate-campaign', json={
        'business_type': 'Tyre Shop',
        'offer': 'Free wheel alignment with every tyre purchase',
        'tone': 'formal'
    })
    assert response.status_code == 200
    assert 'campaign_message' in response.json()