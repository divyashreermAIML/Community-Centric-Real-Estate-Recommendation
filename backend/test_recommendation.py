
from recommendation import recommend_properties

# Sample user preferences
budget = 9000
max_distance = 2
required_amenities = ["Food", "WiFi"]
transport_required = True

# Get recommendations
results = recommend_properties(
    budget,
    max_distance,
    required_amenities,
    transport_required
)

# Display results
print("\n===== PROPERTY RECOMMENDATIONS =====")

if results:
    for property_data in results:
        print("\nProperty:", property_data["name"])
        print("Rent: Rs.", property_data["rent"])
        print("Distance:", property_data["distance"], "km")
        print(
            "Suitability Score:",
            property_data["suitability_score"], "%"
        )
        print(
            "Verification:",
            property_data["verification_status"]
        )
else:
    print("No matching properties found.")
