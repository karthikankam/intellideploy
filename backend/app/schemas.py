from pydantic import BaseModel, Field


class RiskRequest(BaseModel):
    age: int = Field(..., ge=16, le=100, json_schema_extra={"example": 29})
    vehicle_age_years: int = Field(..., ge=0, le=40, json_schema_extra={"example": 4})
    prior_claims: int = Field(..., ge=0, le=20, json_schema_extra={"example": 0})
    annual_mileage_thousands: float = Field(..., ge=0, le=100, json_schema_extra={"example": 12.5})


class RiskResponse(BaseModel):
    risk_label: str
    risk_probability: float


class Policy(BaseModel):
    id: int
    holder_name: str
    vehicle: str
    risk_label: str | None = None


class PolicyCreate(BaseModel):
    holder_name: str
    vehicle: str
