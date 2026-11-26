import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from datetime import date

st.set_page_config(page_title="MavunoShield", page_icon="🌱", layout="wide")

# ---------- Styling ----------
st.markdown("""
<style>
.main {background-color: #f7faf7;}
.hero {padding: 1.2rem 1.4rem; border-radius: 16px; background: linear-gradient(120deg,#123b2b,#23734a); color: white;}
.hero h1 {color:white; margin-bottom:0.15rem;}
.hero p {color:#e5f4e9; margin-bottom:0;}
.small-note {color:#64748b; font-size:0.85rem;}
.metric-card {background:white; padding:1rem; border-radius:12px; border:1px solid #e2e8f0;}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="hero">
<h1>🌱 MavunoShield</h1>
<p>Actuarial intelligence for agricultural climate-risk awareness and research</p>
</div>
""", unsafe_allow_html=True)

st.caption("Student research prototype • Pilot geography: Kenya • Not an insurance quotation or weather forecast")

with st.sidebar:
    st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/4/49/Flag_of_Kenya.svg/320px-Flag_of_Kenya.svg.png", width=85)
    st.title("Navigation")
    page = st.radio("Choose a module", [
        "Overview", "Farm risk assessment", "Actuarial model", "Scenario explorer",
        "Data & methodology", "About the project"
    ])
    st.divider()
    st.caption("MavunoShield • CUK student innovation project")

# Demonstration assumptions only. Replace with validated local data before research conclusions.
DEFAULTS = {
    "Kitui": {"rain": 500, "note": "Semi-arid pilot illustration"},
    "Makueni": {"rain": 550, "note": "Illustrative seasonal baseline"},
    "Machakos": {"rain": 650, "note": "Illustrative seasonal baseline"},
    "Other": {"rain": 600, "note": "User-defined illustrative baseline"}
}

def payout_fraction(ratio, trigger, exit_level):
    if ratio >= trigger:
        return 0.0
    if ratio <= exit_level:
        return 1.0
    return (trigger - ratio) / (trigger - exit_level)

if page == "Overview":
    st.subheader("Project dashboard")
    st.write("MavunoShield explores how rainfall-index concepts and actuarial modelling can help explain agricultural climate risk.")
    c1, c2, c3 = st.columns(3)
    c1.metric("Pilot country", "Kenya")
    c2.metric("Initial pilot county", "Kitui")
    c3.metric("Prototype status", "Research MVP")
    st.markdown("### What this prototype can do")
    cols = st.columns(3)
    cards = [
        ("🌦️", "Rainfall risk", "Compare observed rainfall with an assumed seasonal reference."),
        ("🧮", "Actuarial illustration", "Calculate insured value, indicative premium and index payout."),
        ("📊", "Scenario testing", "Explore how changing rainfall affects an index-based payout.")
    ]
    for col, (emoji, title, desc) in zip(cols, cards):
        with col:
            st.markdown(f"### {emoji} {title}")
            st.write(desc)
    st.warning("The county rainfall reference values in this demo are placeholders, not verified climatological normals. Do not use them to price or sell insurance.")

elif page == "Farm risk assessment":
    st.subheader("Farm risk assessment")
    st.write("Enter farm and seasonal rainfall information to generate an illustrative index assessment.")
    left, right = st.columns(2)
    with left:
        farmer_ref = st.text_input("Farmer reference (avoid entering sensitive personal data)", "DEMO-001")
        county = st.selectbox("County", list(DEFAULTS.keys()))
        crop = st.selectbox("Main crop", ["Maize", "Beans", "Green grams", "Cowpeas", "Sorghum", "Other"])
        acres = st.number_input("Farm size (acres)", min_value=0.1, max_value=10000.0, value=2.0, step=0.1)
        season = st.selectbox("Season", ["Long rains", "Short rains", "Other"])
    with right:
        baseline = DEFAULTS[county]["rain"]
        normal = st.number_input("Reference seasonal rainfall (mm)", min_value=1.0, value=float(baseline), step=10.0,
                                 help="Replace this demo assumption with a documented local reference before interpreting results.")
        actual = st.number_input("Observed seasonal rainfall (mm)", min_value=0.0, value=float(baseline * 0.70), step=10.0)
        crop_value = st.number_input("Estimated crop value per acre (KSh)", min_value=1.0, value=30000.0, step=1000.0)
        premium_rate = st.number_input("Illustrative premium rate (%)", min_value=0.0, max_value=100.0, value=5.0, step=0.5)
    trigger = st.slider("Payout trigger (% of reference rainfall)", 50, 100, 80) / 100
    exit_level = st.slider("Full-payout threshold (% of reference rainfall)", 0, 80, 50) / 100
    if exit_level >= trigger:
        st.error("The full-payout threshold must be lower than the payout trigger.")
    elif st.button("Generate assessment", type="primary"):
        ratio = actual / normal
        deficit = max(0.0, 1 - ratio)
        insured_value = acres * crop_value
        frac = payout_fraction(ratio, trigger, exit_level)
        premium = insured_value * premium_rate / 100
        payout = insured_value * frac
        if ratio >= 0.8:
            risk = "Lower rainfall deficit"
        elif ratio >= 0.6:
            risk = "Moderate rainfall deficit"
        else:
            risk = "Higher rainfall deficit"
        st.divider()
        st.markdown("### Assessment results")
        a, b, c, d = st.columns(4)
        a.metric("Rainfall ratio", f"{ratio:.1%}")
        b.metric("Rainfall deficit", f"{deficit:.1%}")
        c.metric("Illustrative premium", f"KSh {premium:,.0f}")
        d.metric("Illustrative index payout", f"KSh {payout:,.0f}")
        st.info(f"Risk description: **{risk}**. This describes rainfall relative to the entered reference; it is not a validated crop-loss prediction.")
        result = pd.DataFrame([{
            "reference": farmer_ref, "county": county, "crop": crop, "farm_acres": acres,
            "season": season, "reference_rainfall_mm": normal, "observed_rainfall_mm": actual,
            "rainfall_ratio": ratio, "rainfall_deficit": deficit, "insured_value_ksh": insured_value,
            "illustrative_premium_ksh": premium, "illustrative_payout_ksh": payout
        }])
        st.download_button("Download assessment (CSV)", result.to_csv(index=False), "mavunoshield_assessment.csv", "text/csv")

elif page == "Actuarial model":
    st.subheader("Actuarial model: transparent index illustration")
    st.latex(r"R = \frac{\text{Observed seasonal rainfall}}{\text{Reference seasonal rainfall}}")
    st.latex(r"\text{Rainfall deficit} = \max(0, 1-R)")
    st.latex(r"\text{Insured value} = \text{Farm acres} \times \text{Value per acre}")
    st.markdown("For a simple linear rainfall-index design:")
    st.latex(r"g(R)=\begin{cases}0,&R\geq T\\\\\frac{T-R}{T-E},&E<R<T\\\\1,&R\leq E\end{cases}")
    st.latex(r"\text{Illustrative payout}=\text{Insured value}\times g(R)")
    st.latex(r"\text{Illustrative premium}=\text{Insured value}\times\text{Assumed premium rate}")
    st.write("Here, T is the payout trigger and E is the full-payout threshold. These are design assumptions, not established Kenyan policy terms.")
    st.warning("A defensible pure premium requires a historical loss or payout distribution, exposure data, model calibration and validation. A flat assumed premium rate is only a placeholder.")

elif page == "Scenario explorer":
    st.subheader("Rainfall scenario explorer")
    st.write("Explore how the illustrative payout changes as seasonal rainfall changes.")
    normal = st.number_input("Reference rainfall (mm)", min_value=1.0, value=500.0, key="sc_norm")
    insured = st.number_input("Insured value (KSh)", min_value=1.0, value=60000.0, step=1000.0, key="sc_val")
    trigger = st.slider("Trigger", 50, 100, 80, key="sc_trig") / 100
    exit_level = st.slider("Full payout threshold", 0, 80, 50, key="sc_exit") / 100
    if exit_level >= trigger:
        st.error("Full-payout threshold must be lower than trigger.")
    else:
        ratios = np.linspace(0, 1.3, 131)
        payouts = [insured * payout_fraction(x, trigger, exit_level) for x in ratios]
        df = pd.DataFrame({"Rainfall ratio": ratios, "Illustrative payout (KSh)": payouts})
        fig = px.line(df, x="Rainfall ratio", y="Illustrative payout (KSh)", title="Illustrative payout curve")
        fig.update_layout(xaxis_tickformat=".0%")
        st.plotly_chart(fig, use_container_width=True)
        st.caption("This curve is a mathematical demonstration of the selected index rules, not an estimate of actual farm losses.")

elif page == "Data & methodology":
    st.subheader("Data and research methodology")
    st.markdown("""
**Data needed for a credible study**
1. Daily or dekadal rainfall observations for the selected location and growing season.
2. A clearly defined historical reference period.
3. Crop calendar and crop-specific agronomic information.
4. Historical yield or loss observations, where available.
5. Farm exposure and insured-value assumptions.

**Potential public data sources**
- CHIRPS rainfall: https://www.chc.ucsb.edu/data/chirps
- NASA POWER: https://power.larc.nasa.gov/
- Kenya Agricultural and Livestock Research Organization: https://www.kalro.org/
- Insurance Regulatory Authority of Kenya: https://www.ira.go.ke/

**Suggested validation**
- Compare gridded rainfall with available local gauge data.
- Test the index over multiple historical seasons.
- Measure basis risk: cases where the index payout differs from actual crop loss.
- Use out-of-sample validation and sensitivity analysis.
- Document missing data, uncertainty and limitations.
""")
    st.info("Do not label a result as an AI prediction until a model has been trained, tested and independently evaluated.")

else:
    st.subheader("About MavunoShield")
    st.write("""
MavunoShield is a student-led research and innovation concept exploring actuarial approaches to agricultural climate-risk awareness in Kenya.

**Vision:** Make climate-risk information and actuarial thinking more accessible to smallholder farming communities.

**Initial scope:** A transparent rainfall-index research prototype, beginning with a Kitui County case study.

**Important boundaries:** This application is educational and experimental. It is not an insurance provider, does not issue policies, does not guarantee payouts, and does not provide official weather forecasts or insurance quotations.
""")
    st.markdown("### Project details")
    st.write("Institution: The Co-operative University of Kenya (CUK)")
    st.write("Discipline: Actuarial Science")
    st.write("Project stage: Minimum viable prototype")
    st.write("Version: 0.1.0")
    st.caption("Prepared as a foundation for supervised academic research. All assumptions must be sourced and validated before publication.")
