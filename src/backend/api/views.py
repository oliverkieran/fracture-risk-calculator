import datetime

from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import PatientSerializer
from fracture_risk.ml.risk_calculator import BonoAI


@api_view(["POST"])
def getRisk(request):
    now = datetime.datetime.now()
    serializer = PatientSerializer(data=request.data["patientData"])
    risk_horizon = int(request.data["riskHorizon"]) * 12

    if serializer.is_valid():
        data = serializer.validated_data
        print("Data:", data)
        data.pop("sex")  # remove not needed feature
        data["bmi"] = round(data["weight"] / ((data["height"] / 100) ** 2), 2)

        bono_ai = BonoAI()
        vertebral_risk_prediction = bono_ai.predict_risk(
            data, "vertebral", t=risk_horizon
        )
        hip_risk_prediction = bono_ai.predict_risk(data, "hip", t=risk_horizon)
        any_risk_prediction = bono_ai.predict_risk(data, "any", t=risk_horizon)

        # serializer.save()
        print(
            f"API call took {round((datetime.datetime.now() - now).total_seconds(), 2)} seconds."
        )
        return Response(
            {
                "message": "Risk score successfully calculated.",
                "risks": {
                    "vertebral": round(vertebral_risk_prediction * 100, 2),
                    "hip": round(hip_risk_prediction * 100, 2),
                    "any": round(any_risk_prediction * 100, 2),
                },
            }
        )
    else:
        print("Errors:", serializer.errors)
        return Response(serializer.errors)


@api_view(["POST"])
def getShapPlots(request):
    serializer = PatientSerializer(data=request.data["patientData"])
    risk_horizon = int(request.data["riskHorizon"]) * 12

    if serializer.is_valid():
        data = serializer.validated_data
        print("Data:", data)
        data.pop("sex")  # remove not needed feature
        data["bmi"] = round(data["weight"] / ((data["height"] / 100) ** 2), 2)

        bono_ai = BonoAI()
        prepared_data = bono_ai.prepare_data(
            data, bono_ai.models["xgb"]["any"].feature_names
        )
        vertebral_shap_url = bono_ai.create_shap_waterfall(
            bono_ai.models["xgb"]["vertebral"], prepared_data, "vertebral"
        )
        hip_shap_url = bono_ai.create_shap_waterfall(
            bono_ai.models["xgb"]["hip"], prepared_data, "hip"
        )
        any_shap_url = bono_ai.create_shap_waterfall(
            bono_ai.models["xgb"]["any"], prepared_data, "any"
        )

        print("vertebral:", vertebral_shap_url)
        print("hip:", hip_shap_url)
        print("any:", any_shap_url)

        # serializer.save()
        return Response(
            {
                "message": "SHAP plots successfully created.",
                "shap_plots": {
                    "vertebral": vertebral_shap_url,
                    "hip": hip_shap_url,
                    "any": any_shap_url,
                },
            }
        )
    else:
        print("Errors:", serializer.errors)
        return Response(serializer.errors)
