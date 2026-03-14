from sensitivity_engine import sensitivity_analysis


foundation_area = 4
column_capacity = 1000
load_per_storey = 120
soil_capacity = 200


results = sensitivity_analysis(
    foundation_area,
    column_capacity,
    load_per_storey,
    soil_capacity
)


print("Sensitivity Analysis Results")
print("----------------------------------")

for case in results:

    print(
        "Load:", case["load"],
        "| Soil:", case["soil_capacity"],
        "| Column Util:", case["column_utilization"],
        "| Soil Util:", case["soil_utilization"],
        "| Mode:", case["governing_mode"],
        "| Status:", case["status"]
    )
