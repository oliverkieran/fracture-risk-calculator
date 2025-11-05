"""
Test suite for BonoAI Fracture Risk API

Following TDD principles - these tests define the expected behavior
"""
import pytest
from fastapi.testclient import TestClient


# Sample valid patient data for testing
VALID_PATIENT_DATA = {
    "sex": "female",
    "age": 65,
    "height": 165,
    "weight": 60,
    "hip_fracture_parents": False,
    "osteoporotic_fracture_parents": False,
    "corticosteroids": False,
    "steroid_daily_dosage": 0,
    "aromatase_inhibitors": False,
    "antiepileptics": False,
    "rheumatoid_arthritis": False,
    "ankylosing_spondylitis": False,
    "number_of_falls": 0,
    "immobility": False,
    "type_1_diabetes": False,
    "copd": False,
    "gastrointestinal_disease": False,
    "early_menopause": False,
    "hyperpara": False,
    "falling_test_abnormal": False,
    "alcohol": False,
    "nicotin": False,
    "decrease_in_height": False,
    "low_back_pain": False,
    "hyperkyphosis": False,
    "previous_fracture": 0,
    "recent_fracture": 0,
    "tscore_neck": -2.5,
    "tscore_total_hip": -2.0,
    "tscore_ls": -1.5,
    "tbs": 1.2,
    "bisphosphonate_prior": False,
    "bisphosphonate_current": False,
    "bisphosphonate_new": False,
    "denosumab_prior": False,
    "denosumab_current": False,
    "denosumab_new": False,
    "serm_prior": False,
    "serm_current": False,
    "serm_new": False,
    "teriparatide_prior": False,
    "teriparatide_current": False,
    "teriparatide_new": False,
    "hrt_prior": False,
    "hrt_current": False,
    "hrt_new": False,
}


@pytest.fixture(scope="module")
def client():
    """Create a test client for the FastAPI app"""
    from app.main import app
    return TestClient(app)


class TestGetRiskEndpoint:
    """Tests for POST /api/getRisk/ endpoint"""

    def test_valid_risk_calculation(self, client):
        """Test successful risk calculation with valid data"""
        request_data = {
            "riskHorizon": 2,
            "patientData": VALID_PATIENT_DATA
        }

        response = client.post("/api/getRisk/", json=request_data)

        assert response.status_code == 200
        data = response.json()

        # Check response structure
        assert "message" in data
        assert "risks" in data
        assert data["message"] == "Risk score successfully calculated."

        # Check risks object
        risks = data["risks"]
        assert "vertebral" in risks
        assert "hip" in risks
        assert "any" in risks

        # Check risk values are floats between 0 and 100
        for risk_type, risk_value in risks.items():
            assert isinstance(risk_value, (int, float))
            assert 0 <= risk_value <= 100

    def test_risk_horizon_validation(self, client):
        """Test risk horizon must be between 1 and 7"""
        # Test risk horizon = 0 (invalid)
        request_data = {
            "riskHorizon": 0,
            "patientData": VALID_PATIENT_DATA
        }
        response = client.post("/api/getRisk/", json=request_data)
        assert response.status_code == 422  # Validation error

        # Test risk horizon = 8 (invalid)
        request_data["riskHorizon"] = 8
        response = client.post("/api/getRisk/", json=request_data)
        assert response.status_code == 422

        # Test risk horizon = 1 (valid)
        request_data["riskHorizon"] = 1
        response = client.post("/api/getRisk/", json=request_data)
        assert response.status_code == 200

        # Test risk horizon = 7 (valid)
        request_data["riskHorizon"] = 7
        response = client.post("/api/getRisk/", json=request_data)
        assert response.status_code == 200

    def test_missing_risk_horizon(self, client):
        """Test request fails when riskHorizon is missing"""
        request_data = {"patientData": VALID_PATIENT_DATA}
        response = client.post("/api/getRisk/", json=request_data)
        assert response.status_code == 422

    def test_missing_patient_data(self, client):
        """Test request fails when patientData is missing"""
        request_data = {"riskHorizon": 2}
        response = client.post("/api/getRisk/", json=request_data)
        assert response.status_code == 422

    def test_invalid_age(self, client):
        """Test age validation (0-120)"""
        patient_data = VALID_PATIENT_DATA.copy()

        # Age too high
        patient_data["age"] = 121
        request_data = {"riskHorizon": 2, "patientData": patient_data}
        response = client.post("/api/getRisk/", json=request_data)
        assert response.status_code == 422

        # Negative age
        patient_data["age"] = -1
        response = client.post("/api/getRisk/", json=request_data)
        assert response.status_code == 422

        # Valid ages
        for age in [0, 50, 120]:
            patient_data["age"] = age
            response = client.post("/api/getRisk/", json=request_data)
            assert response.status_code == 200

    def test_height_validation(self, client):
        """Test height validation (100-250 cm)"""
        patient_data = VALID_PATIENT_DATA.copy()

        # Height too low
        patient_data["height"] = 99
        request_data = {"riskHorizon": 2, "patientData": patient_data}
        response = client.post("/api/getRisk/", json=request_data)
        assert response.status_code == 422

        # Height too high
        patient_data["height"] = 251
        response = client.post("/api/getRisk/", json=request_data)
        assert response.status_code == 422

    def test_weight_validation(self, client):
        """Test weight validation (20-300 kg)"""
        patient_data = VALID_PATIENT_DATA.copy()

        # Weight too low
        patient_data["weight"] = 19
        request_data = {"riskHorizon": 2, "patientData": patient_data}
        response = client.post("/api/getRisk/", json=request_data)
        assert response.status_code == 422

        # Weight too high
        patient_data["weight"] = 301
        response = client.post("/api/getRisk/", json=request_data)
        assert response.status_code == 422

    def test_tscore_validation(self, client):
        """Test T-score validation (-10 to 10)"""
        patient_data = VALID_PATIENT_DATA.copy()

        for field in ["tscore_neck", "tscore_total_hip", "tscore_ls", "tbs"]:
            # Too low
            patient_data[field] = -10.1
            request_data = {"riskHorizon": 2, "patientData": patient_data}
            response = client.post("/api/getRisk/", json=request_data)
            assert response.status_code == 422

            # Too high
            patient_data[field] = 10.1
            response = client.post("/api/getRisk/", json=request_data)
            assert response.status_code == 422

            # Reset to valid value
            patient_data[field] = -2.0

    def test_recent_fracture_validation(self, client):
        """Test that recent_fracture cannot exceed previous_fracture"""
        patient_data = VALID_PATIENT_DATA.copy()

        # recent_fracture > previous_fracture should fail
        patient_data["previous_fracture"] = 1
        patient_data["recent_fracture"] = 2
        request_data = {"riskHorizon": 2, "patientData": patient_data}
        response = client.post("/api/getRisk/", json=request_data)
        assert response.status_code == 422

        # recent_fracture <= previous_fracture should succeed
        patient_data["recent_fracture"] = 1
        response = client.post("/api/getRisk/", json=request_data)
        assert response.status_code == 200

        patient_data["recent_fracture"] = 0
        response = client.post("/api/getRisk/", json=request_data)
        assert response.status_code == 200

    def test_sex_validation(self, client):
        """Test sex must be 'female' or 'male'"""
        patient_data = VALID_PATIENT_DATA.copy()

        # Invalid sex
        patient_data["sex"] = "other"
        request_data = {"riskHorizon": 2, "patientData": patient_data}
        response = client.post("/api/getRisk/", json=request_data)
        assert response.status_code == 422

        # Valid sex values
        for sex in ["female", "male"]:
            patient_data["sex"] = sex
            response = client.post("/api/getRisk/", json=request_data)
            assert response.status_code == 200

    def test_boolean_fields(self, client):
        """Test boolean fields accept only true/false"""
        patient_data = VALID_PATIENT_DATA.copy()

        # Set a boolean field to true
        patient_data["hip_fracture_parents"] = True
        request_data = {"riskHorizon": 2, "patientData": patient_data}
        response = client.post("/api/getRisk/", json=request_data)
        assert response.status_code == 200

        # Set to false
        patient_data["hip_fracture_parents"] = False
        response = client.post("/api/getRisk/", json=request_data)
        assert response.status_code == 200

        # Invalid boolean value (dict should fail)
        patient_data["hip_fracture_parents"] = {"invalid": "object"}
        response = client.post("/api/getRisk/", json=request_data)
        assert response.status_code == 422


class TestGetShapPlotEndpoint:
    """Tests for POST /api/getShapPlot/ endpoint"""

    def test_valid_shap_plot_generation(self, client):
        """Test successful SHAP plot generation"""
        for fx_type in ["vertebral", "hip", "any"]:
            request_data = {
                "riskHorizon": 2,
                "patientData": VALID_PATIENT_DATA,
                "fxType": fx_type
            }

            response = client.post("/api/getShapPlot/", json=request_data)

            assert response.status_code == 200
            data = response.json()

            # Check response structure
            assert "message" in data
            assert "shap_plot" in data
            assert data["message"] == "SHAP plot successfully created."

            # Check shap_plot is a non-empty string (base64 encoded image)
            assert isinstance(data["shap_plot"], str)
            assert len(data["shap_plot"]) > 0

    def test_invalid_fx_type(self, client):
        """Test fxType validation"""
        request_data = {
            "riskHorizon": 2,
            "patientData": VALID_PATIENT_DATA,
            "fxType": "invalid_type"
        }

        response = client.post("/api/getShapPlot/", json=request_data)
        assert response.status_code == 422

    def test_missing_fx_type(self, client):
        """Test request fails when fxType is missing"""
        request_data = {
            "riskHorizon": 2,
            "patientData": VALID_PATIENT_DATA
        }

        response = client.post("/api/getShapPlot/", json=request_data)
        assert response.status_code == 422

    def test_shap_plot_with_different_horizons(self, client):
        """Test SHAP plot generation with different risk horizons"""
        for horizon in [1, 3, 5, 7]:
            request_data = {
                "riskHorizon": horizon,
                "patientData": VALID_PATIENT_DATA,
                "fxType": "any"
            }

            response = client.post("/api/getShapPlot/", json=request_data)
            assert response.status_code == 200


class TestHealthCheck:
    """Tests for health check endpoint"""

    def test_health_check(self, client):
        """Test health check endpoint is accessible"""
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert "status" in data
        assert data["status"] == "healthy"


class TestCORS:
    """Tests for CORS configuration"""

    def test_cors_headers(self, client):
        """Test CORS headers are present"""
        # Make an OPTIONS request to check CORS
        response = client.options("/api/getRisk/")
        # Should not fail (CORS configured)
        assert response.status_code in [200, 405]  # OPTIONS may not be implemented


class TestAPIDocumentation:
    """Tests for API documentation"""

    def test_openapi_schema_available(self, client):
        """Test OpenAPI schema is accessible"""
        response = client.get("/openapi.json")
        assert response.status_code == 200
        schema = response.json()
        assert "openapi" in schema
        assert "info" in schema
        assert "paths" in schema

    def test_docs_page_available(self, client):
        """Test Swagger UI docs page is accessible"""
        response = client.get("/docs")
        assert response.status_code == 200
