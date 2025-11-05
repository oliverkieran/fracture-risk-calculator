"""
API endpoint implementations for fracture risk calculation
"""
import logging
from typing import Dict

from fastapi import APIRouter, HTTPException
from app.models import RiskRequest, RiskResponse, ShapPlotRequest, ShapPlotResponse
from app.ml.risk_calculator import BonoAI

# Configure logging
logger = logging.getLogger(__name__)

# Create router
router = APIRouter(prefix="/api", tags=["risk-calculation"])

# Initialize BonoAI once at module level for performance
# This avoids loading models on every request
try:
    bono_ai = BonoAI()
    logger.info("BonoAI model loaded successfully")
except Exception as e:
    logger.error(f"Failed to load BonoAI model: {str(e)}", exc_info=True)
    raise


@router.post("/getRisk/", response_model=RiskResponse)
async def get_risk(request: RiskRequest) -> RiskResponse:
    """
    Calculate fracture risk for a patient

    Given patient demographics, medical history, and bone density measurements,
    this endpoint calculates the probability of vertebral, hip, and any fracture
    occurring within the specified time horizon.

    **Parameters:**
    - **riskHorizon**: Years to predict (1-7)
    - **patientData**: Complete patient data including demographics, medical history,
      bone density measurements, and treatment history

    **Returns:**
    - **risks**: Object containing three risk percentages:
        - vertebral: Risk of vertebral fracture
        - hip: Risk of hip fracture
        - any: Risk of any major osteoporotic fracture

    **Example:**
    ```json
    {
        "riskHorizon": 2,
        "patientData": {
            "sex": "female",
            "age": 65,
            "height": 165,
            "weight": 60,
            "tscore_neck": -2.5,
            ...
        }
    }
    ```
    """
    try:
        logger.info(f"Risk calculation request received for {request.riskHorizon} year horizon")

        # Prepare patient data
        data = request.patientData.model_dump()

        # Remove sex field (not used by model)
        data.pop("sex", None)

        # Calculate BMI
        height_m = data["height"] / 100
        data["bmi"] = round(data["weight"] / (height_m ** 2), 2)

        # Convert risk horizon to months
        risk_horizon_months = request.riskHorizon * 12

        # Prepare data for ML model
        prepared_data = bono_ai.prepare_data(data)

        # Calculate risks for each fracture type
        vertebral_risk = bono_ai.predict_risk("vertebral", t=risk_horizon_months)
        hip_risk = bono_ai.predict_risk("hip", t=risk_horizon_months)
        any_risk = bono_ai.predict_risk("any", t=risk_horizon_months)

        # Convert to percentages and round
        risks = {
            "vertebral": round(vertebral_risk * 100, 2),
            "hip": round(hip_risk * 100, 2),
            "any": round(any_risk * 100, 2),
        }

        logger.info(f"Risk calculated successfully: {risks}")

        return RiskResponse(
            message="Risk score successfully calculated.",
            risks=risks
        )

    except ValueError as e:
        logger.warning(f"Validation error in risk calculation: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))

    except Exception as e:
        logger.error(f"Unexpected error in risk calculation: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail="Internal server error during risk calculation"
        )


@router.post("/getShapPlot/", response_model=ShapPlotResponse)
async def get_shap_plot(request: ShapPlotRequest) -> ShapPlotResponse:
    """
    Generate SHAP waterfall plot for model explainability

    Creates a visualization showing how each patient feature contributes
    to the final fracture risk prediction.

    **Parameters:**
    - **riskHorizon**: Years to predict (1-7)
    - **patientData**: Complete patient data
    - **fxType**: Fracture type ("vertebral", "hip", or "any")

    **Returns:**
    - **shap_plot**: Base64 encoded PNG image of the SHAP waterfall plot

    **Example:**
    ```json
    {
        "riskHorizon": 2,
        "patientData": {...},
        "fxType": "any"
    }
    ```
    """
    try:
        logger.info(f"SHAP plot request received for {request.fxType} fracture type")

        # Prepare patient data
        data = request.patientData.model_dump()

        # Remove sex field (not used by model)
        data.pop("sex", None)

        # Calculate BMI
        height_m = data["height"] / 100
        data["bmi"] = round(data["weight"] / (height_m ** 2), 2)

        # Prepare data for ML model
        prepared_data = bono_ai.prepare_data(data)

        # Generate SHAP waterfall plot
        shap_plot_base64 = bono_ai.create_shap_waterfall(prepared_data, request.fxType)

        logger.info(f"SHAP plot created successfully for {request.fxType}")

        return ShapPlotResponse(
            message="SHAP plot successfully created.",
            shap_plot=shap_plot_base64
        )

    except ValueError as e:
        logger.warning(f"Validation error in SHAP plot generation: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))

    except Exception as e:
        logger.error(f"Unexpected error in SHAP plot generation: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail="Internal server error during SHAP plot generation"
        )
