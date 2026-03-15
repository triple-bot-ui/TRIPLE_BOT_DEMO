# ============================================
# TRIPLE BOT V5
# BOQ ENGINE
# ============================================

def generate_boq(
    foundation_width,
    foundation_length,
    total_load,
    soil_capacity
):

    # --------------------------------
    # Foundation geometry
    # --------------------------------

    foundation_area = foundation_width * foundation_length

    # Engineering assumption
    foundation_depth = 0.4

    # --------------------------------
    # Concrete calculation
    # --------------------------------

    concrete_volume_m3 = foundation_area * foundation_depth

    # Excavation volume (include working space factor)
    excavation_volume_m3 = concrete_volume_m3 * 1.8

    # --------------------------------
    # Reinforcement estimate
    # --------------------------------
    # Typical shallow footing assumption
    # ~100 kg rebar per m³ concrete

    reinforcement_estimate = concrete_volume_m3 * 100

    # --------------------------------
    # Return BOQ dictionary
    # --------------------------------

    boq = {

        "foundation_area": round(foundation_area, 3),

        "foundation_depth": foundation_depth,

        "concrete_volume_m3": round(concrete_volume_m3, 3),

        "excavation_volume_m3": round(excavation_volume_m3, 3),

        "reinforcement_estimate": round(reinforcement_estimate, 2)

    }

    return boq