from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import PatientSerializer
from fracture_risk.ml.risk_calculator import BonoAI


@api_view(["POST"])
def getRisk(request):
    serializer = PatientSerializer(data=request.data["patientData"])
    risk_horizon = int(request.data["riskHorizon"]) * 12

    if serializer.is_valid():
        data = serializer.validated_data
        print("Data:", data)
        data.pop("sex")  # remove not needed feature
        data["bmi"] = round(data["weight"] / ((data["height"] / 100) ** 2), 2)

        bono_ai = BonoAI()
        vertebral_risk_prediction = bono_ai.predict_risk(
            data, "vertebral", t=risk_horizon, shap=True
        )
        hip_risk_prediction = bono_ai.predict_risk(
            data, "hip", t=risk_horizon, shap=True
        )
        any_risk_prediction = bono_ai.predict_risk(
            data, "any", t=risk_horizon, shap=True
        )

        # serializer.save()
        return Response(
            {
                "message": "Risk score successfully calculated.",
                "risks": {
                    "vertebral": round(vertebral_risk_prediction["risk"] * 100, 2),
                    "hip": round(hip_risk_prediction["risk"] * 100, 2),
                    "any": round(any_risk_prediction["risk"] * 100, 2),
                },
                "shap_plots": {
                    "vertebral": vertebral_risk_prediction["shap_plot"],
                    "hip": hip_risk_prediction["shap_plot"],
                    "any": any_risk_prediction["shap_plot"],
                },
            }
        )
    else:
        print("Errors:", serializer.errors)
        return Response(serializer.errors)
