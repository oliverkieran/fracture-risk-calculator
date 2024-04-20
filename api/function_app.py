import azure.functions as func
import json
import logging

from ml.risk_calculator import BonoAI

app = func.FunctionApp(http_auth_level=func.AuthLevel.FUNCTION)


@app.route(route="getRisk")
def getRisk(req: func.HttpRequest) -> func.HttpResponse:
    logging.info("Python HTTP trigger function processed a request.")
    try:
        req_body = req.get_json()
        print("BODY: ", req_body)

        risk_horizon = int(req_body["riskHorizon"]) * 12
        data = req_body["patientData"]
        data.pop("sex")  # remove not needed feature
        data["bmi"] = round(data["weight"] / ((data["height"] / 100) ** 2), 2)

        bono_ai = BonoAI()
        vertebral_risk = bono_ai.predict_risk(
            data, "vertebral", t=risk_horizon, shap=False
        )
        hip_risk = bono_ai.predict_risk(data, "hip", t=risk_horizon, shap=False)
        any_risk = bono_ai.predict_risk(data, "any", t=risk_horizon)

        return func.HttpResponse(
            json.dumps(
                {
                    "message": "Risk score successfully calculated.",
                    "risks": {
                        "vertebral": round(vertebral_risk * 100, 2),
                        "hip": round(hip_risk * 100, 2),
                        "any": round(any_risk * 100, 2),
                    },
                }
            ),
            mimetype="application/json",
            status_code=200,
        )
    except ValueError:
        pass
        return func.HttpResponse(
            "This HTTP triggered function executed successfully. Pass a name in the query string or in the request body for a personalized response.",
            status_code=200,
        )
