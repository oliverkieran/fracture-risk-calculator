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
        bono_ai.prepare_data(data)
        vertebral_risk = bono_ai.predict_risk("vertebral", t=risk_horizon)
        hip_risk = bono_ai.predict_risk("hip", t=risk_horizon)
        any_risk = bono_ai.predict_risk("any", t=risk_horizon)

        print(
            f"API call took {round((datetime.datetime.now() - now).total_seconds(), 2)} seconds."
        )
        return Response(
            {
                "message": "Risk score successfully calculated.",
                "risks": {
                    "vertebral": round(vertebral_risk * 100, 2),
                    "hip": round(hip_risk * 100, 2),
                    "any": round(any_risk * 100, 2),
                },
            }
        )
    else:
        print("Errors:", serializer.errors)
        return Response(serializer.errors)


@api_view(["POST"])
def getShapPlot(request):
    serializer = PatientSerializer(data=request.data["patientData"])
    fx_type = request.data["fxType"]

    if serializer.is_valid():
        data = serializer.validated_data
        print("Data:", data)
        data.pop("sex")  # remove not needed feature
        data["bmi"] = round(data["weight"] / ((data["height"] / 100) ** 2), 2)

        bono_ai = BonoAI()
        prepared_data = bono_ai.prepare_data(data)
        shap_data = bono_ai.create_shap_waterfall(prepared_data, fx_type)

        print("SHAP plot created.")

        return Response(
            {
                "message": "SHAP plot successfully created.",
                "shap_plot": shap_data,
            }
        )
    else:
        print("Errors:", serializer.errors)
        return Response(serializer.errors)
