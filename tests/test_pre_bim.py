from pre_bim_validation_engine import pre_bim_validation


foundation_width = 1.0
foundation_length = 1.0

load = 120
soil_capacity = 200


result = pre_bim_validation(
    foundation_width,
    foundation_length,
    load,
    soil_capacity
)


print("Pre-BIM Validation Result")
print("----------------------------------")

for key, value in result.items():
    print(key, ":", value)
