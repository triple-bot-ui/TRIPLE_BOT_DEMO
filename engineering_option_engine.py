# ============================================
# TRIPLE BOT V8
# ENGINE 1 — ENGINEERING OPTION GENERATOR
# Deterministic Engineering Option Exploration
# ============================================

# SEARCH PARAMETERS

MIN_FOUNDATION_SIZE = 1.0
MAX_FOUNDATION_SIZE = 10.0
FOUNDATION_STEP = 0.5

# Overdesign guardrail
MIN_SOIL_UTILIZATION = 0.10

COLUMN_OPTIONS = [
    200,
    300,
    400,
    500,
    800,
    1000
]

LOAD_REDUCTION_OPTIONS = [
    0.00,
    0.05,
    0.10,
    0.20
]


def generate_engineering_options(engineering_results, input_data):

    options = []

    foundation_width = input_data["foundation_width"]
    foundation_length = input_data["foundation_length"]

    load_per_storey = input_data["load_per_storey"]
    storeys = input_data["storeys"]

    soil_capacity = input_data["soil_capacity"]
    column_capacity = input_data["column_capacity"]

    total_load = load_per_storey * storeys

    # ----------------------------------------
    # OPTION TYPE A
    # FOUNDATION SIZE INCREASE
    # ----------------------------------------

    size = MIN_FOUNDATION_SIZE

    while size <= MAX_FOUNDATION_SIZE:

        foundation_area = size * size

        soil_pressure = total_load / foundation_area

        soil_utilization = soil_pressure / soil_capacity

        if (
            soil_utilization <= 1.0 and
            soil_utilization >= MIN_SOIL_UTILIZATION
        ):

            options.append({
                "option_type": "FOUNDATION_INCREASE",
                "foundation_size": round(size, 2),
                "soil_utilization": round(soil_utilization, 3),
                "status": "OPTIMAL"
            })

        size += FOUNDATION_STEP

    # ----------------------------------------
    # OPTION TYPE B
    # COLUMN CAPACITY UPGRADE
    # ----------------------------------------

    for capacity in COLUMN_OPTIONS:

        column_utilization = total_load / capacity

        if column_utilization <= 1.0:

            options.append({
                "option_type": "COLUMN_UPGRADE",
                "column_capacity": capacity,
                "column_utilization": round(column_utilization, 3),
                "status": "OPTIMAL"
            })

    # ----------------------------------------
    # OPTION TYPE C
    # LOAD REDUCTION
    # ----------------------------------------

    for reduction in LOAD_REDUCTION_OPTIONS:

        if reduction == 0:
            continue

        reduced_load = total_load * (1 - reduction)

        column_utilization = reduced_load / column_capacity

        foundation_area = foundation_width * foundation_length

        soil_pressure = reduced_load / foundation_area

        soil_utilization = soil_pressure / soil_capacity

        if column_utilization <= 1.0 and soil_utilization <= 1.0:

            options.append({
                "option_type": "LOAD_REDUCTION",
                "load_reduction": reduction,
                "column_utilization": round(column_utilization, 3),
                "soil_utilization": round(soil_utilization, 3),
                "status": "ACCEPTABLE"
            })

    return options