from engineering_intelligence_engine import generate_engineering_intelligence


structural_validation = {
    "column_utilization": 0.24,
    "soil_utilization": 0.15,
    "column_margin": 380,
    "soil_margin": 170,
    "governing_mode": "COLUMN"
}


result = generate_engineering_intelligence(structural_validation)


print("Engineering Intelligence Result")
print("----------------------------------")

print("Recommendation:", result["recommendation"])
print("Risk Level:", result["risk_level"])
print("Governing Behavior:", result["governing_behavior"])
print("Structural Reserve:", result["structural_reserve"])
