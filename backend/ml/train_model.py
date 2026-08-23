"""
Trains a simple insurance risk classifier and saves it to backend/app/model.pkl.

This is a demo model for the IntelliDeploy CI/CD pipeline — the point is to
have a real artifact that Jenkins can build, test, and ship, not to be a
production-grade risk model. Data is synthetic.
"""
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import joblib
import os

RANDOM_STATE = 42
OUTPUT_PATH = os.path.join(os.path.dirname(__file__), "..", "app", "model.pkl")


def generate_synthetic_data(n_samples: int = 2000):
    """
    Features: [age, vehicle_age_years, prior_claims, annual_mileage_thousands]
    Label: 1 = high risk, 0 = low risk
    """
    rng = np.random.default_rng(RANDOM_STATE)

    age = rng.integers(18, 75, n_samples)
    vehicle_age = rng.integers(0, 20, n_samples)
    prior_claims = rng.poisson(0.6, n_samples)
    annual_mileage = rng.normal(12, 4, n_samples).clip(1, 40)

    # A deliberately simple, explainable risk rule + noise so the model
    # actually has something to learn.
    risk_score = (
        (age < 25).astype(int) * 1.5
        + (vehicle_age > 12).astype(int) * 1.0
        + prior_claims * 1.2
        + (annual_mileage > 20).astype(int) * 0.8
        + rng.normal(0, 0.5, n_samples)
    )
    label = (risk_score > 2.0).astype(int)

    X = np.column_stack([age, vehicle_age, prior_claims, annual_mileage])
    return X, label


def main():
    X, y = generate_synthetic_data()
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=RANDOM_STATE
    )

    model = LogisticRegression(max_iter=1000)
    model.fit(X_train, y_train)

    acc = accuracy_score(y_test, model.predict(X_test))
    print(f"Validation accuracy: {acc:.3f}")

    joblib.dump(model, OUTPUT_PATH)
    print(f"Model saved to {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
