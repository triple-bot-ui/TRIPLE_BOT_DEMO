# =========================================
# TRIPLE BOT V3
# Master Engine
# =========================================

from multi_storey_engine import multi_storey_validation
from sensitivity_engine import sensitivity_analysis
from scenario_engine import scenario_exploration
from pre_bim_validation_engine import pre_bim_validation
from engineering_intelligence_engine import engineering_intelligence


def run_triplebot_analysis(
    foundation_width,
    foundation_length,
    load_per_storey,
    storeys,
    soil_capacity,
    column_capacity
):

    foundation_area = foundation_width * foundation_length
    total_load = load_per_storey * storeys

    # Module 1–2
    structural_result = multi_storey_validation(
        load_per_storey,
        storeys,
        column_capacity,
        foundation_area,
        soil_capacity
    )

    # Module 3
    sensitivity_result = sensitivity_analysis(
        foundation_area,
        column_capacity,
        load_per_storey,
        soil_capacity
    )

    # Module 4
    scenario_result = scenario_exploration(
        foundation_area,
        column_capacity,
        load_per_storey,
        soil_capacity
    )

    # Module 5
    prebim_result = pre_bim_validation(
        foundation_width,
        foundation_length,
        total_load,
        soil_capacity
    )

    # Module 6
    intelligence_result = engineering_intelligence(
        foundation_width,
        foundation_length,
        total_load,
        soil_capacity,
        column_capacity
    )

    result = {

        "structural_validation": structural_result,

        "sensitivity_analysis": sensitivity_result,

        "scenario_exploration": scenario_result,

        "pre_bim_validation": prebim_result,

        "engineering_intelligence": intelligence_result

    }

    return result
