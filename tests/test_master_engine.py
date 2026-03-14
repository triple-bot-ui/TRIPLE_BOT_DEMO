# =========================================
# TRIPLE BOT V3
# MASTER ENGINE TEST
# =========================================

from master_engine_v3 import run_master_engine


foundation_width = 1.0
foundation_length = 1.0
column_capacity = 1000
load_per_storey = 120
number_of_storeys = 1
soil_capacity = 200


results = run_master_engine(
    foundation_width,
    foundation_length,
    column_capacity,
    load_per_storey,
    number_of_storeys,
    soil_capacity
)


print("\n==============================")
print("STRUCTURAL VALIDATION")
print("==============================")
print(results["structural_validation"])


print("\n==============================")
print("SENSITIVITY ANALYSIS")
print("==============================")
for case in results["sensitivity"]:
    print(case)


print("\n==============================")
print("SCENARIO EXPLORATION")
print("==============================")
for case in results["scenario"]:
    print(case)


print("\n==============================")
print("PRE BIM VALIDATION")
print("==============================")
print(results["prebim"])


print("\n==============================")
print("ENGINEERING INTELLIGENCE")
print("==============================")
print(results["intelligence"])
