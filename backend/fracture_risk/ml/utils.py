import numpy as np
import pandas as pd
import random
import xgboost as xgb
import yaml

from sklearn.preprocessing import StandardScaler


TIME_TO_EVALUATE = 24

# set seeds for reproducibility
random.seed(99)
np.random.seed(99)


def prepare_labels(df, model_type):
    FX_TYPES = ["vertebral", "hip", "any"]
    if model_type == "aft":
        # Create lower and upper bounds for AFT
        for idx in df.index:
            for fx_type in FX_TYPES:
                time_to_event = df.loc[idx, fx_type + "_fracture"]
                if df.loc[idx, fx_type + "_right_censored"] == 0:
                    df.loc[idx, fx_type + "_lower_bound"] = time_to_event
                    df.loc[idx, fx_type + "_upper_bound"] = time_to_event
                else:
                    df.loc[idx, fx_type + "_lower_bound"] = time_to_event
                    df.loc[idx, fx_type + "_upper_bound"] = np.inf
        return df.loc[:, "vertebral_lower_bound":"any_upper_bound"]

    elif model_type == "cox":
        # Make censored values negative
        for idx in df.index:
            for fx_type in FX_TYPES:
                censored = df.loc[idx, fx_type + "_right_censored"]
                tte = df.loc[idx, fx_type + "_fracture"]
                if censored:
                    df.loc[idx, fx_type + "_label"] = -tte
                else:
                    df.loc[idx, fx_type + "_label"] = tte
        return df.loc[:, "vertebral_label":"any_label"]
    else:
        # Select and transform y's
        fractures = {}
        for fx_type in FX_TYPES:
            y = df.loc[:, [f"{fx_type}_right_censored", f"{fx_type}_fracture"]]
            y[f"{fx_type}_right_censored"] = y[f"{fx_type}_right_censored"].apply(
                lambda x: not x
            )
            y = [(e1, e2) for e1, e2 in y.to_numpy()]
            y = np.array(
                y, dtype=[("Event_observed", "?"), ("Survival_in_months", "<f8")]
            )
            fractures[f"{fx_type}_label"] = y
        return fractures


def prepare_data(
    data,
    fx_type,
    scaler=None,
    only_first_visits=False,
    feature_list=[],
    model_type=None,
    standardize=False,
):
    if only_first_visits:
        data = data.groupby("patientId").first().reset_index()
    data = data[data["postmenopausal"] == 1]
    data = data.dropna()

    # Prepare labels for xgboost
    labels = prepare_labels(
        data.loc[:, "vertebral_fracture":"any_right_censored"].copy(), model_type
    )

    non_meaningful_features = [
        "patientId",
        "centerId",
        "date",
        "sex",
        "height",
        "weight",
        "postmenopausal",
        "praemenopausal",
        "num_visits",
        "tscore_ls_imputed",
        "tscore_neck_imputed",
        "tscore_totalHip_imputed",
        "tbs_ls_imputed",
        "prostate_cancer",
        "hypogonadismus_mann",
        "hiv positiv",
        "death_by_osteoporosis",
        "deathdate",
        "Romosozumab_prior",
        "Romosozumab_current",
        "Romosozumab_new",
        "malfunction_of_kidney",
        "wrist_fracture",
        "wrist_right_censored",
    ]

    # Feature Engineering
    data["min_tscore"] = data[["tscore_ls", "tscore_totalHip", "tscore_neck"]].min(
        axis=1
    )

    fracture_columns = [
        "vertebral_fracture",
        "hip_fracture",
        "any_fracture",
        "vertebral_right_censored",
        "hip_right_censored",
        "any_right_censored",
    ]

    if standardize:
        # Standardize values
        continuous_variables = [
            "bmi",
            "steroid_daily_dosage",
            "number_of_falls",
            "age",
            "tscore_ls",
            "tscore_neck",
            "tscore_totalHip",
            "min_tscore",
            "tbs_ls",
            "recent_fracture",
            "previous_fracture",
        ]
        if scaler is None:
            scaler = StandardScaler()
            scaler.fit(data[continuous_variables])
        data[continuous_variables] = scaler.transform(data[continuous_variables])

    # Feature Selection
    if len(feature_list) > 0:
        X = data[feature_list].copy()
    else:
        X = data.drop(non_meaningful_features + fracture_columns, axis=1)

    # Define return dictionary
    prepared_data = {"X": X, "scaler": scaler}
    if model_type == "aft":
        prepared_data["y_lower_bound"] = labels[f"{fx_type}_lower_bound"]
        prepared_data["y_upper_bound"] = labels[f"{fx_type}_upper_bound"]

    else:
        prepared_data["y"] = labels[f"{fx_type}_label"]

    return prepared_data


def censor_after(y, t=TIME_TO_EVALUATE):
    y_copy = y.copy()
    larger_than_t = y_copy["Survival_in_months"] > t
    y_copy["Event_observed"][larger_than_t] = 0
    return y_copy


def reshape_y_from_dmatrix(dmatrix, model_type, censored_after=0):
    """
    Reshape y from DMarix into a numpy array of tuples.
    The tuples are of the form (event_observed, survival_in_months)
    """
    if model_type == "aft":
        lower_bounds = dmatrix.get_float_info("label_lower_bound")
        upper_bounds = dmatrix.get_float_info("label_upper_bound")
        y = pd.DataFrame(
            {
                "Event_observed": np.where(upper_bounds < np.inf, 1, 0),
                "Survival_in_months": lower_bounds,
            }
        )

    elif model_type == "cox":
        labels = dmatrix.get_label()
        y = pd.DataFrame(
            {
                "Event_observed": pd.Series(labels).apply(lambda x: 1 if x > 0 else 0),
                "Survival_in_months": np.abs(labels),
            }
        )

    # Create structured array
    y = [(e1, e2) for e1, e2 in y.to_numpy()]
    y = np.array(y, dtype=[("Event_observed", "?"), ("Survival_in_months", "<f8")])

    if censored_after > 0:
        return censor_after(y, t=censored_after)
    return y


def create_dmatrix(prep_data, model_type):
    X = prep_data["X"]
    dmatrix = xgb.DMatrix(X.values, feature_names=X.columns.tolist())
    if model_type == "aft":
        dmatrix.set_float_info("label_lower_bound", prep_data["y_lower_bound"])
        dmatrix.set_float_info("label_upper_bound", prep_data["y_upper_bound"])
    elif model_type == "cox":
        dmatrix.set_label(prep_data["y"])
    return dmatrix


def produce_stats(df, c_index_scores, auc_scores, t=TIME_TO_EVALUATE):
    # Extract fx type
    fx_type = list(c_index_scores["train"].keys())[0].split("_")[0]

    for tv in ["train", "valid"]:
        harrel_global = round(
            np.mean(c_index_scores[tv][f"{fx_type}_harrel_global"]), 4
        )
        harrel_2y = round(np.mean(c_index_scores[tv][f"{fx_type}_harrel"]), 4)
        uno_2y = round(np.mean(c_index_scores[tv][f"{fx_type}_uno"]), 4)

        df.loc[(fx_type, tv), "harrel_global"] = harrel_global
        df.loc[(fx_type, tv), "harrel_2y"] = harrel_2y
        df.loc[(fx_type, tv), "uno_2y"] = uno_2y

        print("-" * 13 + f" {tv} " + "-" * 13)
        print("Harrels C-Index (Global):", harrel_global)
        print(f"Harrels C-Index (at t={t}):", harrel_2y)
        print("Unos C-Index:", uno_2y)

    auc_2y = round(np.mean(auc_scores[fx_type], axis=0)[t // 12 - 1], 4)
    auc_mean = round(np.mean(auc_scores[f"{fx_type}_mean"]), 4)
    df.loc[(fx_type, "valid"), "auc_2y"] = auc_2y
    df.loc[(fx_type, "valid"), "auc_mean"] = auc_mean
    print(f"AUC at {t//12}y:", auc_2y)
    print("Mean AUC:", auc_mean)

    return df


def provide_stratified_bootstap_sample_indices(bs_sample, fx_type):
    fx_type = fx_type + "_right_censored"
    strata = bs_sample.loc[:, fx_type].value_counts()
    bs_index_list_stratified = []

    for idx_stratum_var, n_stratum_var in strata.iteritems():
        data_index_stratum = list(
            bs_sample[bs_sample[fx_type] == idx_stratum_var].index
        )
        bs_index_list_stratified.extend(
            random.choices(data_index_stratum, k=len(data_index_stratum))
        )

    return bs_index_list_stratified


def get_confidence_interval(arr, alpha, decimals=4, ax=None):
    lower = np.percentile(arr, ((1.0 - alpha) / 2.0) * 100, axis=ax)
    upper = np.percentile(arr, (alpha + ((1.0 - alpha) / 2.0)) * 100, axis=ax)
    if ax is None:
        lower = round(lower, decimals)
        upper = round(upper, decimals)
    return lower, upper


def load_params(model, constraints=False):
    path = "config/ml_model_config.yaml"
    with open(path, "r") as f:
        params = yaml.safe_load(f)

    model_params = params["xgboost"]["all_visits"][model]
    monotonic_params = model_params.pop("monotonic")
    if constraints:
        return monotonic_params
    else:
        return model_params
