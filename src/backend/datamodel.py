from pydantic import BaseModel, Field
from typing import Optional


class PatientInfo(BaseModel):
    sex: str = Field(
        ..., pattern="^(female|male)$", description="The sex of the patient"
    )
    age: int = Field(..., gt=0, description="The age of the patient")
    height: int = Field(..., gt=0, description="The height of the patient")
    weight: int = Field(..., gt=0, description="The weight of the patient")
    bmi: Optional[float] = Field(None, description="The body mass index of the patient")
    hip_fracture_parents: bool = Field(
        ..., description="Whether the patient's parents have a history of hip fractures"
    )
    osteoporotic_fracture_parents: bool = Field(
        ...,
        description="Whether the patient's parents have a history of osteoporotic fractures",
    )
    corticosteroids: bool = Field(
        ..., description="Whether the patient is taking corticosteroids"
    )
    steroid_daily_dosage: int = Field(
        ...,
        ge=0,
        description="The daily dosage of corticosteroids taken by the patient",
    )
    aromatase_inhibitors: bool = Field(
        ..., description="Whether the patient is taking aromatase inhibitors"
    )
    antiepileptics: bool = Field(
        ..., description="Whether the patient is taking antiepileptics"
    )
    rheumatoid_arthritis: bool = Field(
        ..., description="Whether the patient has rheumatoid arthritis"
    )
    ankylosing_spondylitis: bool = Field(
        ..., description="Whether the patient has ankylosing spondylitis"
    )
    number_of_falls: int = Field(
        ..., ge=0, description="The number of falls the patient has experienced"
    )
    immobility: bool = Field(..., description="Whether the patient is immobile")
    type_1_diabetes: bool = Field(
        ..., description="Whether the patient has type 1 diabetes"
    )
    copd: bool = Field(
        ..., description="Whether the patient has chronic obstructive pulmonary disease"
    )
    gastrointestinal_disease: bool = Field(
        ..., description="Whether the patient has gastrointestinal disease"
    )
    early_menopause: bool = Field(
        ..., description="Whether the patient has experienced early menopause"
    )
    hyperpara: bool = Field(
        ..., description="Whether the patient has hyperparathyroidism"
    )
    falling_test_abnormal: bool = Field(
        ..., description="Whether the patient's falling test results are abnormal"
    )
    alcohol: bool = Field(..., description="Whether the patient consumes alcohol")
    nicotin: bool = Field(..., description="Whether the patient consumes nicotine")
    decrease_in_height: bool = Field(
        ..., description="Whether the patient has experienced a decrease in height"
    )
    low_back_pain: bool = Field(
        ..., description="Whether the patient has experienced low back pain"
    )
    hyperkyphosis: bool = Field(
        ..., description="Whether the patient has hyperkyphosis"
    )
    previous_fracture: int = Field(
        ...,
        ge=0,
        description="The number of previous fractures the patient has experienced",
    )
    recent_fracture: int = Field(
        ...,
        ge=0,
        description="The number of recent fractures the patient has experienced",
    )
    tscore_neck: float = Field(..., description="The T-score of the patient's neck")
    tscore_total_hip: float = Field(
        ..., description="The T-score of the patient's total hip"
    )
    tscore_ls: float = Field(
        ..., description="The T-score of the patient's lumbar spine"
    )
    tbs: float = Field(
        ..., gt=0, description="The trabecular bone score of the patient"
    )
    bisphosphonate_prior: bool = Field(
        ..., description="Whether the patient has taken bisphosphonates in the past"
    )
    bisphosphonate_current: bool = Field(
        ..., description="Whether the patient is currently taking bisphosphonates"
    )
    bisphosphonate_new: bool = Field(
        ...,
        description="Whether the patient has recently started taking bisphosphonates",
    )
    denosumab_prior: bool = Field(
        ..., description="Whether the patient has taken denosumab in the past"
    )
    denosumab_current: bool = Field(
        ..., description="Whether the patient is currently taking denosumab"
    )
    denosumab_new: bool = Field(
        ..., description="Whether the patient has recently started taking denosumab"
    )
    serm_prior: bool = Field(
        ...,
        description="Whether the patient has taken selective estrogen receptor modulators in the past",
    )
    serm_current: bool = Field(
        ...,
        description="Whether the patient is currently taking selective estrogen receptor modulators",
    )
    serm_new: bool = Field(
        ...,
        description="Whether the patient has recently started taking selective estrogen receptor modulators",
    )
    teriparatide_prior: bool = Field(
        ..., description="Whether the patient has taken teriparatide in the past"
    )
    teriparatide_current: bool = Field(
        ..., description="Whether the patient is currently taking teriparatide"
    )
    teriparatide_new: bool = Field(
        ..., description="Whether the patient has recently started taking teriparatide"
    )
    hrt_prior: bool = Field(
        ...,
        description="Whether the patient has taken hormone replacement therapy in the past",
    )
    hrt_current: bool = Field(
        ...,
        description="Whether the patient is currently taking hormone replacement therapy",
    )
    hrt_new: bool = Field(
        ...,
        description="Whether the patient has recently started taking hormone replacement therapy",
    )

    class Config:
        extra = "forbid"


class FractureRisks(BaseModel):
    vertebral: float = Field(
        ..., ge=0, le=100, description="The risk of vertebral fracture"
    )
    hip: float = Field(..., ge=0, le=100, description="The risk of hip fracture")
    any: float = Field(..., ge=0, le=100, description="The risk of any fracture")

    class Config:
        extra = "forbid"


class ShapPlots(BaseModel):
    vertebral: str = Field(
        ..., description="The SHAP plot for vertebral fracture in base64 format"
    )
    hip: str = Field(..., description="The SHAP plot for hip fracture in base64 format")
    any: str = Field(..., description="The SHAP plot for any fracture in base64 format")

    class Config:
        extra = "forbid"


class RiskCalculationRequest(BaseModel):
    patient_data: PatientInfo
    risk_horizon: int = Field(..., gt=0, description="The risk horizon in years")

    class Config:
        extra = "forbid"


class RiskCalculationResponse(BaseModel):
    risks: FractureRisks
    shap_plots: ShapPlots

    class Config:
        extra = "forbid"
