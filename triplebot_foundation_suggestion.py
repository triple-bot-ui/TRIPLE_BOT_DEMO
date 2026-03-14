# ============================================
# TRIPLE BOT V5
# Foundation Resize Suggestion Engine
# ============================================

import math


def suggest_foundation_resize(prebim_result):

    required_area = prebim_result["required_area"]

    suggested_side = math.sqrt(required_area)

    # round up to engineering friendly size
    suggested_side = round(suggested_side + 0.05, 2)

    suggested_area = round(suggested_side * suggested_side, 3)

    return {
        "required_area": required_area,
        "suggested_foundation_width": suggested_side,
        "suggested_foundation_length": suggested_side,
        "suggested_foundation_area": suggested_area
    }