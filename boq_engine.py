# ============================================
# TRIPLE BOT V5.2
# SMART BOQ ENGINE
# Deterministic Quantity Generator
# ============================================

import math

SYSTEM_VERSION = "Triple Bot V5.2"

# ============================================
# ENGINEERING CONSTANTS
# ============================================

# Base footing thickness (conceptual engineering baseline)
BASE_FOUNDATION_DEPTH = 0.4

# Load influence increment
LOAD_DEPTH_INCREMENT = 0.1

# Soil influence increment
SOIL_DEPTH_INCREMENT = 0.1

# Maximum practical footing depth (conceptual limit)
MAX_FOUNDATION_DEPTH = 1.0

# Excavation allowances
WORKING_SPACE_ALLOWANCE = 0.2
EXCAVATION_EXTRA_DEPTH = 0.1

# Reinforcement density (kg per m³ of concrete)
REBAR_DENSITY = 100

# Numerical safety
EPSILON = 1e-6


def generate_boq(
    foundation_width,
    foundation_length,
    total_load,
    soil_capacity
):

    result = {}

    # ============================================
    # FOUNDATION GEOMETRY
    # ============================================

    foundation_area = foundation_width * foundation_length

    # ============================================
    # SMART FOUNDATION DEPTH
    # Deterministic engineering heuristic
    # ============================================

    depth = BASE_FOUNDATION_DEPTH

    # Load influence
    if total_load > 200:
        depth += LOAD_DEPTH_INCREMENT

    if total_load > 400:
        depth += LOAD_DEPTH_INCREMENT

    # Soil influence
    if soil_capacity < 150:
        depth += SOIL_DEPTH_INCREMENT

    if soil_capacity < 100:
        depth += SOIL_DEPTH_INCREMENT

    # Clamp to engineering bounds
    depth = max(BASE_FOUNDATION_DEPTH, min(depth, MAX_FOUNDATION_DEPTH))

    foundation_depth = round(depth, 3)

    # ============================================
    # CONCRETE VOLUME
    # ============================================

    concrete_volume = foundation_area * foundation_depth

    # ============================================
    # EXCAVATION VOLUME
    # Working space + extra depth allowance
    # ============================================

    excavation_width = foundation_width + WORKING_SPACE_ALLOWANCE
    excavation_length = foundation_length + WORKING_SPACE_ALLOWANCE
    excavation_depth = foundation_depth + EXCAVATION_EXTRA_DEPTH

    excavation_volume = (
        excavation_width *
        excavation_length *
        excavation_depth
    )

    # ============================================
    # REINFORCEMENT ESTIMATE
    # kg per cubic meter of concrete
    # ============================================

    reinforcement_kg = concrete_volume * REBAR_DENSITY

    # ============================================
    # FORMWORK AREA
    # perimeter × depth
    # ============================================

    perimeter = 2 * (foundation_width + foundation_length)

    formwork_area = perimeter * foundation_depth

    # ============================================
    # SOIL PRESSURE CHECK
    # ============================================

    safe_area = foundation_area if foundation_area > EPSILON else EPSILON
    safe_soil = soil_capacity if soil_capacity > EPSILON else EPSILON

    soil_pressure = total_load / safe_area
    soil_utilization = soil_pressure / safe_soil

    # ============================================
    # OUTPUT
    # ============================================

    result["foundation_area"] = round(foundation_area, 3)
    result["foundation_depth"] = foundation_depth

    result["concrete_volume_m3"] = round(concrete_volume, 3)
    result["excavation_volume_m3"] = round(excavation_volume, 3)

    result["reinforcement_kg"] = round(reinforcement_kg, 1)
    result["formwork_area_m2"] = round(formwork_area, 3)

    result["soil_pressure"] = round(soil_pressure, 3)
    result["soil_utilization"] = round(soil_utilization, 3)

    return result