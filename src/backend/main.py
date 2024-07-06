from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from datamodel import (
    FractureRisks,
    ShapPlots,
    RiskCalculationRequest,
    RiskCalculationResponse,
)
from fracture_risk.ml.risk_calculator import BonoAI


app = FastAPI()

origins = [
    "http://localhost:5173",  # IMPORTANT: this must be the same as the frontend
    "https://bonoai-frontend.onrender.com",
    "https://www.bonoai.ch",
    "https://bonoai.ch",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/getRisk/")
async def root(request: RiskCalculationRequest) -> RiskCalculationResponse:
    print(request)
    data = request.patient_data.dict()
    data.pop("sex")
    data["bmi"] = round(data["weight"] / ((data["height"] / 100) ** 2), 2)

    risk_horizon = request.risk_horizon * 12

    bono_ai = BonoAI()
    vertebral_result = bono_ai.predict_risk(data, "vertebral", t=risk_horizon)
    hip_result = bono_ai.predict_risk(data, "hip", t=risk_horizon)
    any_result = bono_ai.predict_risk(data, "any", t=risk_horizon)
    risks = FractureRisks(
        vertebral=round(vertebral_result["risk"] * 100, 2),
        hip=round(hip_result["risk"] * 100, 2),
        any=round(any_result["risk"] * 100, 2),
    )
    shap_plots = ShapPlots(
        vertebral=vertebral_result["shap_plot"],
        hip=hip_result["shap_plot"],
        any=any_result["shap_plot"],
    )
    return RiskCalculationResponse(risks=risks, shap_plots=shap_plots)
