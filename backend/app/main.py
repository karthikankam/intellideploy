from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from app.schemas import RiskRequest, RiskResponse, Policy, PolicyCreate
from app.model import predict_risk

app = FastAPI(
    title="IntelliDeploy API",
    description="AI/ML-integrated backend for the IntelliDeploy CI/CD demo project",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # demo only — restrict in real deployments
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory store just to demonstrate a real fullstack CRUD flow.
_policies: list[Policy] = []
_next_id = 1


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/api/predict", response_model=RiskResponse)
def predict(payload: RiskRequest):
    label, proba = predict_risk(
        payload.age,
        payload.vehicle_age_years,
        payload.prior_claims,
        payload.annual_mileage_thousands,
    )
    return RiskResponse(risk_label=label, risk_probability=round(proba, 4))


@app.get("/api/policies", response_model=list[Policy])
def list_policies():
    return _policies


@app.post("/api/policies", response_model=Policy, status_code=201)
def create_policy(payload: PolicyCreate):
    global _next_id
    policy = Policy(id=_next_id, holder_name=payload.holder_name, vehicle=payload.vehicle)
    _policies.append(policy)
    _next_id += 1
    return policy


@app.delete("/api/policies/{policy_id}", status_code=204)
def delete_policy(policy_id: int):
    global _policies
    before = len(_policies)
    _policies = [p for p in _policies if p.id != policy_id]
    if len(_policies) == before:
        raise HTTPException(status_code=404, detail="Policy not found")
    return None
