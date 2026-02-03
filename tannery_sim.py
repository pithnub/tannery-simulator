import streamlit as st

# --- INITIAL SETUP ---
st.set_page_config(page_title="Tannery Pro Sim v3.5", layout="wide")

# Custom Styling for the Lab Report
st.markdown("""
    <style>
    .report-box {
        background-color: #f8f9fa;
        padding: 25px;
        border-radius: 12px;
        border-left: 8px solid #34495e;
        color: #2c3e50;
        font-family: 'Courier New', Courier, monospace;
    }
    .metric-card {
        background-color: #ffffff;
        padding: 15px;
        border-radius: 8px;
        box-shadow: 2px 2px 5px rgba(0,0,0,0.1);
    }
    </style>
    """, unsafe_allow_html=True)

st.title("革 The Tannery Master Simulator")
st.write("---")

# --- SIDEBAR: MISSION CONTROL ---
st.sidebar.header("🎯 Target Production Brief")
mission = st.sidebar.selectbox(
    "Select End-Use:", 
    ["Rugged Combat Boot", "Luxury Upholstery Nappa", "Classic Oxford Shoe"]
)

# Dynamic Brief Info
briefs = {
    "Rugged Combat Boot": {"thick": "2.0-2.2mm", "ph": "4.5-4.8", "spec": "Waterproof / High Tensile"},
    "Luxury Upholstery Nappa": {"thick": "0.9-1.1mm", "ph": "5.0-5.5", "spec": "High Drape / Low Fogging"},
    "Classic Oxford Shoe": {"thick": "1.4-1.6mm", "ph": "4.8-5.0", "spec": "Tight Break / High Shine"}
}

st.sidebar.info(f"""
**Technical Requirements:**
- Target Thickness: {briefs[mission]['thick']}
- Ideal Neutralization pH: {briefs[mission]['ph']}
- Key Spec: {briefs[mission]['spec']}
""")

# --- INPUT SECTION ---
col1, col2 = st.columns(2)

with col1:
    st.header("1. Mechanical & Neutralization")
    shave = st.slider("Shave Thickness (mm)", 0.5, 3.0, 1.5, help="Sets the potential strength envelope.")
    neutral_ph = st.slider("Neutralization pH", 3.0, 7.0, 4.8, help="Determines depth of chemical penetration.")
    
    st.header("2. Retanning Blend")
    retans = st.multiselect("Select Agents:", ["Mimosa (Veg)", "Phenolic Syntan", "Acrylic Resin", "Chrome III"])
    
with col2:
    st.header("3. Lubrication & Fixation")
    fat_type = st.selectbox("Fatliquor Chemistry:", ["Fish Oil (Standard)", "Synthetic (Low Fog)", "Waterproof Polymer"])
    fat_level = st.slider("Fatliquor Dosage (%)", 2, 20, 8)
    
    st.header("4. Finishing & Protection")
    adhesion = st.checkbox("Apply Adhesion/Seal Coat?", value=True)
    finish_sys = st.selectbox("Finish System:", ["Aniline", "Semi-Aniline", "Pigmented"])

# --- THE SIMULATION ENGINE ---
st.write("---")
if st.button("🚀 EXECUTE PRODUCTION RUN"):
    score = 100
    warnings = []
    microscope = ""
    handle = ""

    # --- ANALYTICAL LAB LOGIC ---
    # PH Logic
    if neutral_ph < 4.2:
        score -= 30
        microscope = "Fibers congested at the surface; 'Case-hardened' shell visible. Center is white/starved."
        handle = "Boardy and 'tinny'. Grain will crack under tension."
    elif neutral_ph > 5.8:
        score -= 25
        microscope = "Excessive fiber bundles separation. Connection between grain and corium is frayed."
        handle = "Loose and spongy. Poor 'snap' and terrible piping."
    else:
        microscope = "Uniform chemical distribution. Fiber bundles are well-split and lubricated to the core."
        handle = "Balanced stand with a tight, fine break."

    # Mission-Specific Penalties
    if mission == "Rugged Combat Boot":
        if shave < 1.8: score -= 30; warnings.append("❌ FAIL: Tensile strength below safety limits.")
        if fat_type != "Waterproof Polymer": score -= 40; warnings.append("❌ FAIL: Leaked in Bally Flex test.")
        
    elif mission == "Luxury Upholstery Nappa":
        if fat_type == "Fish Oil (Standard)": score -= 50; warnings.append("❌ FAIL: High VOCs - windshield fogging detected.")
        if "Mimosa (Veg)" in retans: score -= 20; warnings.append("⚠️ Hand is too firm for upholstery.")
        
    elif mission == "Classic Oxford Shoe":
        if "Phenolic Syntan" not in retans: score -= 20; warnings.append("⚠️ Grain break is too coarse for formal footwear.")
        if shave > 1.8: warnings.append("⚠️ Too thick; lasting machines will struggle.")

    if not adhesion:
        score -= 40
        warnings.append("❌ CRITICAL: Finish failed rub-fastness test (Delamination).")

    # --- RESULTS DISPLAY ---
    c_lab, c_feedback = st.columns([2, 1])
    
    with c_lab:
        st.markdown(f"""
        <div class="report-box">
            <h3>🔬 ANALYTICAL LAB REPORT</h3>
            <p><strong>Microscope View:</strong> {microscope}</p>
            <p><strong>Physical Handle:</strong> {handle}</p>
            <p><strong>Chemical Fixation:</strong> {'Stable' if 4.0 < neutral_ph < 5.5 else 'Unstable/Surface Heavy'}</p>
        </div>
        """, unsafe_allow_html=True)

    with c_feedback:
        st.subheader("Factory Feedback")
        if score >= 80:
            st.success(f"Score: {score}/100")
            st.write("🌟 'The best batch we've seen this month. Perfect for the cutting room!'")
            st.balloons()
        elif score >= 50:
            st.warning(f"Score: {score}/100")
            st.write("⚖️ 'Acceptable as B-Grade, but we'll have to discount the price.'")
        else:
            st.error(f"Score: {score}/100")
            st.write("🗑️ 'Scrap. This doesn't even feel like leather. Send it to the landfill.'")

    if warnings:
        st.markdown("### ⚠️ Non-Conformance Issues")
        for w in warnings:
            st.write(w)
