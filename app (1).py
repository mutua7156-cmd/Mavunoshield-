import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from pathlib import Path

st.set_page_config(page_title="MavunoShield V2.0 | Actuarial Research", page_icon="🌱", layout="wide")

st.title("🌱 MavunoShield V2.0")
st.subheader("Actuarial modelling for rainfall-index agricultural climate-risk research")
st.caption("VERSION 2.0 • Student research prototype • Kenya pilot • Not an insurance quotation, regulated product, or weather forecast")

with st.sidebar:
    st.header("MavunoShield V2.0")
    st.caption("Actuarial research platform")
    page = st.radio("Choose a module", [
        "Overview", "Farm assessment", "Historical rainfall analysis",
        "Index contract & pricing", "Scenario explorer", "Methodology & limitations"
    ])

def payout_fraction(ratio, trigger, exit_level):
    """Linear payout: 0 above trigger; 100% at/below exit level."""
    if ratio >= trigger:
        return 0.0
    if ratio <= exit_level:
        return 1.0
    return (trigger - ratio) / (trigger - exit_level)

if page == "Overview":
    st.markdown("""
    MavunoShield is a student-built research platform for exploring how rainfall-index
    insurance concepts and actuarial methods can support agricultural climate-risk analysis.
    The first pilot geography is Kitui County, Kenya.
    """)
    c1, c2, c3 = st.columns(3)
    c1.metric("Research focus", "Rainfall index")
    c2.metric("Pilot geography", "Kitui, Kenya")
    c3.metric("Primary discipline", "Actuarial science")
    st.info("The current application is a research prototype. It does not sell insurance, issue policies, determine official drought status, or guarantee a payout.")
    st.success("Version 2.0 introduces historical rainfall CSV analysis, a preliminary historical-burn-cost pricing module, improved scenario exploration and clearer research limitations.")
    st.markdown("### What the platform can do")
    st.markdown("""
    - Calculate rainfall ratios and deficits against a user-supplied reference.
    - Illustrate a transparent parametric payout function.
    - Analyse uploaded historical rainfall observations.
    - Estimate a preliminary pure premium from historical simulated payouts when suitable data are supplied.
    - Explore how contract parameters affect payouts.
    """)
    st.markdown("### Important data rule")
    st.warning("Do not interpret the included example values as observed Kitui climate data. Upload quality-controlled observations from a documented source before making empirical claims.")

elif page == "Farm assessment":
    st.header("Farm-level rainfall-index illustration")
    st.write("Enter a reference rainfall amount and the observed rainfall for the same defined location and crop season.")
    a, b = st.columns(2)
    with a:
        county = st.selectbox("County", ["Kitui", "Makueni", "Machakos", "Other"])
        crop = st.selectbox("Crop", ["Maize", "Beans", "Sorghum", "Green grams", "Other"])
        acreage = st.number_input("Farm size (acres)", min_value=0.1, value=2.0, step=0.1)
        expected = st.number_input("Reference seasonal rainfall (mm)", min_value=1.0, value=500.0, step=10.0)
        observed = st.number_input("Observed seasonal rainfall (mm)", min_value=0.0, value=250.0, step=10.0)
    with b:
        value_per_acre = st.number_input("Insured value per acre (KSh)", min_value=1.0, value=30000.0, step=1000.0)
        trigger = st.slider("Payout trigger (rainfall ratio)", 0.10, 1.00, 0.80, 0.05)
        exit_level = st.slider("Exit level (rainfall ratio)", 0.00, 0.95, 0.50, 0.05)
        illustrative_rate = st.number_input("Illustrative premium rate (%)", min_value=0.0, value=5.0, step=0.5)
    if exit_level >= trigger:
        st.error("Exit level must be lower than trigger.")
    else:
        ratio = observed / expected
        deficit = max(0.0, 1.0 - ratio)
        insured = acreage * value_per_acre
        fraction = payout_fraction(ratio, trigger, exit_level)
        premium = insured * illustrative_rate / 100
        payout = insured * fraction
        x1, x2, x3, x4 = st.columns(4)
        x1.metric("Rainfall ratio", f"{ratio:.1%}")
        x2.metric("Rainfall deficit", f"{deficit:.1%}")
        x3.metric("Illustrative premium", f"KSh {premium:,.0f}")
        x4.metric("Illustrative index payout", f"KSh {payout:,.0f}")
        st.write(f"**Farm profile:** {county} County • {crop} • {acreage:g} acres")
        st.write(f"**Payout fraction:** {fraction:.1%}")
        st.warning("The premium rate is user-entered and illustrative. It is not actuarially priced. The payout is determined by the selected index contract, not verified crop loss. This creates basis risk.")

elif page == "Historical rainfall analysis":
    st.header("Historical rainfall analysis")
    st.write("Upload a CSV containing at least `year` and `rainfall_mm`. Optional columns: `season`, `location`, `source`.")
    uploaded = st.file_uploader("Upload rainfall CSV", type=["csv"])
    if uploaded:
        try:
            df = pd.read_csv(uploaded)
            required = {"year", "rainfall_mm"}
            if not required.issubset(df.columns):
                st.error("CSV must contain columns named year and rainfall_mm.")
            else:
                df["year"] = pd.to_numeric(df["year"], errors="coerce")
                df["rainfall_mm"] = pd.to_numeric(df["rainfall_mm"], errors="coerce")
                df = df.dropna(subset=["year", "rainfall_mm"]).sort_values("year")
                if df.empty:
                    st.error("No valid rainfall observations were found.")
                else:
                    st.success(f"Loaded {len(df)} valid observations.")
                    st.dataframe(df, use_container_width=True)
                    if "season" in df.columns:
                        season = st.selectbox("Filter season", ["All"] + sorted(df["season"].dropna().astype(str).unique().tolist()))
                        view = df if season == "All" else df[df["season"].astype(str) == season]
                    else:
                        view = df
                    st.subheader("Descriptive statistics")
                    stats = view["rainfall_mm"].describe()
                    st.dataframe(stats.to_frame("rainfall_mm").T, use_container_width=True)
                    st.plotly_chart(px.line(view, x="year", y="rainfall_mm", color="season" if "season" in view.columns else None,
                                             markers=True, title="Rainfall observations over time"), use_container_width=True)
                    threshold = st.number_input("Illustrative drought threshold (mm)", min_value=0.0,
                                                value=float(view["rainfall_mm"].quantile(0.20)), step=5.0)
                    droughts = view[view["rainfall_mm"] < threshold]
                    st.metric("Observations below threshold", f"{len(droughts)} / {len(view)}",
                              f"{len(droughts)/len(view):.1%} of uploaded observations")
                    st.caption("This frequency is conditional on the uploaded data, chosen threshold, location and season. It is not automatically a county-wide drought probability.")
                    st.download_button("Download cleaned data", view.to_csv(index=False), "mavunoshield_cleaned_rainfall.csv", "text/csv")
        except Exception as e:
            st.error(f"Could not read the file: {e}")
    else:
        st.info("No real rainfall dataset is bundled. This prevents invented or unverified observations from being mistaken for measured climate data.")

elif page == "Index contract & pricing":
    st.header("Transparent index contract and preliminary pricing")
    st.write("This module prices a simple contract from historical observations supplied by the researcher.")
    st.markdown("""
    **Contract payout:** for rainfall ratio `R`, trigger `T`, and exit level `E` where `E < T`:
    - 0% payout when `R ≥ T`
    - 100% payout when `R ≤ E`
    - Linear payout between E and T
    """)
    uploaded = st.file_uploader("Upload historical seasonal rainfall CSV", type=["csv"], key="pricing")
    c1, c2, c3 = st.columns(3)
    ref = c1.number_input("Reference rainfall (mm)", min_value=1.0, value=500.0, key="refp")
    trigger = c2.slider("Trigger ratio", 0.10, 1.00, 0.80, 0.05, key="tp")
    exit_level = c3.slider("Exit ratio", 0.00, 0.95, 0.50, 0.05, key="ep")
    sum_insured = st.number_input("Sum insured per simulated policy (KSh)", min_value=1.0, value=60000.0, step=1000.0)
    expense_loading = st.number_input("Expense and risk loading (%)", min_value=0.0, value=20.0, step=1.0)
    if exit_level >= trigger:
        st.error("Exit level must be lower than trigger.")
    elif uploaded:
        df = pd.read_csv(uploaded)
        if not {"year", "rainfall_mm"}.issubset(df.columns):
            st.error("CSV must contain year and rainfall_mm.")
        else:
            df["rainfall_mm"] = pd.to_numeric(df["rainfall_mm"], errors="coerce")
            df = df.dropna(subset=["rainfall_mm"])
            if len(df) < 5:
                st.error("At least five valid seasonal observations are required for this preliminary illustration; more are strongly recommended.")
            else:
                df["rainfall_ratio"] = df["rainfall_mm"] / ref
                df["payout_fraction"] = df["rainfall_ratio"].apply(lambda r: payout_fraction(r, trigger, exit_level))
                df["simulated_payout_ksh"] = df["payout_fraction"] * sum_insured
                pure_premium = df["simulated_payout_ksh"].mean()
                loaded_premium = pure_premium * (1 + expense_loading/100)
                st.metric("Historical average simulated payout (pure premium)", f"KSh {pure_premium:,.2f}")
                st.metric("Loaded indicative premium", f"KSh {loaded_premium:,.2f}")
                st.dataframe(df, use_container_width=True)
                st.plotly_chart(px.bar(df, x="year", y="simulated_payout_ksh", title="Simulated historical contract payouts"), use_container_width=True)
                st.download_button("Download pricing analysis", df.to_csv(index=False), "mavunoshield_pricing_analysis.csv", "text/csv")
                st.warning("This is a preliminary historical-burn-cost estimate, not a complete commercial tariff. It omits credibility adjustment, parameter uncertainty, reinsurance, capital costs, taxes, adverse selection, data error and regulatory requirements.")
    else:
        st.info("Upload quality-controlled seasonal rainfall data to calculate an empirical historical-burn-cost illustration.")

elif page == "Scenario explorer":
    st.header("Scenario explorer")
    ref = st.number_input("Reference rainfall (mm)", min_value=1.0, value=500.0)
    observed = st.slider("Observed rainfall (mm)", 0.0, float(max(1000, ref*1.5)), float(ref*0.5), 10.0)
    trigger = st.slider("Trigger ratio", 0.10, 1.00, 0.80, 0.05)
    exit_level = st.slider("Exit ratio", 0.00, 0.95, 0.50, 0.05)
    insured = st.number_input("Sum insured (KSh)", min_value=1.0, value=60000.0, step=1000.0)
    if exit_level >= trigger:
        st.error("Exit level must be lower than trigger.")
    else:
        ratios = np.linspace(0, 1.5, 151)
        curve = pd.DataFrame({"rainfall_ratio": ratios,
                              "payout_fraction": [payout_fraction(r, trigger, exit_level) for r in ratios]})
        curve["payout_ksh"] = curve["payout_fraction"] * insured
        current = observed/ref
        st.metric("Current scenario payout", f"KSh {payout_fraction(current, trigger, exit_level)*insured:,.0f}")
        st.plotly_chart(px.line(curve, x="rainfall_ratio", y="payout_ksh", title="Contract payout against rainfall ratio"), use_container_width=True)

else:
    st.header("Methodology, assumptions and limitations")
    st.markdown("""
    ### Research design
    The prototype demonstrates a rainfall-index contract using a defined rainfall reference, trigger and exit level. Historical observations are required to estimate empirical payout frequency and a preliminary burn-cost premium.

    ### Core variables
    - Rainfall ratio = observed seasonal rainfall / reference seasonal rainfall.
    - Rainfall deficit = max(0, 1 − rainfall ratio).
    - Sum insured = acreage × insured value per acre.
    - Simulated payout = sum insured × payout fraction.

    ### Data requirements
    Use a documented rainfall source, location or grid cell, season definition, units, observation period, missing-data treatment and quality-control procedure. Do not mix daily, monthly and seasonal totals without a consistent aggregation method.

    ### Key actuarial risks
    - **Basis risk:** the index payout may differ from the farmer's actual loss.
    - **Parameter risk:** trigger, exit level and reference rainfall may be poorly selected.
    - **Data risk:** satellite estimates and station observations can differ; missing values and spatial representativeness matter.
    - **Model risk:** a simple burn-cost estimate may be unstable with short or non-representative history.

    ### Limitations
    This software is not an insurer, does not issue policies, does not provide official weather forecasts, and does not constitute a regulated insurance product. Any academic or commercial claim requires validation with local agronomic evidence, crop-loss data, expert review and applicable regulatory guidance.
    """)
    st.markdown("### Suggested validation before any pilot")
    st.markdown("""
    1. Compare rainfall estimates with quality-controlled KMD station observations.
    2. Define crop-specific planting and harvest windows with agronomic experts.
    3. Obtain historical yield or crop-loss data for the same locations and seasons.
    4. Quantify false positives, false negatives and payout-loss correlation.
    5. Test out-of-sample performance and sensitivity to contract parameters.
    6. Obtain actuarial, agricultural and regulatory review.
    """)
