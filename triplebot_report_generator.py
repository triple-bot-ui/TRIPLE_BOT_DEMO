# ============================================
# TRIPLE BOT V5
# Engineering Report Generator
# ============================================

from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import A4
from io import BytesIO
from datetime import datetime

from triplebot_diagram_engine import generate_conceptual_diagram

SYSTEM_VERSION = "Triple Bot V5"


def generate_engineering_report(result, intelligence, prebim, boq):

    buffer = BytesIO()

    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4
    )

    styles = getSampleStyleSheet()
    elements = []

    # ============================================
    # HEADER
    # ============================================

    elements.append(
        Paragraph(
            "Triple Bot V5 – Structural Validation Report",
            styles["Title"]
        )
    )

    timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")

    elements.append(
        Paragraph(f"System Version: {SYSTEM_VERSION}", styles["Normal"])
    )

    elements.append(
        Paragraph(f"Timestamp: {timestamp}", styles["Normal"])
    )

    elements.append(Spacer(1, 20))

    # ============================================
    # VALIDATION RESULT
    # ============================================

    elements.append(
        Paragraph("Structural Validation Result", styles["Heading2"])
    )

    elements.append(
        Paragraph(f"Status: {result['status']}", styles["Normal"])
    )

    elements.append(
        Paragraph(
            f"Column Utilization: {result['column_utilization']}",
            styles["Normal"]
        )
    )

    elements.append(
        Paragraph(
            f"Soil Utilization: {result['soil_utilization']}",
            styles["Normal"]
        )
    )

    elements.append(
        Paragraph(
            f"Governing Mode: {result['governing_mode']}",
            styles["Normal"]
        )
    )

    elements.append(Spacer(1, 10))

    # ============================================
    # PRE-BIM
    # ============================================

    elements.append(
        Paragraph("Pre-BIM Validation", styles["Heading2"])
    )

    elements.append(
        Paragraph(
            f"Total Load: {prebim['total_load']} kN",
            styles["Normal"]
        )
    )

    elements.append(
        Paragraph(
            f"Soil Pressure: {prebim['soil_pressure']} kN/m²",
            styles["Normal"]
        )
    )

    elements.append(
        Paragraph(
            f"Foundation Area: {prebim['foundation_area']} m²",
            styles["Normal"]
        )
    )

    elements.append(
        Paragraph(
            f"Required Area: {prebim['required_area']} m²",
            styles["Normal"]
        )
    )

    elements.append(Spacer(1, 10))

    # ============================================
    # ENGINEERING RECOMMENDATION
    # ============================================

    elements.append(
        Paragraph("Engineering Recommendation", styles["Heading2"])
    )

    elements.append(
        Paragraph(
            intelligence["recommendation"],
            styles["Normal"]
        )
    )

    elements.append(Spacer(1, 20))

    # ============================================
    # STRUCTURAL DIAGRAM
    # ============================================

    elements.append(
        Paragraph("Structural Conceptual Diagram", styles["Heading2"])
    )

    foundation_area = boq["foundation_area"]
    foundation_size = foundation_area ** 0.5

    diagram = generate_conceptual_diagram(
        foundation_size,
        foundation_size,
        prebim["total_load"],
        prebim["soil_pressure"]
    )

    img_buffer = diagram

    elements.append(Image(img_buffer, width=400, height=250))

    elements.append(Spacer(1, 20))

    # ============================================
    # BOQ
    # ============================================

    elements.append(
        Paragraph("Bill of Quantities (BOQ)", styles["Heading2"])
    )

    elements.append(
        Paragraph(
            f"Foundation Area: {boq['foundation_area']} m²",
            styles["Normal"]
        )
    )

    elements.append(
        Paragraph(
            f"Foundation Depth: {boq['foundation_depth']} m",
            styles["Normal"]
        )
    )

    elements.append(
        Paragraph(
            f"Concrete Volume: {boq['concrete_volume_m3']} m³",
            styles["Normal"]
        )
    )

    elements.append(
        Paragraph(
            f"Excavation Volume: {boq['excavation_volume_m3']} m³",
            styles["Normal"]
        )
    )

    elements.append(
        Paragraph(
            f"Reinforcement Estimate: {boq['reinforcement_kg']} kg",
            styles["Normal"]
        )
    )

    elements.append(Spacer(1, 20))

    # ============================================
    # ENGINEERING ASSUMPTIONS
    # ============================================

    elements.append(
        Paragraph("Engineering Assumptions", styles["Heading2"])
    )

    elements.append(
        Paragraph(
            "Concrete Volume = Foundation Area × Foundation Depth",
            styles["Normal"]
        )
    )

    elements.append(
        Paragraph(
            "Reinforcement Estimate = Concrete Volume × 100 kg/m³",
            styles["Normal"]
        )
    )

    elements.append(
        Paragraph(
            "Excavation Volume = (Width + 0.2) × (Length + 0.2) × (Depth + 0.1)",
            styles["Normal"]
        )
    )

    elements.append(
        Paragraph(
            "Required Foundation Area = Total Load / Soil Capacity",
            styles["Normal"]
        )
    )

    elements.append(Spacer(1, 20))

    doc.build(elements)

    pdf = buffer.getvalue()
    buffer.close()

    return pdf