# ============================================
# TRIPLE BOT V8
# ENGINE 3 — ENGINEERING DECISION ENGINE
# Deterministic Engineering Decision Selection
# ============================================


def generate_engineering_decision(ranked_options, engineering_results):

    if not ranked_options:
        return {
            "error": "No engineering options generated"
        }

    # ----------------------------------------
    # BEST OPTION
    # ----------------------------------------

    best_option = ranked_options[0]

    # ----------------------------------------
    # ALTERNATIVE OPTION
    # ----------------------------------------

    alternative_option = None
    if len(ranked_options) > 1:
        alternative_option = ranked_options[1]

    # ----------------------------------------
    # THIRD OPTION
    # ----------------------------------------

    third_option = None
    if len(ranked_options) > 2:
        third_option = ranked_options[2]

    # ----------------------------------------
    # DECISION NOTE
    # ----------------------------------------

    option_type = best_option.get("option_type")

    if option_type == "FOUNDATION_INCREASE":

        note = (
            f"Recommended foundation size: "
            f"{best_option.get('foundation_size')} m "
            f"(soil utilization {best_option.get('soil_utilization')})."
        )

    elif option_type == "COLUMN_UPGRADE":

        note = (
            f"Recommended column capacity: "
            f"{best_option.get('column_capacity')} kN "
            f"(column utilization {best_option.get('column_utilization')})."
        )

    elif option_type == "LOAD_REDUCTION":

        reduction_percent = best_option.get("load_reduction", 0) * 100

        note = (
            f"Recommended load reduction: "
            f"{reduction_percent}% "
            f"to achieve acceptable structural utilization."
        )

    else:

        note = "Engineering review required."

    # ----------------------------------------
    # DECISION STRUCTURE
    # ----------------------------------------

    decision = {
        "best_option": best_option,
        "alternative_option": alternative_option,
        "third_option": third_option,
        "decision_note": note
    }

    return decision