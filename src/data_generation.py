import pandas as pd
import numpy as np
import random
import os

np.random.seed(42)
random.seed(42)

# -----------------------------
# Helper Functions
# -----------------------------

def snap_size(size):
    size_buckets = [
        750, 900, 1000, 1200, 1350, 1500,
        1800, 2000, 2200, 2500, 3000, 3500
    ]
    return min(size_buckets, key=lambda x: abs(x - size))


def round_price_per_sqft(price):
    return int(round(price / 500) * 500)


def to_crores(amount):
    return round(amount / 1e7, 2)   # 1 Cr = 10,000,000


def estimate_rent(total_price, city):
    rent_yield = {
        "Hyderabad": 0.035,
        "Bengaluru": 0.032,
        "Pune": 0.030
    }
    annual_rent = total_price * rent_yield[city]
    return int(annual_rent / 12)


# -----------------------------
# Configurations (ASSUMPTIONS)
# -----------------------------

cities = {
    "Hyderabad": {
        "base_price": 6500,
        "localities": {
            "Gachibowli": 1.30,
            "Hitech City": 1.35,
            "Madhapur": 1.28,
            "Kondapur": 1.15,
            "Kukatpally": 0.95,
            "Miyapur": 0.90,
            "Uppal": 0.85,
            "LB Nagar": 0.82
        }
    },
    "Bengaluru": {
        "base_price": 7200,
        "localities": {
            "Whitefield": 1.25,
            "Electronic City": 1.10,
            "Indiranagar": 1.40,
            "Sarjapur Road": 1.22,
            "Yelahanka": 1.05
        }
    },
    "Pune": {
        "base_price": 7000,
        "localities": {
            "Hinjewadi": 1.20,
            "Wakad": 1.05,
            "Baner": 1.30,
            "Kharadi": 1.25
        }
    }
}

property_type_factor = {
    "Apartment": 1.0,
    "Villa": 1.45
}

records = []

# -----------------------------
# Data Generation
# -----------------------------

for city, city_info in cities.items():
    base_price = city_info["base_price"]

    for locality, loc_factor in city_info["localities"].items():
        for _ in range(150):  # per locality
            raw_size = random.randint(700, 3600)
            size_sqft = snap_size(raw_size)

            age_years = random.randint(0, 25)
            property_type = random.choice(["Apartment", "Villa"])
            distance_to_metro = round(np.random.uniform(0.3, 10.0), 2)
            amenities_score = random.randint(5, 10)

            size_factor = (size_sqft / 1000) ** 0.85
            age_factor = max(0.6, 1 - (0.015 * age_years))

            base_psf = (
                base_price
                * loc_factor
                * property_type_factor[property_type]
                * size_factor
                * age_factor
            )

            noise = np.random.normal(1.0, 0.08)
            price_per_sqft = round_price_per_sqft(base_psf * noise)

            total_price = price_per_sqft * size_sqft
            total_price_cr = to_crores(total_price)

            rent_monthly = estimate_rent(total_price, city)

            records.append([
                city,
                locality,
                size_sqft,
                property_type,
                age_years,
                distance_to_metro,
                amenities_score,
                price_per_sqft,
                total_price_cr,
                rent_monthly
            ])

# -----------------------------
# Save Dataset
# -----------------------------

columns = [
    "City",
    "Locality",
    "Size_sqft",
    "Property_Type",
    "Age_years",
    "Distance_to_metro_km",
    "Amenities_score",
    "Price_per_sqft",
    "Total_Price_Cr",
    "Estimated_Monthly_Rent"
]

df = pd.DataFrame(records, columns=columns)

os.makedirs("data/structured", exist_ok=True)
df.to_csv("data/structured/real_estate_data.csv", index=False)

print(f"Dataset generated successfully with {len(df)} rows")