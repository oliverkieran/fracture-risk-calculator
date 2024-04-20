import io
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import pickle
import os
import shap
import xgboost as xgb

# Agg, is a non-interactive backend that can only write to files
# for more info see: https://matplotlib.org/stable/users/explain/backends.html
matplotlib.use("agg")


class BonoAI:
    def __init__(self):
        self.models = self.load_models()
        self.times = np.arange(12, 95, 12)

    def load_models(self):
        models = {"xgb": {}, "cox": {}}
        base_path = os.path.dirname(os.path.realpath(__file__))

        for fx_type in ["vertebral", "hip", "any"]:
            xgb_model = xgb.Booster()
            xgb_path = os.path.join(base_path, f"models/{fx_type}_xgb.json")
            xgb_model.load_model(xgb_path)
            models["xgb"][fx_type] = xgb_model

            cox_path = os.path.join(base_path, f"models/{fx_type}_cox.pkl")
            with open(cox_path, "rb") as file:
                models["cox"][fx_type] = pickle.load(file)

        return models

    def prepare_data(self, data, features):
        patient_data = pd.Series(data, dtype="float64")

        # convert bool values to int
        """ for key in patient_data.keys():
            if type(patient_data[key]) == bool:
                patient_data[key] = int(patient_data[key]) """

        if patient_data[["hrt_prior", "hrt_current"]].sum() > 0:
            patient_data["hrt"] = 1
        else:
            patient_data["hrt"] = 0

        # rename features
        name_translations = {
            "antiepileptics": "antiepileptic_drugs",
            "tscore_total_hip": "tscore_totalHip",
            "tbs": "tbs_ls",
            "bisphosphonate_prior": "Bisphosphonat_prior",
            "bisphosphonate_current": "Bisphosphonat_current",
            "bisphosphonate_new": "Bisphosphonat_new",
            "denosumab_prior": "Denosumab_prior",
            "denosumab_current": "Denosumab_current",
            "denosumab_new": "Denosumab_new",
            "serm_prior": "SERM_prior",
            "serm_current": "SERM_current",
            "serm_new": "SERM_new",
            "hrt_prior": "HRT_prior",
            "hrt_current": "HRT_current",
            "hrt_new": "HRT_new",
            "teriparatide_prior": "Teriparatide_prior",
            "teriparatide_current": "Teriparatide_current",
            "teriparatide_new": "Teriparatide_new",
        }
        patient_data = patient_data.rename(name_translations)

        # calculate min tscore
        patient_data["min_tscore"] = patient_data[
            ["tscore_neck", "tscore_totalHip", "tscore_ls"]
        ].min()

        # add No treatment feature
        patient_data["No_treatment"] = int(
            patient_data.loc["Bisphosphonat_prior":"HRT_new"].sum() == 0
        )
        # sort features the same way as in the xgb model
        xgb_features = features
        patient_data = patient_data[xgb_features]

        return patient_data

    def predict_risk(self, data, fx_type, t=24, shap=False):
        xgb_model = self.models["xgb"][fx_type]
        cox_model = self.models["cox"][fx_type]

        prepared_data = self.prepare_data(data, xgb_model.feature_names)

        xgb_data = xgb.DMatrix(
            prepared_data.values.reshape(1, -1),
            feature_names=prepared_data.index.tolist(),
        )
        xgb_pred = xgb_model.predict(xgb_data)

        survival_function = cox_model.predict_survival_function(xgb_pred.reshape(-1, 1))
        fracture_proba = 1 - survival_function[0](t)

        print(fx_type, fracture_proba)

        if shap:
            self.create_shap_waterfall(xgb_model, prepared_data, fx_type)
        return fracture_proba

    def create_shap_waterfall(self, model, data, fx_type):
        explainer = shap.Explainer(model)
        patient_data = pd.DataFrame(data).T
        shap_values = explainer(patient_data)
        fig = shap.plots.waterfall(shap_values[0], show=False)

        # Save plot to S3 bucket
        img_data = io.BytesIO()
        plt.savefig(img_data, format="png", bbox_inches="tight")
        img_data.seek(0)

        print(f"{fx_type}: SHAP waterfall plot saved.")


# FOR TESTING PURPOSES

# bono_ai = BonoAI()
# data = {
#     "sex": "female",
#     "age": 65,
#     "bmi": 25.0,
#     "hip_fracture_parents": True,
#     "osteoporotic_fracture_parents": False,
#     "corticosteroids": False,
#     "steroid_daily_dosage": 0,
#     "aromatase_inhibitors": False,
#     "antiepileptics": False,
#     "rheumatoid_arthritis": False,
#     "ankylosing_spondylitis": False,
#     "number_of_falls": 0,
#     "immobility": False,
#     "type_1_diabetes": False,
#     "copd": False,
#     "gastrointestinal_disease": False,
#     "early_menopause": False,
#     "hyperpara": False,
#     "falling_test_abnormal": False,
#     "alcohol": False,
#     "nicotin": False,
#     "decrease_in_height": False,
#     "low_back_pain": False,
#     "hyperkyphosis": False,
#     "previous_fracture": 0,
#     "recent_fracture": 0,
#     "tscore_neck": -2,
#     "tscore_total_hip": -2,
#     "tscore_ls": -2,
#     "tbs": 1.3,
#     "bisphosphonate_prior": False,
#     "bisphosphonate_current": False,
#     "bisphosphonate_new": False,
#     "denosumab_prior": False,
#     "denosumab_current": False,
#     "denosumab_new": False,
#     "serm_prior": False,
#     "serm_current": False,
#     "serm_new": False,
#     "teriparatide_prior": False,
#     "teriparatide_current": False,
#     "teriparatide_new": False,
#     "hrt_prior": True,
#     "hrt_current": False,
#     "hrt_new": False,
# }

# print("Vertebral Fracture Risk:", bono_ai.predict_risk(data, "vertebral", t=24))
# print("Hip Fracture Risk:", bono_ai.predict_risk(data, "hip", t=24))
# print("Any Fracture Risk:", bono_ai.predict_risk(data, "any", t=24))
