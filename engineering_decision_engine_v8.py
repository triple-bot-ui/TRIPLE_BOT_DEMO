# engineering_decision_engine_v8.py
# Triple Bot V8 Decision Engine
# Deterministic engineering recommendation layer


def prioritize_options_by_governing_mode(options, governing_mode):

    if not options:
        return []

    priority = []
    secondary = []

    for opt in options:

        option_type = opt.get("option_type")

        if governing_mode == "COLUMN":

            if option_type == "COLUMN_UPGRADE":
                priority.append(opt)
            else:
                secondary.append(opt)

        elif governing_mode == "SOIL":

            if option_type == "FOUNDATION_INCREASE":
                priority.append(opt)
            else:
                secondary.append(opt)

        else:
            secondary.append(opt)

    return priority + secondary


def generate_engineering_decision(options, engineering_results=None):

    if not options:
        return {
            "best_option": None,
            "recommended_action": "NONE",
            "new_foundation_size": None,
            "upgraded_column_capacity": None,
            "load_reduction": None
        }

    governing_mode = None

    if engineering_results:
        governing_mode = engineering_results.get("governing_mode")

    ranked_options = prioritize_options_by_governing_mode(
        options,
        governing_mode
    )

    best_option = ranked_options[0]

    decision = {
        "best_option": best_option,
        "recommended_action": best_option.get("option_type"),
        "new_foundation_size": best_option.get("new_foundation_size"),
        "upgraded_column_capacity": best_option.get("upgraded_column_capacity"),
        "load_reduction": best_option.get("load_reduction")
    }

    return decision