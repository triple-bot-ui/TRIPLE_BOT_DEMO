from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib import colors
import io


def generate_engineering_report(result, intelligence, prebim, boq, decision):

    buffer = io.BytesIO()

    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=30,
        leftMargin=30,
        topMargin=30,
        bottomMargin=30
    )

    styles = getSampleStyleSheet()

    elements = []

    # ============================================
    # TITLE
    # ============================================

    elements.append(Paragraph("Triple Bot Engineering Report", styles['Title']))
    elements.append(Spacer(1, 10))

    elements.append(
        Paragraph("Units: SI (kN, m, m², m³)", styles['Normal'])
    )

    elements.append(Spacer(1, 20))

    # ============================================
    # STRUCTURAL VALIDATION RESULT (V5)
    # ============================================

    elements.append(
        Paragraph("Structural Validation Result (V5)", styles['Heading2'])
    )

    table_data = [
        ["Parameter", "Value"],
        ["Status", result["status"]],
        ["Column Utilization", f"{result['column_utilization']:.3f}"],
        ["Soil Utilization", f"{result['soil_utilization']:.3f}"],
        ["Column Margin", f"{result['column_margin']:.2f} kN"],
        ["Soil Margin", f"{result['soil_margin']:.2f} kN/m²"],
        ["Governing Mode", result["governing_mode"]],
    ]

    table = Table(table_data)

    table.setStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey)
    ])

    elements.append(table)
    elements.append(Spacer(1, 20))

    # ============================================
    # PRE-BIM VALIDATION
    # ============================================

    elements.append(
        Paragraph("Pre-BIM Validation (V5)", styles['Heading2'])
    )

    table_data = [
        ["Parameter", "Value"],
        ["Total Load", f"{prebim['total_load']} kN"],
        ["Soil Pressure", f"{prebim['soil_pressure']} kN/m²"],
        ["Foundation Area", f"{prebim['foundation_area']} m²"],
        ["Required Area", f"{prebim['required_area']} m²"],
        ["Utilization", prebim["utilization"]],
        ["Status", prebim["status"]],
    ]

    table = Table(table_data)

    table.setStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey)
    ])

    elements.append(table)
    elements.append(Spacer(1, 20))

    # ============================================
    # ENGINEERING RECOMMENDATION (V5)
    # ============================================

    elements.append(
        Paragraph("Engineering Recommendation (V5)", styles['Heading2'])
    )

    elements.append(
        Paragraph(intelligence["recommendation"], styles['Normal'])
    )

    elements.append(Spacer(1, 20))

    # ============================================
    # ENGINEERING DECISION (V8)
    # ============================================

    elements.append(
        Paragraph("Engineering Decision (V8)", styles['Heading2'])
    )

    if result.get("status") == "SAFE":

        table_data = [
            ["Parameter", "Value"],
            ["Recommended Action", "None"],
        ]

    elif decision.get("best_option"):

        best = decision["best_option"]

        option_type = best.get("option_type")

        load_reduction = "N/A"
        foundation_size = "N/A"
        column_upgrade = "N/A"

        if option_type == "LOAD_REDUCTION":
            # BUG FIX: guard against load_reduction being None before multiplying
            lr = best.get("load_reduction")
            load_reduction = f"{lr * 100:.1f} %" if lr is not None else "N/A"

        if option_type == "FOUNDATION_INCREASE":
            foundation_size = best.get("foundation_size", "N/A")

        if option_type == "COLUMN_UPGRADE":
            column_upgrade = best.get("column_capacity", "N/A")

        table_data = [
            ["Parameter", "Value"],
            ["Recommended Action", option_type],
            ["Load Reduction", load_reduction],
            ["New Foundation Size", foundation_size],
            ["Upgraded Column Capacity", column_upgrade],
        ]

    else:

        table_data = [
            ["Parameter", "Value"],
            ["Recommended Action", "None"],
        ]

    table = Table(table_data)

    table.setStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey)
    ])

    elements.append(table)
    elements.append(Spacer(1, 20))

    # ============================================
    # BOQ
    # ============================================

    elements.append(
        Paragraph("Bill of Quantities (V5)", styles['Heading2'])
    )

    table_data = [
        ["Parameter", "Value"],
        ["Foundation Area", f"{boq['foundation_area']} m²"],
        ["Foundation Depth", f"{boq['foundation_depth']} m"],
        ["Concrete Volume", f"{boq['concrete_volume_m3']} m³"],
        ["Excavation Volume", f"{boq['excavation_volume_m3']} m³"],
        ["Reinforcement Estimate", f"{boq['reinforcement_estimate']} kg"],
    ]

    table = Table(table_data)

    table.setStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey)
    ])

    elements.append(table)
    elements.append(Spacer(1, 20))

    # ============================================
    # DISCLAIMER
    # ============================================

    elements.append(
        Paragraph(
            "Note: This report provides deterministic structural validation "
            "based on the provided input parameters. Final engineering approval "
            "must be performed by a licensed structural engineer.",
            styles['Italic']
        )
    )

    doc.build(elements)

    pdf = buffer.getvalue()
    buffer.close()

    return pdf
