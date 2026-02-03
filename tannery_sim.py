import streamlit as st

# --- INITIAL SETUP ---
st.set_page_config(page_title="Tannery Pro: Arcade Edition", layout="wide")

# Custom Styling
st.markdown("""
    <style>
    .report-box { background-color: #f8f9fa; padding: 20px; border-radius: 12px; border-left: 8px solid #34495e; }
    .leaderboard { background-color: #1e1e1e; color: #00ff00; padding: 15px; border-radius: 10px; font-family: 'Courier New', monospace; }
    </style>
    """, unsafe_allow_html=True)

st.title("革 Tannery Master: Arcade Edition")

# --- SIDEBAR: LEADERBOARD ---
with st.sidebar:
    st.header("🏆 GLOBAL LEADERBOARD")
    st.markdown("""
    <div class="leaderboard">
    1. L. Pasteur ... 98 pts<br>
    2. H. Kohlstamm .. 94 pts<br>
    3. Pithnub (YOU) . ?? pts<br>
    4. Apprentice .... 45 pts
    </div>
    """, unsafe_allow_html=True)
    st.write("---")
    mission = st.selectbox("Select End-Use:", ["Rugged Combat Boot", "Luxury Upholstery Nappa", "Classic Oxford Shoe"])

# --- INPUTS ---
col1, col2 = st.columns(2)
with col1:
    st.header("1. Wet-End Prep")
    shave = st.slider("Shave Thickness (mm)", 0.5, 3.0, 1.5)
    neutral_ph = st.slider("Neutralization pH", 3.0, 7.0, 4.8)
    retans = st.multiselect("Retanning Blend:", ["Mimosa (Veg)", "Phenolic Syntan", "Acrylic Resin", "Chrome III"])
    
with col2:
    st.header("2. Fat & Finish")
    fat_type = st.selectbox("Fatliquor Chemistry:", ["Fish Oil (Standard)", "Synthetic (Low Fog)", "Waterproof Polymer"])
    adhesion = st.checkbox("Apply Adhesion/Seal Coat?", value=True)
    finish_sys = st.selectbox("Finish System:", ["Aniline", "Semi-Aniline", "Pigmented"])

# --- ARCADE ENGINE ---
if st.button("🚀 RUN PRODUCTION BATCH"):
    score = 100
    cost = 10.00 # Base cost per sq ft
    
    # Logic: Chemicals increase cost
    cost += len(retans) * 1.50
    if fat_type == "Waterproof Polymer": cost += 3.00
    
    # Technical Logic (Adaptive pH)
    if neutral_ph < 4.2: score -= 30
    elif neutral_ph > 5.8 and shave >= 1.8: score -= 25
    
    # Mission Check
    if mission == "Rugged Combat Boot" and fat_type != "Waterproof Polymer": score -= 40
    if not adhesion: score -= 40

    score = max(0, score)
    
    # --- RESULTS ---
    st.write("---")
    c1, c2 = st.columns(2)
    
    with c1:
        st.subheader("🔬 Lab Analysis")
        st.info(f"Final Quality Score: {score}/100")
        if score >= 80: st.balloons()
        
    with c2:
        st.subheader("💰 Commercials")
        st.metric("Production Cost", f"${cost:.2f} /sqft", delta=f"{cost-10:.2f} Over Base")

    if score < 50:
        st.error("BATCH REJECTED: Send to landfill.")
    else:
        st.success("BATCH APPROVED: Ready for shipment.")
