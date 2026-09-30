import streamlit as st
from PIL import Image

from xray_model import predict
from disease_info import get_disease_info
from report import generate_pdf_report

st.set_page_config(
    page_title="Chest X-ray Disease Detection",
    page_icon="🩺",
    layout="centered"
)

# ── Custom styling ───────────────────────────────────────
st.markdown("""
<style>
    .main {
        background-color: #f5f8fb;
    }
    .block-container {
        padding-top: 2rem;
        padding-bottom: 3rem;
        max-width: 800px;
    }
    .app-header {
        text-align: center;
        padding: 1.5rem 1rem 1rem 1rem;
    }
    .app-header h1 {
        font-size: 2.1rem;
        color: #1f4e79;
        margin-bottom: 0.2rem;
    }
    .app-header p {
        color: #6c7a89;
        font-size: 0.95rem;
        margin-top: 0;
    }
    .section-card {
        background-color: #ffffff;
        border-radius: 12px;
        padding: 1.4rem 1.6rem;
        margin-bottom: 1.2rem;
        box-shadow: 0 1px 4px rgba(0,0,0,0.08);
        border: 1px solid #e8edf3;
    }
    .section-title {
        font-size: 1.05rem;
        font-weight: 700;
        color: #1f4e79;
        margin-bottom: 0.6rem;
        border-bottom: 2px solid #eaf1f8;
        padding-bottom: 0.4rem;
    }
    .disease-name-box {
        text-align: center;
        background: linear-gradient(135deg, #1f4e79, #2e6da4);
        color: white;
        border-radius: 14px;
        padding: 1.4rem;
        margin-bottom: 1.2rem;
    }
    .disease-name-box h2 {
        margin: 0;
        font-size: 1.6rem;
    }
    .checklist-item {
        padding: 4px 0;
        font-size: 0.96rem;
        color: #333;
    }
    .specialist-box {
        background-color: #eaf6ec;
        border-radius: 10px;
        padding: 0.9rem 1.2rem;
        font-size: 1.05rem;
        font-weight: 600;
        color: #256029;
        text-align: center;
    }
    .disclaimer-box {
        background-color: #f1f1f1;
        border-left: 4px solid #999;
        padding: 0.8rem 1rem;
        font-size: 0.85rem;
        color: #555;
        border-radius: 6px;
    }
    div[data-testid="stMetricValue"] {
        color: #1f4e79;
    }
    hr {
        border-top: 1px solid #e0e6ed;
    }
</style>
""", unsafe_allow_html=True)

HOME_CARE_TIPS = [
    "Drink plenty of fluids",
    "Take adequate rest",
    "Monitor oxygen level",
    "Avoid smoking"
]

SPECIALIST_MAP = {
    "Cardiomegaly": "Cardiologist",
    "Hernia": "General Surgeon",
    "Support Devices": "General Physician",
    "No Finding": "General Physician",
}
DEFAULT_SPECIALIST = "Pulmonologist"


def get_risk_level(probability):
    if probability >= 75:
        return "High", "🔴"
    elif probability >= 40:
        return "Moderate", "🟠"
    else:
        return "Low", "🟢"


def render_checklist(items):
    for item in items:
        st.markdown(f"<div class='checklist-item'>✔ {item}</div>", unsafe_allow_html=True)


# ── Header ───────────────────────────────────────────────
st.markdown("""
<div class="app-header">
    <h1>🩺 Chest X-ray Disease Detection</h1>
    <p>AI-assisted screening for common chest X-ray findings</p>
</div>
""", unsafe_allow_html=True)

uploaded_file = st.file_uploader(
    "Upload a chest X-ray image",
    type=["png", "jpg", "jpeg"]
)

if uploaded_file is not None:
    image = Image.open(uploaded_file).convert("RGB")
    st.image(image, caption="Uploaded X-ray", use_container_width=True)

    with st.spinner("Analyzing X-ray..."):
        results = predict(image)

    top_result = results[0]
    disease_name = top_result["Disease"]
    probability = top_result["Probability"]
    risk_level, risk_emoji = get_risk_level(probability)
    info = get_disease_info(disease_name)
    specialist = SPECIALIST_MAP.get(disease_name, DEFAULT_SPECIALIST)

    # Disease name banner
    st.markdown(f"""
    <div class="disease-name-box">
        <h2>{disease_name}</h2>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        st.metric("Probability", f"{probability}%")
    with col2:
        st.markdown(f"**Risk Level**  \n{risk_emoji} {risk_level}")

    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Description</div>', unsafe_allow_html=True)
    st.write(info["description"])
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Symptoms</div>', unsafe_allow_html=True)
    render_checklist(info["symptoms"])
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Possible Causes</div>', unsafe_allow_html=True)
    render_checklist(info["causes"])
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Home Care</div>', unsafe_allow_html=True)
    render_checklist(HOME_CARE_TIPS)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Treatment</div>', unsafe_allow_html=True)
    render_checklist(info["treatment"])
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Recommended Specialist</div>', unsafe_allow_html=True)
    st.markdown(f"""<div class="specialist-box">👨‍⚕️ {specialist}</div>""", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Emergency Warning</div>', unsafe_allow_html=True)
    st.warning(
        "🚨 Seek immediate medical care if oxygen saturation falls below "
        "90%, severe chest pain develops, or breathing becomes very difficult."
    )
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown(f"""
    <div class="disclaimer-box">
        <strong>Disclaimer:</strong> This AI prediction is for screening purposes only
        and is not a confirmed medical diagnosis.
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")
    pdf_bytes = generate_pdf_report(
        disease_name, probability, risk_level, info, specialist
    )
    st.download_button(
        label="📄 Download PDF Report",
        data=pdf_bytes,
        file_name=f"xray_report_{disease_name.replace(' ', '_')}.pdf",
        mime="application/pdf"
    )

    with st.expander("See all detected findings (full probability list)"):
        for r in results:
            st.write(f"{r['Disease']}: {r['Probability']}%")
else:
    st.info("👆 Upload a chest X-ray image to get started.")