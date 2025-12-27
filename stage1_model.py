import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
import joblib

from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from sklearn.linear_model import LinearRegression, Ridge
from sklearn.ensemble import RandomForestRegressor

# Try importing XGBoost
try:
    from xgboost import XGBRegressor
    XGBOOST_AVAILABLE = True
except ImportError:
    XGBOOST_AVAILABLE = False

# -----------------------
# Paths
# -----------------------
DATA_PATH = "data/structured/real_estate_data.csv"
MODEL_DIR = "models"
FIG_PATH = "reports/figures"

os.makedirs(MODEL_DIR, exist_ok=True)
os.makedirs(FIG_PATH, exist_ok=True)

# -----------------------
# Load data
# -----------------------
df = pd.read_csv(DATA_PATH)
print("Data loaded:", df.shape)

# -----------------------
# Features / Target
# -----------------------
X = df.drop(columns=[
    "Price_per_sqft",
    "Total_Price_Cr",
    "Estimated_Monthly_Rent"
])
y = df["Price_per_sqft"]

X = pd.get_dummies(X, drop_first=True)

# -----------------------
# Train-test split
# -----------------------
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# -----------------------
# Models to compare
# -----------------------
models = {
    "Linear_Regression": LinearRegression(),
    "Ridge_Regression": Ridge(alpha=1.0),
    "Random_Forest": RandomForestRegressor(
        n_estimators=300,
        max_depth=15,
        random_state=42
    )
}

if XGBOOST_AVAILABLE:
    models["XGBoost"] = XGBRegressor(
        n_estimators=300,
        learning_rate=0.05,
        max_depth=6,
        subsample=0.8,
        colsample_bytree=0.8,
        random_state=42
    )

# -----------------------
# Train & Evaluate
# -----------------------
results = []

for name, model in models.items():
    print(f"\nTraining {name}...")
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)

    rmse = np.sqrt(mean_squared_error(y_test, y_pred))
    mae = mean_absolute_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)

    results.append({
        "Model": name,
        "RMSE": rmse,
        "MAE": mae,
        "R2": r2
    })

    joblib.dump(model, f"{MODEL_DIR}/{name}.pkl")

# -----------------------
# Results DataFrame
# -----------------------
results_df = pd.DataFrame(results).sort_values("R2", ascending=False)
print("\nModel Comparison:")
print(results_df)

results_df.to_csv("reports/model_comparison.csv", index=False)

# -----------------------
# Plot comparison
# -----------------------
plt.figure(figsize=(8, 5))
plt.bar(results_df["Model"], results_df["R2"])
plt.ylabel("R² Score")
plt.title("Model Comparison (Price per Sqft Prediction)")
plt.xticks(rotation=30)
plt.tight_layout()
plt.savefig(f"{FIG_PATH}/model_comparison_r2.png")
plt.close()

# -----------------------
# Select & save best model
# -----------------------
best_model_name = results_df.iloc[0]["Model"]
best_model = joblib.load(f"{MODEL_DIR}/{best_model_name}.pkl")

joblib.dump(best_model, f"{MODEL_DIR}/best_price_model.pkl")

print(f"\nBest model selected: {best_model_name}")
print("Saved as models/best_price_model.pkl")