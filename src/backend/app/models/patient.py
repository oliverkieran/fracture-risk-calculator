"""
Pydantic models for patient data validation and API contracts
"""
from typing import Literal
from pydantic import BaseModel, Field, field_validator, ConfigDict


class PatientData(BaseModel):
    """Patient data model with comprehensive validation"""

    # Demographics
    sex: Literal["female", "male"] = Field(
        default="female",
        description="Patient sex"
    )
    age: int = Field(
        ge=0,
        le=120,
        description="Patient age in years"
    )
    height: int = Field(
        ge=100,
        le=250,
        description="Height in centimeters"
    )
    weight: int = Field(
        ge=20,
        le=300,
        description="Weight in kilograms"
    )

    # Medical history - Boolean fields
    hip_fracture_parents: bool = Field(
        default=False,
        description="History of hip fracture in parents"
    )
    osteoporotic_fracture_parents: bool = Field(
        default=False,
        description="History of osteoporotic fracture in parents"
    )
    corticosteroids: bool = Field(
        default=False,
        description="Corticosteroid use"
    )
    aromatase_inhibitors: bool = Field(
        default=False,
        description="Aromatase inhibitor use"
    )
    antiepileptics: bool = Field(
        default=False,
        description="Antiepileptic medication use"
    )
    rheumatoid_arthritis: bool = Field(
        default=False,
        description="Rheumatoid arthritis diagnosis"
    )
    ankylosing_spondylitis: bool = Field(
        default=False,
        description="Ankylosing spondylitis diagnosis"
    )
    immobility: bool = Field(
        default=False,
        description="Immobility condition"
    )
    type_1_diabetes: bool = Field(
        default=False,
        description="Type 1 diabetes diagnosis"
    )
    copd: bool = Field(
        default=False,
        description="COPD diagnosis"
    )
    gastrointestinal_disease: bool = Field(
        default=False,
        description="Gastrointestinal disease"
    )
    early_menopause: bool = Field(
        default=False,
        description="Early menopause (before age 45)"
    )
    hyperpara: bool = Field(
        default=False,
        description="Hyperparathyroidism"
    )
    falling_test_abnormal: bool = Field(
        default=False,
        description="Abnormal falling test result"
    )
    alcohol: bool = Field(
        default=False,
        description="Excessive alcohol consumption"
    )
    nicotin: bool = Field(
        default=False,
        description="Nicotine use"
    )
    decrease_in_height: bool = Field(
        default=False,
        description="Documented decrease in height"
    )
    low_back_pain: bool = Field(
        default=False,
        description="Chronic low back pain"
    )
    hyperkyphosis: bool = Field(
        default=False,
        description="Hyperkyphosis (excessive spine curvature)"
    )

    # Medical history - Numeric fields
    steroid_daily_dosage: int = Field(
        ge=0,
        le=100,
        default=0,
        description="Daily steroid dosage in mg"
    )
    number_of_falls: int = Field(
        ge=0,
        le=50,
        default=0,
        description="Number of falls in past year"
    )
    previous_fracture: int = Field(
        ge=0,
        le=20,
        default=0,
        description="Number of previous fractures"
    )
    recent_fracture: int = Field(
        ge=0,
        le=20,
        default=0,
        description="Number of recent fractures (past 2 years)"
    )

    # Bone mineral density measurements (T-scores)
    tscore_neck: float = Field(
        ge=-10.0,
        le=10.0,
        description="T-score for femoral neck"
    )
    tscore_total_hip: float = Field(
        ge=-10.0,
        le=10.0,
        description="T-score for total hip"
    )
    tscore_ls: float = Field(
        ge=-10.0,
        le=10.0,
        description="T-score for lumbar spine"
    )
    tbs: float = Field(
        ge=-10.0,
        le=10.0,
        description="Trabecular bone score"
    )

    # Treatment history - Bisphosphonates
    bisphosphonate_prior: bool = Field(
        default=False,
        description="Prior bisphosphonate treatment"
    )
    bisphosphonate_current: bool = Field(
        default=False,
        description="Current bisphosphonate treatment"
    )
    bisphosphonate_new: bool = Field(
        default=False,
        description="Newly started bisphosphonate treatment"
    )

    # Treatment history - Denosumab
    denosumab_prior: bool = Field(
        default=False,
        description="Prior denosumab treatment"
    )
    denosumab_current: bool = Field(
        default=False,
        description="Current denosumab treatment"
    )
    denosumab_new: bool = Field(
        default=False,
        description="Newly started denosumab treatment"
    )

    # Treatment history - SERM
    serm_prior: bool = Field(
        default=False,
        description="Prior SERM treatment"
    )
    serm_current: bool = Field(
        default=False,
        description="Current SERM treatment"
    )
    serm_new: bool = Field(
        default=False,
        description="Newly started SERM treatment"
    )

    # Treatment history - Teriparatide
    teriparatide_prior: bool = Field(
        default=False,
        description="Prior teriparatide treatment"
    )
    teriparatide_current: bool = Field(
        default=False,
        description="Current teriparatide treatment"
    )
    teriparatide_new: bool = Field(
        default=False,
        description="Newly started teriparatide treatment"
    )

    # Treatment history - HRT
    hrt_prior: bool = Field(
        default=False,
        description="Prior hormone replacement therapy"
    )
    hrt_current: bool = Field(
        default=False,
        description="Current hormone replacement therapy"
    )
    hrt_new: bool = Field(
        default=False,
        description="Newly started hormone replacement therapy"
    )

    @field_validator("recent_fracture")
    @classmethod
    def validate_recent_fractures(cls, v: int, info) -> int:
        """Validate that recent fractures don't exceed previous fractures"""
        if "previous_fracture" in info.data:
            previous = info.data["previous_fracture"]
            if v > previous:
                raise ValueError(
                    f"Recent fractures ({v}) cannot exceed previous fractures ({previous})"
                )
        return v

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "sex": "female",
                "age": 65,
                "height": 165,
                "weight": 60,
                "hip_fracture_parents": False,
                "osteoporotic_fracture_parents": False,
                "corticosteroids": False,
                "steroid_daily_dosage": 0,
                "antiepileptics": False,
                "number_of_falls": 0,
                "previous_fracture": 1,
                "recent_fracture": 0,
                "tscore_neck": -2.5,
                "tscore_total_hip": -2.0,
                "tscore_ls": -1.5,
                "tbs": 1.2,
            }
        }
    )


class RiskRequest(BaseModel):
    """Request model for risk calculation endpoint"""

    riskHorizon: int = Field(
        ge=1,
        le=7,
        description="Time horizon for risk prediction in years (1-7)"
    )
    patientData: PatientData = Field(
        description="Complete patient data for risk assessment"
    )

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "riskHorizon": 2,
                "patientData": {
                    "sex": "female",
                    "age": 65,
                    "height": 165,
                    "weight": 60,
                    "tscore_neck": -2.5,
                    "tscore_total_hip": -2.0,
                    "tscore_ls": -1.5,
                    "tbs": 1.2,
                }
            }
        }
    )


class RiskResponse(BaseModel):
    """Response model for risk calculation endpoint"""

    message: str = Field(
        description="Status message"
    )
    risks: dict[str, float] = Field(
        description="Calculated fracture risks (vertebral, hip, any)"
    )

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "message": "Risk score successfully calculated.",
                "risks": {
                    "vertebral": 2.15,
                    "hip": 1.45,
                    "any": 8.23
                }
            }
        }
    )


class ShapPlotRequest(BaseModel):
    """Request model for SHAP plot generation endpoint"""

    riskHorizon: int = Field(
        ge=1,
        le=7,
        description="Time horizon for risk prediction in years (1-7)"
    )
    patientData: PatientData = Field(
        description="Complete patient data for SHAP analysis"
    )
    fxType: Literal["vertebral", "hip", "any"] = Field(
        description="Fracture type for SHAP plot"
    )

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "riskHorizon": 2,
                "patientData": {"sex": "female", "age": 65},
                "fxType": "any"
            }
        }
    )


class ShapPlotResponse(BaseModel):
    """Response model for SHAP plot generation endpoint"""

    message: str = Field(
        description="Status message"
    )
    shap_plot: str = Field(
        description="Base64 encoded PNG image of SHAP waterfall plot"
    )

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "message": "SHAP plot successfully created.",
                "shap_plot": "iVBORw0KGgoAAAANSUhEUgAA..."
            }
        }
    )
