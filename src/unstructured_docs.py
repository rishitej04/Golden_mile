import os
import random
from datetime import datetime

random.seed(42)

BASE_DIR = "data/unstructured"

cities = {
    "Hyderabad": [
        "Gachibowli", "Hitech City", "Madhapur",
        "Kondapur", "Kukatpally", "Miyapur", "Uppal"
    ],
    "Bengaluru": [
        "Whitefield", "Electronic City",
        "Indiranagar", "Sarjapur Road", "Yelahanka"
    ],
    "Pune": [
        "Hinjewadi", "Wakad", "Baner", "Kharadi"
    ]
}

doc_templates = {
    "market_update": [
        "The real estate market in {locality}, {city} has shown steady growth in {year}. "
        "Demand remains strong due to employment opportunities and infrastructure expansion. "
        "Average prices have increased moderately compared to the previous year.",

        "{locality} continues to be a preferred residential destination in {city}. "
        "The market in {year} reflects stable buyer interest supported by connectivity and social infrastructure."
    ],

    "rent_demand": [
        "Rental demand in {locality}, {city} remains high in {year}, driven primarily by working professionals. "
        "Properties closer to metro stations and IT hubs command premium rents.",

        "In {year}, {locality} witnessed increased rental absorption due to corporate hiring and limited new supply."
    ],

    "supply_pipeline": [
        "The supply pipeline in {locality}, {city} during {year} includes mid-rise residential developments. "
        "Most new projects are focused on 2 and 3 BHK units.",

        "Developers in {locality} are prioritizing phased construction to manage inventory levels in {year}."
    ],

    "it_corridor_growth": [
        "{locality} has benefited from IT corridor expansion in {city} during {year}. "
        "New office spaces and tech parks have positively influenced residential demand.",

        "The growth of IT employment hubs near {locality} has contributed to steady housing demand in {year}."
    ]
}

# -----------------------------
# Document Generation
# -----------------------------

os.makedirs(BASE_DIR, exist_ok=True)

years = [2023, 2024]

for city, localities in cities.items():
    city_dir = os.path.join(BASE_DIR, city)
    os.makedirs(city_dir, exist_ok=True)

    for locality in localities:
        for doc_type, templates in doc_templates.items():
            year = random.choice(years)
            content = random.choice(templates).format(
                city=city,
                locality=locality,
                year=year
            )

            filename = f"{locality.lower().replace(' ', '_')}_{doc_type}_{year}.txt"
            filepath = os.path.join(city_dir, filename)

            with open(filepath, "w") as f:
                f.write(f"Title: {doc_type.replace('_', ' ').title()}\n")
                f.write(f"City: {city}\n")
                f.write(f"Locality: {locality}\n")
                f.write(f"Year: {year}\n\n")
                f.write(content)

print("Unstructured text documents generated successfully.")