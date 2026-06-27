import os
import pickle
import numpy as np
from models.training_data import TRAINING_DATA


# ── Feature Extraction ──────────────────────────────────────

HOT_WORDS = [
    'urgent', 'urgently', 'immediately', 'asap',
    'bulk', 'wholesale', 'large order', 'units',
    'price', 'pricing', 'cost', 'how much', 'quote',
    'purchase', 'order', 'demo', 'today', 'buy',
    'invoice', 'payment', 'delivery', 'sign up'
]

WARM_WORDS = [
    'interested', 'looking for', 'need', 'want',
    'tell me more', 'more details', 'features',
    'how does', 'what is', 'recommend', 'suggest',
    'explain', 'catalogue', 'warranty', 'service',
    'emi', 'offer', 'discount', 'install'
]

COLD_WORDS = [
    'just browsing', 'just checking', 'not sure',
    'maybe', 'later', 'someday', 'no budget',
    'expensive', 'next year', 'just curious',
    'thinking about', 'will get back', 'no plans'
]


def extract_features(message: str) -> list:
    msg = message.lower()

    hot_count = sum(1 for w in HOT_WORDS if w in msg)
    warm_count = sum(1 for w in WARM_WORDS if w in msg)
    cold_count = sum(1 for w in COLD_WORDS if w in msg)
    word_count = len(msg.split())
    char_count = len(msg)
    has_question = 1 if '?' in msg else 0
    has_number = 1 if any(c.isdigit() for c in msg) else 0

    return [
        hot_count,
        warm_count,
        cold_count,
        word_count,
        char_count,
        has_question,
        has_number
    ]


# ── Train Model ──────────────────────────────────────────────

def train_model():
    from sklearn.ensemble import RandomForestClassifier
    from sklearn.model_selection import train_test_split
    from sklearn.metrics import accuracy_score

    # Prepare data
    X = [extract_features(msg) for msg, label in TRAINING_DATA]
    y = [label for msg, label in TRAINING_DATA]

    # Split into train and test
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    # Train Random Forest
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    # Check accuracy
    predictions = model.predict(X_test)
    accuracy = accuracy_score(y_test, predictions)
    print(f'Model trained successfully!')
    print(f'Accuracy on test data: {round(accuracy * 100, 1)}%')

    # Save model to disk
    model_path = os.path.join(os.path.dirname(__file__), 'lead_scorer.pkl')
    with open(model_path, 'wb') as f:
        pickle.dump(model, f)

    print(f'Model saved to models/lead_scorer.pkl')
    return model, accuracy


# ── Load and Predict ─────────────────────────────────────────

def load_model():
    model_path = os.path.join(os.path.dirname(__file__), 'lead_scorer.pkl')

    if not os.path.exists(model_path):
        print('No saved model found — training now...')
        model, _ = train_model()
        return model

    with open(model_path, 'rb') as f:
        model = pickle.load(f)
    print('ML model loaded from disk')
    return model


def predict_score(message: str, model) -> dict:
    features = extract_features(message)
    prediction = model.predict([features])[0]
    probabilities = model.predict_proba([features])[0]
    confidence = round(float(max(probabilities)), 2)

    label_map = {0: 'Cold', 1: 'Warm', 2: 'Hot'}
    score = label_map[prediction]

    reason_map = {
        'Hot': 'ML model detected strong buying signals',
        'Warm': 'ML model detected moderate interest',
        'Cold': 'ML model detected low intent signals'
    }

    return {
        'score': score,
        'reason': reason_map[score],
        'confidence': confidence,
        'model': 'random_forest_v1'
    }