# ============================================
# TRIPLE BOT V5
# Structural Validation UI
# ============================================

import streamlit as st
import pandas as pd
from datetime import datetime

from master_engine_v3 import run_structural_validation
from scenario_engine import run_scenario_exploration
from sensitivity_engine import run_sensitivity_analysis
from pre_bim_validation_engine import run_prebim_validation
from engineering_intelligence_engine import generate_engineering_intelligence
from triplebot_report_generator import generate_engineering_report
from boq_engine import generate_boq
from triplebot_diagram_engine import generate_conceptual_diagram


st.set_page_config(page_title="Triple Bot V5", layout="wide")

st.title("Triple Bot V5 – Structural Validation")

# ============================================
# SYSTEM TRACEABILITY
# ============================================

SYSTEM_VERSION = "Triple Bot V5"
timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")

st.caption(f"System Version: {SYSTEM_VERSION}")
st.caption(f"Timestamp: {timestamp}")

# ============================================
# INPUT SECTION
# ============================================

foundation_width = st.number_input(
    "Foundation Width (m)", value=1.0, min_value=0.0
)

foundation_length = st.number_input(
    "Foundation Length (m)", value=1.0, min_value=0.0
)

column_capacity = st.number_input(
    "Column Capacity (kN)", value=500.0, min_value=0.0
)

load_per_storey = st.number_input(
    "Load per Storey (kN)", value=120.0, min_value=0.0
)

storeys = st.number_input(
    "Number of Storeys", value=1, min_value=1
)

soil_capacity = st.number_input(
    "Soil Capacity (kN/m²)", value=200.0, min_value=0.0
)

run = st.button("Run Validation")

# ============================================
# INPUT VALIDATION
# ============================================

if run:

    if foundation_width <= 0 or foundation_length <= 0:
        st.error("Foundation dimensions must be greater than zero.")
        st.stop()

    if column_capacity <= 0:
        st.error("Column capacity must be greater than zero.")
        st.stop()

    if soil_capacity <= 0:
        st.error("Soil capacity must be greater than zero.")
        st.stop()

    total_load = load_per_storey * storeys

    # ============================================
    # STRUCTURAL VALIDATION
    # ============================================

    result = run_structural_validation(
        foundation_width,
        foundation_length,
        column_capacity,
        total_load,
        soil_capacity
    )

    st.header("Structural Validation Result")

    status = result["status"]
    column_util = result["column_utilization"]
    soil_util = result["soil_utilization"]

    column_margin = result["column_margin"]
    soil_margin = result["soil_margin"]

    governing_mode = result["governing_mode"]

    if status == "SAFE":
        st.success("Status: SAFE")
    else:
        st.error("Status: FAIL")

    # ============================================
    # STRUCTURAL DIAGRAM
    # ============================================

    st.subheader("Structural Conceptual Diagram")

    diagram = generate_conceptual_diagram(
        foundation_width,
        foundation_length,
        total_load,
        result["soil_pressure"]
    )

    st.image(diagram)

    # ============================================
    # UTILIZATION DISPLAY
    # ============================================

    st.subheader("Utilization Overview")

    st.write("Column Utilization")
    st.progress(min(column_util, 1.0))

    st.write("Soil Utilization")
    st.progress(min(soil_util, 1.0))

    col1, col2 = st.columns(2)

    col1.metric("Column Utilization", f"{column_util:.3f}")
    col2.metric("Soil Utilization", f"{soil_util:.3f}")

    col1.metric("Column Margin (kN)", f"{column_margin:.2f}")
    col2.metric("Soil Margin (kN/m²)", f"{soil_margin:.2f}")

    st.write(f"Governing Mode: **{governing_mode}**")

    # ============================================
    # SAFETY FACTORS
    # ============================================

    st.subheader("Safety Factors")

    foundation_area = foundation_width * foundation_length
    soil_pressure = total_load / foundation_area

    column_sf = column_capacity / total_load
    soil_sf = soil_capacity / soil_pressure

    col3, col4 = st.columns(2)

    col3.metric("Column Safety Factor", f"{column_sf:.2f}")
    col4.metric("Soil Safety Factor", f"{soil_sf:.2f}")

    # ============================================
    # SCENARIO
    # ============================================

    st.header("Scenario Exploration")

    scenario_df = run_scenario_exploration(
        load_per_storey,
        storeys,
        foundation_width,
        foundation_length,
        column_capacity,
        soil_capacity
    )

    st.dataframe(pd.DataFrame(scenario_df))

    # ============================================
    # SENSITIVITY
    # ============================================

    st.header("Sensitivity Analysis")

    sens_df = run_sensitivity_analysis(
        load_per_storey,
        storeys,
        foundation_width,
        foundation_length,
        column_capacity,
        soil_capacity
    )

    st.dataframe(pd.DataFrame(sens_df))

    # ============================================
    # PRE-BIM
    # ============================================

    st.header("Pre-BIM Validation")

    prebim = run_prebim_validation(
        load_per_storey,
        storeys,
        foundation_width,
        foundation_length,
        column_capacity,
        soil_capacity
    )

    col5, col6 = st.columns(2)

    col5.metric("Total Load (kN)", prebim["total_load"])
    col6.metric("Soil Pressure (kN/m²)", prebim["soil_pressure"])

    col5.metric("Foundation Area (m²)", prebim["foundation_area"])
    col6.metric("Required Area (m²)", prebim["required_area"])

    st.write(f"Utilization: {prebim['utilization']}")
    st.write(f"Status: {prebim['status']}")

    # ============================================
    # CONSTRUCTION RECOMMENDATION
    # ============================================

    st.header("Construction Recommendation (V5)")

    intelligence = generate_engineering_intelligence(result)

    st.success(intelligence["recommendation"])

    # ============================================
    # BOQ SECTION
    # ============================================

    st.header("Bill of Quantities (V5)")

    boq = generate_boq(
        foundation_width,
        foundation_length,
        total_load,
        soil_capacity
    )

    col7, col8 = st.columns(2)

    col7.metric("Foundation Area (m²)", boq["foundation_area"])
    col8.metric("Foundation Depth (m)", boq["foundation_depth"])

    col7.metric("Concrete Volume (m³)", boq["concrete_volume_m3"])
    col8.metric("Excavation Volume (m³)", boq["excavation_volume_m3"])

    st.metric("Reinforcement Estimate (kg)", boq["reinforcement_kg"])

    # ============================================
    # REPORT
    # ============================================

    st.header("Download Engineering Report")

    pdf = generate_engineering_report(
        result,
        intelligence,
        prebim,
        boq
    )

    st.download_button(
        label="Download PDF Report",
        data=pdf,
        file_name="engineering_report.pdf",
        mime="application/pdf"
    )