import pandas as pd
from predictor import predict_price_per_sqft

DATA_PATH = "data/structured/real_estate_data.csv"

df = pd.read_csv(DATA_PATH)


def recommend_properties(
    budget_cr,
    size_sqft,
    near_metro=True,
    preferred_city=None,
    min_ppsf=5000
):
    """
    Budget-based property recommendation engine
    """

    df_copy = df.copy()

    # -----------------------
    # Optional city filter
    # -----------------------
    if preferred_city:
        df_copy = df_copy[df_copy["City"].str.lower() == preferred_city.lower()]

    # -----------------------
    # Metro proximity filter
    # -----------------------
    if near_metro:
        df_copy = df_copy[df_copy["Distance_to_metro_km"] <= 2]

    # -----------------------
    # Predict Price per Sqft
    # -----------------------
    df_copy["Predicted_PPSF"] = df_copy.apply(
        lambda row: predict_price_per_sqft({
            "City": row["City"],
            "Locality": row["Locality"],
            "Size_sqft": size_sqft,
            "Age_years": row["Age_years"],
            "Distance_to_metro_km": row["Distance_to_metro_km"],
            "Amenities_score": row["Amenities_score"],
            "Property_Type": row["Property_Type"]
        }),
        axis=1
    )

    # -----------------------
    # Realism guardrail
    # -----------------------
    df_copy = df_copy[df_copy["Predicted_PPSF"] >= min_ppsf]

    # -----------------------
    # Total price calculation
    # -----------------------
    df_copy["Predicted_Total_Cr"] = (
        df_copy["Predicted_PPSF"] * size_sqft
    ) / 1e7

    # -----------------------
    # Budget filter
    # -----------------------
    df_copy = df_copy[df_copy["Predicted_Total_Cr"] <= budget_cr]

    # -----------------------
    # Rank & return
    # -----------------------
    return (
        df_copy
        .sort_values("Predicted_Total_Cr")
        .head(5)
        .reset_index(drop=True)
    )