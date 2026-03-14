from scenario_engine import scenario_exploration


foundation_area = 4
column_capacity = 1000
load_per_storey = 120
soil_capacity = 200


results = scenario_exploration(
    foundation_area,
    column_capacity,
    load_per_storey,
    soil_capacity
)


print("Scenario Exploration Results")
print("----------------------------------")

for case in results:

    print(
        "Scenario:", case["scenario"],
        "| Load:", case["load"],
        "| Column Util:", case["column_utilization"],
        "| Soil Util:", case["soil_utilization"],
        "| Mode:", case["governing_mode"],
        "| Status:", case["status"]
    )
