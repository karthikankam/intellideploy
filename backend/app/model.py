import os
import joblib
import numpy as np

MODEL_PATH = os.path.join(os.path.dirname(__file__), "model.pkl")

_model = None


def get_model():
    global _model
    if _model is None:
        if not os.path.exists(MODEL_PATH):
            raise FileNotFoundError(
                f"Model not found at {MODEL_PATH}. Run `python ml/train_model.py` first."
            )
        _model = joblib.load(MODEL_PATH)
    return _model


def predict_risk(age: int, vehicle_age_years: int, prior_claims: int, annual_mileage_thousands: float):
    model = get_model()
    X = np.array([[age, vehicle_age_years, prior_claims, annual_mileage_thousands]])
    proba = model.predict_proba(X)[0][1]
    label = "high" if proba > 0.5 else "low"
    return label, float(proba)
