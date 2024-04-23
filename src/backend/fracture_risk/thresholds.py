# Step 1: Define the table
MOF_thresholds_table = [
    {"age": 40, "LAT": 2.9, "UAT": 7.8, "VHRT": 10.3},
    {"age": 45, "LAT": 3.0, "UAT": 8.0, "VHRT": 10.6},
    {"age": 50, "LAT": 4.2, "UAT": 10.9, "VHRT": 14.6},
    {"age": 55, "LAT": 5.3, "UAT": 13.3, "VHRT": 17.7},
    {"age": 60, "LAT": 6.1, "UAT": 15.0, "VHRT": 20.0},
    {"age": 65, "LAT": 8.5, "UAT": 19.9, "VHRT": 26.5},
    {"age": 70, "LAT": 11.6, "UAT": 25.6, "VHRT": 34.1},
]


def _get_risk_threshold(lower_bound, upper_bound, age_ratio):
    return lower_bound + (upper_bound - lower_bound) * age_ratio


def get_risk_category(age, risk_score, time_horizon=10):
    risk_score = risk_score * 100 * (10 / time_horizon)
    for i, row in enumerate(MOF_thresholds_table):
        if age > row["age"]:
            continue
        if i == 0:
            lower_bounds = {"age": 40, "LAT": 0, "UAT": 0, "VHRT": 0}
            upper_bounds = MOF_thresholds_table[i]
        elif i == len(MOF_thresholds_table) - 1:
            lower_bounds = MOF_thresholds_table[i]
            upper_bounds = {"age": 70, "LAT": 100, "UAT": 100, "VHRT": 100}
        else:
            lower_bounds = MOF_thresholds_table[i - 1]
            upper_bounds = MOF_thresholds_table[i]

        if lower_bounds["age"] != upper_bounds["age"]:
            age_ratio = (age - lower_bounds["age"]) / (
                upper_bounds["age"] - lower_bounds["age"]
            )
        elif upper_bounds["age"] == 40:
            age_ratio = 1
        else:
            age_ratio = 0

        if risk_score < _get_risk_threshold(
            lower_bounds["LAT"], upper_bounds["LAT"], age_ratio
        ):
            return "Low risk"
        elif risk_score < _get_risk_threshold(
            lower_bounds["UAT"], upper_bounds["UAT"], age_ratio
        ):
            return "Moderate risk"
        elif risk_score < _get_risk_threshold(
            lower_bounds["VHRT"], upper_bounds["VHRT"], age_ratio
        ):
            return "High risk"
        else:
            return "Very high risk"


get_risk_category(age=70, risk_score=0.052, time_horizon=2)
