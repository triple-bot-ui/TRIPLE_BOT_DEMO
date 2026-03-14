target_utilization = 0.8

column_utilization = total_load / column_capacity
soil_utilization = total_load / (soil_capacity * foundation_area)

result = {}

if column_utilization <= 1 and soil_utilization <= 1:

    result["status"] = "SAFE"
    result["recommendation"] = "Design already safe. Optimization possible."

else:

    result["status"] = "FAIL"
    fixes = []

    required_column_capacity = total_load / target_utilization
    fixes.append({
        "type": "column",
        "recommended_capacity": round(required_column_capacity,2)
    })

    required_area = total_load / (soil_capacity * target_utilization)
    side = math.sqrt(required_area)

    fixes.append({
        "type": "foundation",
        "recommended_size": round(side,2)
    })

    result["fix_options"] = fixes

return result
