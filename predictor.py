import joblib
import pandas as pd

MODEL_PATH = "models/best_price_model.pkl"
model = joblib.load(MODEL_PATH)

print("ML price-per-sqft model loaded ✅")


def predict_price_per_sqft(input_dict):
    """
    Low-level ML prediction (already trained)
    """
    df = pd.DataFrame([input_dict])
    df = pd.get_dummies(df)
    df = df.reindex(columns=model.feature_names_in_, fill_value=0)
    return model.predict(df)[0]


def predict_properties(user_inputs: dict) -> pd.DataFrame:
    """
    High-level business prediction used by Flask + LLM
    """
    df = pd.read_csv("data/structured/real_estate_data.csv")  # unified dataset

    results = []

    for _, row in df.iterrows():
        model_input = {
            "City": row["City"],
            "Locality": row["Locality"],
            "Distance_to_metro_km": row["Distance_to_metro_km"],
            "Property_Type": row["Property_Type"],
            "Age_years": row.get("Age_years", 5),  # default if missing
            "Amenities_score": row.get("Amenities_score", 5),
            "Size_sqft": user_inputs["size"]
        }

        price_per_sqft = predict_price_per_sqft(model_input)
        total_price = (price_per_sqft * user_inputs["size"]) / 1e7  # → Cr

        if total_price <= user_inputs["budget"] * 1.25:
            results.append({
                "City": row["City"],
                "Locality": row["Locality"],
                "Size_sqft": user_inputs["size"],  # ensure present for prompt
                "Predicted_Total_Cr": round(total_price, 2),
                "Distance_to_metro_km": row["Distance_to_metro_km"]
            })

    return pd.DataFrame(results)