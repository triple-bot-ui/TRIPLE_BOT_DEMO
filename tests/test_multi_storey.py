from multi_storey_engine import multi_storey_validation, calculate_max_storeys

load_per_storey = 120
storeys = 3
column_capacity = 1000
foundation_area = 4
soil_capacity = 200

result = multi_storey_validation(
    load_per_storey,
    storeys,
    column_capacity,
    foundation_area,
    soil_capacity
)

print("Validation Result")
print(result)

max_storeys = calculate_max_storeys(
    load_per_storey,
    column_capacity,
    foundation_area,
    soil_capacity
)

print("Maximum Safe Storeys")
print(max_storeys)