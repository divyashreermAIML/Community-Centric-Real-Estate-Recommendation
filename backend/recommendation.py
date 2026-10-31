
import pandas as pd
from pathlib import Path

# Project scoring weights
WEIGHTS = {
    "budget": 0.30,
    "location": 0.25,
    "amenities": 0.20,
    "transport": 0.15,
    "community": 0.10
}

# Read the property dataset
DATASET_PATH = (
    Path(__file__).resolve().parent.parent
    / "dataset"
    / "properties.csv"
)


def calculate_budget_score(rent, budget):
    ratio = rent / budget

    if ratio <= 0.75:
        return 100
    elif ratio <= 0.85:
        return 85
    elif ratio <= 0.95:
        return 70
    else:
        return 60


def calculate_location_score(distance, max_distance):
    score = 100 * (1 - distance / max_distance)
    return round(max(0, score), 2)


def calculate_amenities_score(property_amenities, required):
    if not required:
        return 100

    available = [
        item.strip().lower()
        for item in str(property_amenities).split(";")
    ]

    matched = sum(
        1 for item in required
        if item.strip().lower() in available
    )

    return round((matched / len(required)) * 100, 2)


def recommend_properties(
    budget,
    max_distance,
    required_amenities,
    transport_required
):

    df = pd.read_csv(DATASET_PATH)

    # Step 1: Filter properties
    df = df[
        (df["rent"] <= budget) &
        (df["distance"] <= max_distance)
    ].copy()

    # Step 2: Apply transport requirement
    if transport_required:
        df = df[
            df["transport"].str.lower() == "yes"
        ].copy()

    results = []

    # Step 3: Calculate suitability scores
    for _, property_data in df.iterrows():

        budget_score = calculate_budget_score(
            property_data["rent"], budget
        )

        location_score = calculate_location_score(
            property_data["distance"], max_distance
        )

        amenities_score = calculate_amenities_score(
            property_data["amenities"],
            required_amenities
        )

        transport_score = (
            100 if str(property_data["transport"]).lower() == "yes"
            else 0
        )

        community_score = float(
            property_data["community_score"]
        )

        # Step 4: Calculate final weighted score
        final_score = (
            budget_score * WEIGHTS["budget"] +
            location_score * WEIGHTS["location"] +
            amenities_score * WEIGHTS["amenities"] +
            transport_score * WEIGHTS["transport"] +
            community_score * WEIGHTS["community"]
        )

        results.append({
            "id": int(property_data["id"]),
            "name": property_data["name"],
            "category": property_data["category"],
            "rent": int(property_data["rent"]),
            "distance": float(property_data["distance"]),
            "budget_score": budget_score,
            "location_score": location_score,
            "amenities_score": amenities_score,
            "transport_score": transport_score,
            "community_score": community_score,
            "suitability_score": round(final_score, 2),
            "verification_status": property_data["verification_status"]
        })

    # Step 5: Rank properties from highest to lowest
    results.sort(
        key=lambda x: x["suitability_score"],
        reverse=True
    )

    return results
