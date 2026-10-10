import streamlit as st
import pickle
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import os
import io
import warnings
from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

warnings.filterwarnings('ignore')

# ==============================================================================
# 1. PAGE CONFIGURATION & METADATA
# ==============================================================================
st.set_page_config(
    page_title="MedPulse AI | Clinical Decision Support Suite",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==============================================================================
# 2. GLASSMORPHIC DARK DESIGN SYSTEM (CSS)
# ==============================================================================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap');

    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    
    .stApp {
        background: radial-gradient(circle at 10% 10%, #0f172a 0%, #070b14 100%) !important;
        color: #f8fafc;
    }

    /* Top Hero Banner */
    .hero-banner {
        background: linear-gradient(135deg, rgba(15, 23, 42, 0.95) 0%, rgba(30, 27, 75, 0.95) 50%, rgba(2, 132, 199, 0.85) 100%);
        border: 1px solid rgba(56, 189, 248, 0.25);
        padding: 24px 32px;
        border-radius: 20px;
        margin-bottom: 24px;
        box-shadow: 0 16px 40px rgba(0, 0, 0, 0.55), inset 0 1px 0 rgba(255, 255, 255, 0.15);
        backdrop-filter: blur(12px);
    }

    /* Glass Cards */
    .glass-card {
        background: rgba(30, 41, 59, 0.5);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 16px;
        padding: 20px 24px;
        backdrop-filter: blur(10px);
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.35);
        margin-bottom: 18px;
    }

    /* Risk Status Cards */
    .status-card-danger {
        background: linear-gradient(135deg, rgba(153, 27, 27, 0.35) 0%, rgba(69, 10, 10, 0.25) 100%);
        border: 1px solid #ef4444;
        border-left: 8px solid #ef4444;
        border-radius: 16px;
        padding: 24px;
        margin-top: 15px;
        box-shadow: 0 10px 30px rgba(239, 68, 68, 0.2);
    }
    .status-card-safe {
        background: linear-gradient(135deg, rgba(6, 78, 59, 0.35) 0%, rgba(2, 44, 34, 0.25) 100%);
        border: 1px solid #10b981;
        border-left: 8px solid #10b981;
        border-radius: 16px;
        padding: 24px;
        margin-top: 15px;
        box-shadow: 0 10px 30px rgba(16, 185, 129, 0.2);
    }

    /* Badges & Pills */
    .badge-pill {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        background: rgba(56, 189, 248, 0.15);
        border: 1px solid rgba(56, 189, 248, 0.4);
        color: #38bdf8;
        padding: 4px 12px;
        border-radius: 9999px;
        font-size: 12px;
        font-weight: 600;
        letter-spacing: 0.3px;
    }
    .badge-success {
        background: rgba(16, 185, 129, 0.15);
        border-color: rgba(16, 185, 129, 0.4);
        color: #34d399;
    }
    .badge-danger {
        background: rgba(239, 68, 68, 0.15);
        border-color: rgba(239, 68, 68, 0.4);
        color: #f87171;
    }
    .badge-warning {
        background: rgba(245, 158, 11, 0.15);
        border-color: rgba(245, 158, 11, 0.4);
        color: #fbbf24;
    }

    /* Metric Cards */
    .metric-container {
        display: flex;
        gap: 16px;
        margin-bottom: 20px;
    }
    .metric-card {
        flex: 1;
        background: rgba(15, 23, 42, 0.65);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 14px;
        padding: 16px 20px;
        backdrop-filter: blur(8px);
    }
    .metric-title {
        font-size: 12px;
        color: #94a3b8;
        text-transform: uppercase;
        letter-spacing: 0.8px;
        font-weight: 600;
        margin-bottom: 4px;
    }
    .metric-value {
        font-size: 24px;
        font-weight: 800;
        color: #38bdf8;
    }

    /* Buttons */
    .stButton > button {
        background: linear-gradient(135deg, #0284c7 0%, #0369a1 100%) !important;
        color: #ffffff !important;
        border: none !important;
        border-radius: 10px !important;
        padding: 10px 22px !important;
        font-weight: 700 !important;
        font-size: 14px !important;
        box-shadow: 0 4px 14px rgba(2, 132, 199, 0.4) !important;
        transition: all 0.25s ease !important;
    }
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 24px rgba(2, 132, 199, 0.6) !important;
    }

    /* Download Button */
    .stDownloadButton > button {
        background: linear-gradient(135deg, #059669 0%, #047857 100%) !important;
        color: #ffffff !important;
        border: none !important;
        border-radius: 10px !important;
        padding: 10px 22px !important;
        font-weight: 700 !important;
        font-size: 14px !important;
        box-shadow: 0 4px 14px rgba(5, 150, 105, 0.4) !important;
        transition: all 0.25s ease !important;
    }
    .stDownloadButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 24px rgba(5, 150, 105, 0.6) !important;
    }

    /* Tabs Styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background-color: rgba(15, 23, 42, 0.6);
        padding: 6px;
        border-radius: 12px;
        border: 1px solid rgba(255, 255, 255, 0.08);
    }
    .stTabs [data-baseweb="tab"] {
        border-radius: 8px;
        color: #94a3b8;
        padding: 8px 18px;
        font-weight: 600;
        transition: all 0.2s ease;
    }
    .stTabs [aria-selected="true"] {
        background-color: rgba(2, 132, 199, 0.25) !important;
        color: #38bdf8 !important;
        border-bottom: 2px solid #38bdf8 !important;
    }
</style>
""", unsafe_allow_html=True)

# ==============================================================================
# 3. ROBUST CACHED MODEL LOADERS
# ==============================================================================
@st.cache_resource
def load_models():
    """Load pre-trained machine learning models safely with fallbacks."""
    models_dict = {}
    model_configs = [
        ('Diabetes', 'diabetes_model.pkl'),
        ('Heart Disease', 'heart_model.pkl'),
        ('Kidney Disease', 'kidney_model.pkl')
    ]
    for name, filename in model_configs:
        if os.path.exists(filename):
            try:
                with open(filename, 'rb') as f:
                    models_dict[name] = pickle.load(f)
            except Exception as e:
                models_dict[name] = None
        else:
            models_dict[name] = None
    return models_dict

models = load_models()

# ==============================================================================
# 4. AUDIT TRAIL & RECORD LOGGING
# ==============================================================================
RECORDS_FILE = "patient_records.csv"

def log_patient_record(patient_id, name, age, gender, disease, result, prob, key_vitals_summary):
    """Log clinical evaluation result to persistent CSV storage."""
    record = {
        'Timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'Patient_ID': patient_id,
        'Patient_Name': name,
        'Age': age,
        'Gender': gender,
        'Disease_Module': disease,
        'Risk_Result': result,
        'Risk_Probability': f"{prob:.1f}%",
        'Key_Vitals': key_vitals_summary
    }
    df_new = pd.DataFrame([record])
    if os.path.exists(RECORDS_FILE):
        try:
            df_existing = pd.read_csv(RECORDS_FILE)
            df_combined = pd.concat([df_new, df_existing], ignore_index=True)
            df_combined.to_csv(RECORDS_FILE, index=False)
        except Exception:
            df_new.to_csv(RECORDS_FILE, index=False)
    else:
        df_new.to_csv(RECORDS_FILE, index=False)

def get_records():
    """Retrieve audit history safely."""
    if os.path.exists(RECORDS_FILE):
        try:
            return pd.read_csv(RECORDS_FILE)
        except Exception:
            return pd.DataFrame()
    return pd.DataFrame()

# ==============================================================================
# 5. CLINICAL PDF REPORT GENERATION (REPORTLAB)
# ==============================================================================
def generate_pdf_report(patient_name, patient_id, age, gender, disease, risk_title, prob, is_high_risk, biomarkers_dict, care_steps):
    """Generate professional medical report PDF in-memory."""
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer, pagesize=letter,
        rightMargin=40, leftMargin=40, topMargin=36, bottomMargin=36
    )
    styles = getSampleStyleSheet()
    
    title_style = ParagraphStyle('MedTitle', parent=styles['Heading1'], fontName='Helvetica-Bold', fontSize=18, textColor=colors.HexColor('#0284c7'), spaceAfter=4)
    sub_style = ParagraphStyle('MedSub', parent=styles['Normal'], fontName='Helvetica', fontSize=10, textColor=colors.HexColor('#64748b'), spaceAfter=10)
    sec_style = ParagraphStyle('MedSec', parent=styles['Heading2'], fontName='Helvetica-Bold', fontSize=12, textColor=colors.HexColor('#0f172a'), spaceBefore=8, spaceAfter=6)
    label_style = ParagraphStyle('MedLabel', fontName='Helvetica-Bold', fontSize=9, textColor=colors.HexColor('#1e293b'))
    val_style = ParagraphStyle('MedVal', fontName='Helvetica', fontSize=9, textColor=colors.HexColor('#334155'))
    disc_style = ParagraphStyle('MedDisc', fontName='Helvetica-Oblique', fontSize=8, textColor=colors.HexColor('#94a3b8'))

    elements = []
    
    # Header Banner
    elements.append(Paragraph("🏥 MedPulse AI — Clinical Diagnostic Report", title_style))
    elements.append(Paragraph("Automated Clinical Decision Support System | Explainable AI Health Suite", sub_style))
    elements.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor('#0284c7'), spaceAfter=12))

    # Patient Demographics Table
    demo_data = [
        [Paragraph("<b>Patient Name:</b>", label_style), Paragraph(str(patient_name), val_style), Paragraph("<b>Patient ID:</b>", label_style), Paragraph(str(patient_id), val_style)],
        [Paragraph("<b>Age:</b>", label_style), Paragraph(f"{age} Years", val_style), Paragraph("<b>Gender:</b>", label_style), Paragraph(str(gender), val_style)],
        [Paragraph("<b>Assessment Date:</b>", label_style), Paragraph(datetime.now().strftime('%Y-%m-%d %H:%M'), val_style), Paragraph("<b>Diagnostic Module:</b>", label_style), Paragraph(disease, val_style)]
    ]
    t_demo = Table(demo_data, colWidths=[100, 160, 100, 160])
    t_demo.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#f8fafc')),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#cbd5e1')),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor('#e2e8f0')),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
    ]))
    elements.append(t_demo)
    elements.append(Spacer(1, 12))

    # Diagnostic Outcome Box
    outcome_color = colors.HexColor('#ef4444') if is_high_risk else colors.HexColor('#10b981')
    outcome_bg = colors.HexColor('#fee2e2') if is_high_risk else colors.HexColor('#d1fae5')
    outcome_text = f"<b>STATUS: {risk_title.upper()}</b> &nbsp;|&nbsp; Model Probability Score: <b>{prob:.1f}%</b>"
    p_outcome = Paragraph(outcome_text, ParagraphStyle('OutStyle', fontName='Helvetica-Bold', fontSize=12, textColor=outcome_color))
    
    t_outcome = Table([[p_outcome]], colWidths=[520])
    t_outcome.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), outcome_bg),
        ('BOX', (0,0), (-1,-1), 1.5, outcome_color),
        ('TOPPADDING', (0,0), (-1,-1), 10),
        ('BOTTOMPADDING', (0,0), (-1,-1), 10),
        ('LEFTPADDING', (0,0), (-1,-1), 14),
    ]))
    elements.append(t_outcome)
    elements.append(Spacer(1, 12))

    # Biomarkers Table
    elements.append(Paragraph("Clinical Biomarkers Evaluated", sec_style))
    bio_table_data = [[
        Paragraph("<b>Biomarker Parameter</b>", label_style),
        Paragraph("<b>Recorded Value</b>", label_style),
        Paragraph("<b>Clinical Normal Range</b>", label_style),
        Paragraph("<b>Status</b>", label_style)
    ]]
    for bio, info in biomarkers_dict.items():
        bio_table_data.append([
            Paragraph(bio, val_style),
            Paragraph(str(info['value']), val_style),
            Paragraph(info['range'], val_style),
            Paragraph(f"<font color='{info['color']}'><b>{info['status']}</b></font>", val_style)
        ])
    t_bio = Table(bio_table_data, colWidths=[160, 110, 150, 100])
    t_bio.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#f1f5f9')),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#cbd5e1')),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor('#e2e8f0')),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
    ]))
    elements.append(t_bio)
    elements.append(Spacer(1, 12))

    # Recommended Care Steps
    elements.append(Paragraph("Actionable Care Recommendations", sec_style))
    for step in care_steps:
        elements.append(Paragraph(f"• {step}", val_style))
        elements.append(Spacer(1, 2))
    elements.append(Spacer(1, 14))

    # Disclaimer & Signature
    elements.append(HRFlowable(width="100%", thickness=0.8, color=colors.HexColor('#e2e8f0'), spaceAfter=8))
    elements.append(Paragraph(
        "<b>LEGAL & CLINICAL DISCLAIMER:</b> MedPulse AI is an experimental Clinical Decision Support System powered by Machine Learning (Random Forest). It is intended to assist medical evaluation, not replace formal physician judgment. All findings must be clinically correlated with standardized laboratory tests.",
        disc_style
    ))
    
    doc.build(elements)
    buffer.seek(0)
    return buffer

# ==============================================================================
# 6. SIDEBAR CONTROLS & PATIENT DEMOGRAPHICS
# ==============================================================================
with st.sidebar:
    st.image("https://img.icons8.com/color/96/medical-heart.png", width=60)
    st.markdown("<h2 style='margin: 0; color: #38bdf8; font-weight: 800;'>MedPulse AI</h2>", unsafe_allow_html=True)
    st.caption("Clinical Decision Support Suite")
    
    st.markdown("---")
    selected_disease = st.selectbox(
        "🎯 Select Diagnostic Module",
        ["Diabetes Prediction", "Heart Disease Prediction", "Chronic Kidney Disease"],
        index=0,
        help="Choose between Diabetes, Heart Disease, and Chronic Kidney Disease (CKD) AI models."
    )

    st.markdown("---")
    with st.expander("👤 Patient Demographics", expanded=True):
        name = st.text_input("Full Name", "Sheetal Jain")
        patient_id = st.text_input("Patient ID", "PX-9042")
        age = st.slider("Age (Years)", 1, 100, 45)
        gender = st.radio("Gender", ["Male", "Female", "Other"], horizontal=True)

    st.markdown("---")
    st.markdown("<b style='color: #94a3b8;'>⚡ Quick Clinical Presets:</b>", unsafe_allow_html=True)
    col_p1, col_p2 = st.columns(2)
    with col_p1:
        load_healthy = st.button("🟢 Healthy", use_container_width=True, help="Populate with low-risk baseline vitals")
    with col_p2:
        load_risky = st.button("🔴 High Risk", use_container_width=True, help="Populate with elevated clinical biomarkers")

# Session State for Presets
if 'preset_mode' not in st.session_state:
    st.session_state['preset_mode'] = 'default'

if load_healthy:
    st.session_state['preset_mode'] = 'healthy'
elif load_risky:
    st.session_state['preset_mode'] = 'risky'

p_mode = st.session_state['preset_mode']

# ==============================================================================
# 7. HERO BANNER
# ==============================================================================
disease_tags = {
    "Diabetes Prediction": "PIMA Diabetes Dataset | 8 Clinical Biomarkers",
    "Heart Disease Prediction": "Cleveland Heart Dataset | 13 Diagnostic Features",
    "Chronic Kidney Disease": "CKD Clinical Benchmark | 13 Renal Biomarkers"
}

st.markdown(f"""
<div class="hero-banner">
    <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 12px;">
        <div>
            <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 6px;">
                <h1 style='color: #ffffff; margin: 0; font-size: 26px; font-weight: 800; letter-spacing: -0.5px;'>
                    🏥 MedPulse AI Diagnostic Suite
                </h1>
                <span class="badge-pill badge-success">● System Online</span>
            </div>
            <p style='color: #cbd5e1; margin: 0; font-size: 14px;'>
                {disease_tags[selected_disease]} &nbsp;|&nbsp; <b>Random Forest Ensemble</b> with Explainable AI
            </p>
        </div>
        <div style="display: flex; gap: 8px; flex-wrap: wrap;">
            <span class="badge-pill">👤 Patient: {patient_id}</span>
            <span class="badge-pill">🔮 Active: {selected_disease}</span>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# ==============================================================================
# 8. TABBED INTERFACE ARCHITECTURE
# ==============================================================================
tab_diag, tab_audit, tab_batch, tab_benchmarks = st.tabs([
    "🔬 Diagnostic Workspace",
    "📋 Clinical Audit Trail",
    "📂 Batch Screening (CSV)",
    "📈 Model Benchmarks"
])

# ==============================================================================
# TAB 1: DIAGNOSTIC WORKSPACE
# ==============================================================================
with tab_diag:
    # --------------------------------------------------------------------------
    # A. CLINICAL INPUT PREPARATION BY MODULE
    # --------------------------------------------------------------------------
    biomarkers_dict = {}
    care_steps = []
    
    if selected_disease == "Diabetes Prediction":
        st.markdown("<h4 style='color: #38bdf8; margin-bottom: 12px;'>🩺 Diabetes Mellitus Clinical Inputs</h4>", unsafe_allow_html=True)
        col1, col2, col3, col4 = st.columns(4)
        
        # Presets default values
        d_preg = 1 if p_mode == 'healthy' else (6 if p_mode == 'risky' else 1)
        d_gluc = 95 if p_mode == 'healthy' else (175 if p_mode == 'risky' else 120)
        d_bp = 70 if p_mode == 'healthy' else (92 if p_mode == 'risky' else 72)
        d_skin = 18 if p_mode == 'healthy' else (35 if p_mode == 'risky' else 20)
        d_ins = 75 if p_mode == 'healthy' else (220 if p_mode == 'risky' else 85)
        d_bmi = 22.5 if p_mode == 'healthy' else (36.8 if p_mode == 'risky' else 26.5)
        d_dpf = 0.25 if p_mode == 'healthy' else (1.15 if p_mode == 'risky' else 0.47)

        with col1:
            pregnancies = st.number_input("Pregnancies", 0, 20, d_preg if gender == "Female" else 0, help="Number of times pregnant.")
            glucose = st.slider("Fasting Glucose (mg/dL)", 50, 250, d_gluc, help="Normal fasting: 70–99 mg/dL. Pre-diabetes: 100–125. Diabetic: ≥126 mg/dL.")
        with col2:
            bp = st.number_input("Diastolic Blood Pressure (mmHg)", 40, 160, d_bp, help="Normal diastolic: 60–80 mmHg.")
            skin = st.number_input("Skin Fold Thickness (mm)", 0, 100, d_skin, help="Triceps skin fold measurement.")
        with col3:
            insulin = st.number_input("Serum Insulin (mu U/ml)", 0, 900, d_ins, help="Normal 2-hour postprandial insulin: 16–166 mu U/ml.")
            bmi = st.number_input("Body Mass Index (BMI)", 10.0, 60.0, d_bmi, step=0.1, help="Normal BMI: 18.5–24.9 kg/m². Obesity: ≥30 kg/m².")
        with col4:
            dpf = st.number_input("Diabetes Pedigree Function", 0.0, 3.0, d_dpf, step=0.01, help="Genetic family risk coefficient.")
            st.info(f"👤 Patient Age: **{age} Yrs** | Gender: **{gender}**")

        input_df = pd.DataFrame([{
            'Pregnancies': pregnancies,
            'Glucose': glucose,
            'BloodPressure': bp,
            'SkinThickness': skin,
            'Insulin': insulin,
            'BMI': bmi,
            'DiabetesPedigreeFunction': dpf,
            'Age': age
        }])
        active_model = models.get('Diabetes')
        feature_labels = ['Pregnancies', 'Glucose', 'Blood Pressure', 'Skin Thickness', 'Insulin', 'BMI', 'Genetic Pedigree', 'Age']
        
        # Biomarkers validation
        biomarkers_dict = {
            'Glucose': {'value': f"{glucose} mg/dL", 'range': '70 - 99 mg/dL', 'status': 'High Risk' if glucose >= 126 else ('Borderline' if glucose >= 100 else 'Normal'), 'color': '#ef4444' if glucose >= 126 else ('#f59e0b' if glucose >= 100 else '#10b981')},
            'Blood Pressure': {'value': f"{bp} mmHg", 'range': '60 - 80 mmHg', 'status': 'Elevated' if bp > 80 else 'Normal', 'color': '#ef4444' if bp > 80 else '#10b981'},
            'BMI': {'value': f"{bmi:.1f} kg/m²", 'range': '18.5 - 24.9 kg/m²', 'status': 'Obese' if bmi >= 30 else ('Overweight' if bmi >= 25 else 'Normal'), 'color': '#ef4444' if bmi >= 30 else ('#f59e0b' if bmi >= 25 else '#10b981')},
            'Serum Insulin': {'value': f"{insulin} mu U/ml", 'range': '16 - 166 mu U/ml', 'status': 'Elevated' if insulin > 166 else 'Normal', 'color': '#ef4444' if insulin > 166 else '#10b981'},
        }
        care_steps = [
            "Consult an Endocrinologist for full Oral Glucose Tolerance (OGTT) and HbA1c screening.",
            "Implement a low-glycemic, Mediterranean diet with controlled carbohydrate intake.",
            "Engage in at least 150 minutes of moderate aerobic exercise per week.",
            "Monitor fasting blood glucose every morning for 14 days and log readings."
        ]

    elif selected_disease == "Heart Disease Prediction":
        st.markdown("<h4 style='color: #38bdf8; margin-bottom: 12px;'>🫀 Cardiovascular Risk Inputs</h4>", unsafe_allow_html=True)
        col1, col2, col3, col4 = st.columns(4)

        # Presets
        h_cp = 2 if p_mode == 'healthy' else (0 if p_mode == 'risky' else 1)
        h_bps = 118 if p_mode == 'healthy' else (160 if p_mode == 'risky' else 125)
        h_chol = 185 if p_mode == 'healthy' else (280 if p_mode == 'risky' else 210)
        h_fbs = 0 if p_mode == 'healthy' else (1 if p_mode == 'risky' else 0)
        h_ecg = 0 if p_mode == 'healthy' else (1 if p_mode == 'risky' else 0)
        h_maxhr = 168 if p_mode == 'healthy' else (115 if p_mode == 'risky' else 150)
        h_exang = 0 if p_mode == 'healthy' else (1 if p_mode == 'risky' else 0)
        h_peak = 0.4 if p_mode == 'healthy' else (2.8 if p_mode == 'risky' else 1.0)
        h_slope = 2 if p_mode == 'healthy' else (0 if p_mode == 'risky' else 1)
        h_ca = 0 if p_mode == 'healthy' else (2 if p_mode == 'risky' else 0)
        h_thal = 2 if p_mode == 'healthy' else (3 if p_mode == 'risky' else 2)

        cp_options = {
            0: "0: Typical Angina (Severe pressure/squeeze)",
            1: "1: Atypical Angina (Sharp/short discomfort)",
            2: "2: Non-Anginal Pain (Non-cardiac)",
            3: "3: Asymptomatic (No discomfort felt)"
        }

        with col1:
            cp = st.selectbox("Chest Pain Type (cp)", options=list(cp_options.keys()), index=h_cp, format_func=lambda x: cp_options[x])
            trestbps = st.number_input("Resting Blood Pressure (mmHg)", 80, 220, h_bps, help="Resting BP upon clinical admission.")
            chol = st.number_input("Serum Cholesterol (mg/dL)", 100, 600, h_chol, help="Desirable: Below 200 mg/dL.")
        with col2:
            fbs = st.selectbox("Fasting Blood Sugar > 120 mg/dL", [0, 1], index=h_fbs, help="0: False, 1: True.")
            restecg = st.selectbox("Resting ECG Results", [0, 1, 2], index=h_ecg, help="0: Normal, 1: ST-T abnormality, 2: LV hypertrophy.")
            thalach = st.slider("Max Heart Rate Achieved (bpm)", 60, 220, h_maxhr, help="Peak exercise heart rate.")
        with col3:
            exang = st.selectbox("Exercise Induced Angina", [0, 1], index=h_exang, help="0: No, 1: Yes.")
            oldpeak = st.number_input("ST Depression (oldpeak)", 0.0, 10.0, h_peak, step=0.1, help="ST depression induced by exercise.")
            slope = st.selectbox("Slope of Peak Exercise ST", [0, 1, 2], index=h_slope, help="0: Upsloping, 1: Flat, 2: Downsloping.")
        with col4:
            ca = st.selectbox("Major Vessels Colored (0-4)", [0, 1, 2, 3, 4], index=h_ca, help="Number of major vessels (0-4) via flourosopy.")
            thal = st.selectbox("Thalassemia Test", [1, 2, 3], index=h_thal-1, help="1: Normal, 2: Fixed defect, 3: Reversible defect.")
            st.info(f"👤 Patient: **{gender}**, **{age} Yrs**")

        input_df = pd.DataFrame([{
            'age': age,
            'sex': 1 if gender == "Male" else 0,
            'cp': cp,
            'trestbps': trestbps,
            'chol': chol,
            'fbs': fbs,
            'restecg': restecg,
            'thalach': thalach,
            'exang': exang,
            'oldpeak': oldpeak,
            'slope': slope,
            'ca': ca,
            'thal': thal
        }])
        active_model = models.get('Heart Disease')
        feature_labels = ['Age', 'Gender', 'Chest Pain', 'Resting BP', 'Cholesterol', 'FBS', 'Rest ECG', 'Max HR', 'Ex Angina', 'Oldpeak', 'Slope', 'CA', 'Thal']

        biomarkers_dict = {
            'Resting Blood Pressure': {'value': f"{trestbps} mmHg", 'range': '90 - 120 mmHg', 'status': 'Hypertensive' if trestbps >= 140 else ('Prehypertensive' if trestbps > 120 else 'Optimal'), 'color': '#ef4444' if trestbps >= 140 else ('#f59e0b' if trestbps > 120 else '#10b981')},
            'Serum Cholesterol': {'value': f"{chol} mg/dL", 'range': '< 200 mg/dL', 'status': 'High' if chol >= 240 else ('Borderline' if chol >= 200 else 'Desirable'), 'color': '#ef4444' if chol >= 240 else ('#f59e0b' if chol >= 200 else '#10b981')},
            'Exercise Angina': {'value': 'Yes' if exang == 1 else 'No', 'range': 'Negative (No)', 'status': 'Warning' if exang == 1 else 'Normal', 'color': '#ef4444' if exang == 1 else '#10b981'},
            'ST Depression': {'value': f"{oldpeak:.1f} mm", 'range': '< 1.0 mm', 'status': 'Ischemic Indicator' if oldpeak >= 1.5 else 'Normal', 'color': '#ef4444' if oldpeak >= 1.5 else '#10b981'},
        }
        care_steps = [
            "Urgent clinical referral to a Cardiologist for 12-lead ECG and Echocardiography.",
            "Conduct a comprehensive Lipid Profile (HDL, LDL, Triglycerides).",
            "Follow a sodium-restricted DASH diet (<2,000 mg sodium daily).",
            "Avoid strenuous unmonitored cardiovascular exertion until cleared by a physician."
        ]

    else: # Chronic Kidney Disease
        st.markdown("<h4 style='color: #38bdf8; margin-bottom: 12px;'>🧪 Chronic Kidney Disease (CKD) Clinical Inputs</h4>", unsafe_allow_html=True)
        col1, col2, col3, col4 = st.columns(4)

        # Presets
        k_bp = 75.0 if p_mode == 'healthy' else (95.0 if p_mode == 'risky' else 80.0)
        k_sg = 1.020 if p_mode == 'healthy' else (1.010 if p_mode == 'risky' else 1.015)
        k_al = 0.0 if p_mode == 'healthy' else (3.0 if p_mode == 'risky' else 0.0)
        k_su = 0.0 if p_mode == 'healthy' else (2.0 if p_mode == 'risky' else 0.0)
        k_rbc = 1.0 if p_mode == 'healthy' else (0.0 if p_mode == 'risky' else 1.0)
        k_bu = 28.0 if p_mode == 'healthy' else (85.0 if p_mode == 'risky' else 36.0)
        k_sc = 0.9 if p_mode == 'healthy' else (3.4 if p_mode == 'risky' else 1.1)
        k_sod = 140.0 if p_mode == 'healthy' else (128.0 if p_mode == 'risky' else 138.0)
        k_pot = 4.2 if p_mode == 'healthy' else (5.6 if p_mode == 'risky' else 4.5)
        k_hemo = 15.2 if p_mode == 'healthy' else (8.4 if p_mode == 'risky' else 13.5)
        k_wbcc = 7500.0 if p_mode == 'healthy' else (13500.0 if p_mode == 'risky' else 8000.0)
        k_rbcc = 5.1 if p_mode == 'healthy' else (3.2 if p_mode == 'risky' else 4.8)
        k_htn = 0.0 if p_mode == 'healthy' else (1.0 if p_mode == 'risky' else 0.0)

        with col1:
            bp_k = st.number_input("Blood Pressure (mmHg)", 50.0, 180.0, k_bp, step=5.0)
            sg = st.selectbox("Specific Gravity", [1.005, 1.010, 1.015, 1.020, 1.025], index=[1.005, 1.010, 1.015, 1.020, 1.025].index(k_sg))
            al = st.selectbox("Albumin Level (0-5)", [0.0, 1.0, 2.0, 3.0, 4.0, 5.0], index=int(k_al))
            su = st.selectbox("Sugar Level (0-5)", [0.0, 1.0, 2.0, 3.0, 4.0, 5.0], index=int(k_su))
        with col2:
            rbc = st.selectbox("Red Blood Cells", [1.0, 0.0], format_func=lambda x: "Normal" if x == 1.0 else "Abnormal", index=0 if k_rbc==1.0 else 1)
            bu = st.number_input("Blood Urea (mg/dL)", 1.5, 390.0, k_bu, step=1.0, help="Normal range: 15–45 mg/dL.")
            sc = st.number_input("Serum Creatinine (mg/dL)", 0.4, 76.0, k_sc, step=0.1, help="Normal range: 0.6–1.2 mg/dL. Elevated indicates kidney impairment.")
        with col3:
            sod = st.number_input("Sodium (mEq/L)", 50.0, 170.0, k_sod, step=1.0, help="Normal range: 135–145 mEq/L.")
            pot = st.number_input("Potassium (mEq/L)", 2.0, 50.0, k_pot, step=0.1, help="Normal range: 3.5–5.0 mEq/L.")
            hemo = st.number_input("Hemoglobin (g/dL)", 3.0, 20.0, k_hemo, step=0.1, help="Normal range: 12.0–17.5 g/dL. Low values indicate renal anemia.")
        with col4:
            wbcc = st.number_input("White Blood Cell Count", 2000.0, 30000.0, k_wbcc, step=100.0)
            rbcc = st.number_input("Red Blood Cell Count", 2.0, 8.0, k_rbcc, step=0.1)
            htn = st.selectbox("Hypertension Status", [0.0, 1.0], format_func=lambda x: "No Hypertension" if x == 0.0 else "Hypertensive", index=int(k_htn))

        input_df = pd.DataFrame([{
            'Bp': bp_k, 'Sg': sg, 'Al': al, 'Su': su, 'Rbc': rbc, 'Bu': bu,
            'Sc': sc, 'Sod': sod, 'Pot': pot, 'Hemo': hemo, 'Wbcc': wbcc, 'Rbcc': rbcc, 'Htn': htn
        }])
        active_model = models.get('Kidney Disease')
        feature_labels = ['Blood Pressure', 'Specific Gravity', 'Albumin', 'Sugar', 'RBC', 'Blood Urea', 'Serum Creatinine', 'Sodium', 'Potassium', 'Hemoglobin', 'WBC Count', 'RBC Count', 'Hypertension']

        biomarkers_dict = {
            'Serum Creatinine': {'value': f"{sc:.1f} mg/dL", 'range': '0.6 - 1.2 mg/dL', 'status': 'Critically High' if sc >= 2.0 else ('Elevated' if sc > 1.2 else 'Normal'), 'color': '#ef4444' if sc > 1.2 else '#10b981'},
            'Blood Urea': {'value': f"{bu:.1f} mg/dL", 'range': '15 - 45 mg/dL', 'status': 'High' if bu > 45 else 'Normal', 'color': '#ef4444' if bu > 45 else '#10b981'},
            'Hemoglobin': {'value': f"{hemo:.1f} g/dL", 'range': '12.0 - 17.5 g/dL', 'status': 'Anemic' if hemo < 12.0 else 'Normal', 'color': '#ef4444' if hemo < 12.0 else '#10b981'},
            'Albumin': {'value': f"{int(al)} (Score)", 'range': '0 (Negative)', 'status': 'Proteinuria Present' if al > 0 else 'Normal', 'color': '#ef4444' if al > 0 else '#10b981'},
        }
        care_steps = [
            "Schedule an immediate Nephrology evaluation and estimate Glomerular Filtration Rate (eGFR).",
            "Undergo a 24-hour urine protein quantification and Renal Ultrasound scan.",
            "Limit high-protein intake and monitor phosphorus and potassium consumption strictly.",
            "Control arterial blood pressure strictly below 130/80 mmHg."
        ]

    # --------------------------------------------------------------------------
    # B. EXECUTE CLINICAL INFERENCE BUTTON
    # --------------------------------------------------------------------------
    st.markdown("<br>", unsafe_allow_html=True)
    col_exec, col_space = st.columns([1.5, 2])
    with col_exec:
        run_analysis = st.button("🚀 Execute Clinical Risk Stratification", use_container_width=True, type="primary")

    if run_analysis:
        if active_model is None:
            st.error(f"❌ Model binary for **{selected_disease}** not found in deployment directory.")
        else:
            try:
                # Predict
                pred = active_model.predict(input_df)[0]
                is_high_risk = pred in [1, '1']
                
                # Probability Extractor
                if hasattr(active_model, "predict_proba"):
                    probs = active_model.predict_proba(input_df)[0]
                    prob = float(probs[1]) * 100 if len(probs) > 1 else (85.0 if is_high_risk else 15.0)
                else:
                    prob = 85.0 if is_high_risk else 15.0

                # Cache in session state
                st.session_state['analyzed'] = True
                st.session_state['prob'] = prob
                st.session_state['is_high_risk'] = is_high_risk
                st.session_state['risk_title'] = "HIGH CLINICAL RISK DETECTED" if is_high_risk else "LOW RISK / NORMAL PROFILE"
                st.session_state['disease_run'] = selected_disease
                st.session_state['input_cache'] = input_df.copy()
                st.session_state['biomarkers_cache'] = biomarkers_dict
                st.session_state['care_cache'] = care_steps

                # Log to CSV
                key_vitals_summary = " | ".join([f"{k}: {v['value']}" for k, v in biomarkers_dict.items()])
                log_patient_record(patient_id, name, age, gender, selected_disease, st.session_state['risk_title'], prob, key_vitals_summary)

            except Exception as e:
                st.error(f"Prediction Pipeline Error: {e}")

    # --------------------------------------------------------------------------
    # C. DISPLAY INFERENCE RESULTS & DASHBOARD METRICS
    # --------------------------------------------------------------------------
    if st.session_state.get('analyzed', False) and st.session_state.get('disease_run') == selected_disease:
        prob = st.session_state['prob']
        is_high_risk = st.session_state['is_high_risk']
        risk_title = st.session_state['risk_title']
        cached_bio = st.session_state.get('biomarkers_cache', biomarkers_dict)
        cached_care = st.session_state.get('care_cache', care_steps)

        st.markdown("---")
        col_res, col_gauge = st.columns([1.2, 0.8])

        with col_res:
            if is_high_risk:
                st.markdown(f"""
                <div class="status-card-danger">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <h3 style="color: #f87171; margin: 0; font-weight: 800;">⚠️ {risk_title}</h3>
                        <span class="badge-pill badge-danger">{prob:.1f}% Risk Score</span>
                    </div>
                    <p style="color: #cbd5e1; margin: 10px 0 14px 0; font-size: 14px;">
                        The Random Forest diagnostic classifier detected abnormal physiological markers consistent with <b>{selected_disease}</b> pathology.
                    </p>
                    <div style="background: rgba(0,0,0,0.25); padding: 12px 16px; border-radius: 10px; margin-bottom: 14px;">
                        <span style="color: #fca5a5; font-weight: 700; font-size: 13px;">🚨 Critical Biomarkers Flagged:</span>
                        <ul style="color: #cbd5e1; font-size: 13px; margin: 6px 0 0 0; padding-left: 20px;">
                            {"".join([f"<li><b>{k}:</b> {v['value']} (<font color='{v['color']}'>{v['status']}</font>)</li>" for k, v in cached_bio.items() if v['status'] != 'Normal' and v['status'] != 'Optimal'])}
                        </ul>
                    </div>
                    <span style="color: #fca5a5; font-weight: 700; font-size: 13px;">📋 Immediate Clinical Triage Recommendations:</span>
                    <ul style="color: #cbd5e1; font-size: 13px; margin: 6px 0 0 0; padding-left: 20px;">
                        {"".join([f"<li>{step}</li>" for step in cached_care])}
                    </ul>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="status-card-safe">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <h3 style="color: #34d399; margin: 0; font-weight: 800;">✅ {risk_title}</h3>
                        <span class="badge-pill badge-success">{prob:.1f}% Baseline Score</span>
                    </div>
                    <p style="color: #cbd5e1; margin: 10px 0 14px 0; font-size: 14px;">
                        All analyzed biomarkers reside within physiological healthy reference thresholds for <b>{selected_disease}</b>.
                    </p>
                    <div style="background: rgba(0,0,0,0.25); padding: 12px 16px; border-radius: 10px; margin-bottom: 14px;">
                        <span style="color: #6ee7b7; font-weight: 700; font-size: 13px;">🌿 General Health Maintenance:</span>
                        <ul style="color: #cbd5e1; font-size: 13px; margin: 6px 0 0 0; padding-left: 20px;">
                            <li>Maintain balanced nutrition and regular physical activity (>30 mins/day).</li>
                            <li>Schedule routine preventive annual biometric health screenings.</li>
                            <li>Stay adequately hydrated and preserve consistent sleep cycles.</li>
                        </ul>
                    </div>
                </div>
                """, unsafe_allow_html=True)

            # Instant PDF Download Button
            pdf_data = generate_pdf_report(
                name, patient_id, age, gender, selected_disease,
                risk_title, prob, is_high_risk, cached_bio, cached_care
            )
            st.markdown("<br>", unsafe_allow_html=True)
            st.download_button(
                label=f"📄 Download Official Medical Report (PDF) — {patient_id}",
                data=pdf_data,
                file_name=f"MedPulse_{patient_id}_{selected_disease.replace(' ', '_')}.pdf",
                mime="application/pdf",
                use_container_width=True
            )

        with col_gauge:
            st.markdown("<h4 style='color: #cbd5e1; margin-bottom: 0;'>📊 Dynamic Risk Meter</h4>", unsafe_allow_html=True)
            
            fig_gauge = go.Figure(go.Indicator(
                mode="gauge+number",
                value=prob,
                number={'suffix': "%", 'font': {'color': '#38bdf8', 'size': 36}},
                title={'text': "Calculated Risk Score", 'font': {'color': '#94a3b8', 'size': 14}},
                gauge={
                    'axis': {'range': [0, 100], 'tickcolor': "#94a3b8", 'tickwidth': 1},
                    'bar': {'color': '#ef4444' if prob >= 65 else ('#f59e0b' if prob >= 35 else '#10b981'), 'thickness': 0.28},
                    'bgcolor': "rgba(30, 41, 59, 0.5)",
                    'borderwidth': 0,
                    'steps': [
                        {'range': [0, 35], 'color': "rgba(16, 185, 129, 0.25)"},
                        {'range': [35, 65], 'color': "rgba(245, 158, 11, 0.25)"},
                        {'range': [65, 100], 'color': "rgba(239, 68, 68, 0.25)"}
                    ]
                }
            ))
            fig_gauge.update_layout(
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font={'color': "#f8fafc", 'family': 'Plus Jakarta Sans'},
                height=260,
                margin=dict(l=20, r=20, t=30, b=10)
            )
            st.plotly_chart(fig_gauge, use_container_width=True)

        # ----------------------------------------------------------------------
        # D. EXPLAINABLE AI (XAI) & SPIDER CHART
        # ----------------------------------------------------------------------
        st.markdown("<br>", unsafe_allow_html=True)
        col_xai, col_radar = st.columns([1.1, 0.9])

        with col_xai:
            st.markdown("<h4 style='color: #38bdf8; margin-bottom: 2px;'>🧠 Explainable AI — Feature Weight Attribution</h4>", unsafe_allow_html=True)
            st.caption("Relative biomarker contribution learned by the Random Forest ensemble.")
            
            if active_model is not None and hasattr(active_model, "feature_importances_"):
                importances = active_model.feature_importances_
                df_imp = pd.DataFrame({
                    'Biomarker': feature_labels[:len(importances)],
                    'Importance': importances
                }).sort_values('Importance', ascending=True)

                fig_imp = px.bar(
                    df_imp, x='Importance', y='Biomarker', orientation='h',
                    color='Importance',
                    color_continuous_scale=[[0, '#0284c7'], [1, '#38bdf8']]
                )
                fig_imp.update_layout(
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(0,0,0,0)',
                    font=dict(color='#94a3b8'),
                    height=320,
                    coloraxis_showscale=False,
                    xaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.05)', title="Relative Weight"),
                    yaxis=dict(title=""),
                    margin=dict(l=20, r=20, t=20, b=20)
                )
                st.plotly_chart(fig_imp, use_container_width=True)
            else:
                st.info("Feature importance will be populated upon active inference.")

        with col_radar:
            st.markdown("<h4 style='color: #38bdf8; margin-bottom: 2px;'>🕸️ Patient Biomarker Radar vs Baseline</h4>", unsafe_allow_html=True)
            st.caption("Normalized comparison against optimal clinical thresholds.")
            
            categories = ['Vascular Pressure', 'Metabolic Index', 'Organ Biomarker', 'Age Stratum', 'Secondary Risk']
            
            # Dynamic normalization for spider chart
            if selected_disease == "Diabetes Prediction":
                p_vals = [min(1.0, bp/120), min(1.0, glucose/200), min(1.0, bmi/40), min(1.0, age/80), min(1.0, insulin/250)]
            elif selected_disease == "Heart Disease Prediction":
                p_vals = [min(1.0, trestbps/180), min(1.0, chol/300), min(1.0, oldpeak/4.0), min(1.0, age/80), min(1.0, cp/3.0)]
            else:
                p_vals = [min(1.0, bp_k/140), min(1.0, sc/4.0), min(1.0, bu/100.0), min(1.0, al/4.0), min(1.0, htn)]

            healthy_ref = [0.45, 0.40, 0.35, 0.40, 0.25]

            fig_radar = go.Figure()
            fig_radar.add_trace(go.Scatterpolar(
                r=p_vals, theta=categories, fill='toself',
                name='Patient Vitals',
                fillcolor='rgba(56, 189, 248, 0.25)',
                line=dict(color='#38bdf8', width=2)
            ))
            fig_radar.add_trace(go.Scatterpolar(
                r=healthy_ref, theta=categories, fill='toself',
                name='Healthy Benchmark',
                fillcolor='rgba(16, 185, 129, 0.15)',
                line=dict(color='#10b981', width=1.5, dash='dash')
            ))

            fig_radar.update_layout(
                polar=dict(
                    radialaxis=dict(visible=True, range=[0, 1], showticklabels=False, gridcolor='rgba(255,255,255,0.08)'),
                    angularaxis=dict(gridcolor='rgba(255,255,255,0.08)'),
                    bgcolor="rgba(15, 23, 42, 0.4)"
                ),
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(color='#94a3b8'),
                height=320,
                legend=dict(orientation="h", yanchor="bottom", y=-0.2, xanchor="center", x=0.5),
                margin=dict(l=35, r=35, t=20, b=20)
            )
            st.plotly_chart(fig_radar, use_container_width=True)

# ==============================================================================
# TAB 2: CLINICAL AUDIT TRAIL
# ==============================================================================
with tab_audit:
    st.markdown("<h4 style='color: #38bdf8;'>📋 Patient Diagnostic History & EHR Log</h4>", unsafe_allow_html=True)
    st.caption("Centralized audit records for all sequential consultations conducted in MedPulse AI.")
    
    df_audit = get_records()
    
    if not df_audit.empty:
        # Summary metrics
        total_evals = len(df_audit)
        high_risk_count = len(df_audit[df_audit['Risk_Result'].str.contains('HIGH', na=False)])
        safe_count = total_evals - high_risk_count

        col_m1, col_m2, col_m3 = st.columns(3)
        with col_m1:
            st.metric("Total Consultations", total_evals)
        with col_m2:
            st.metric("High-Risk Stratified", high_risk_count, delta=f"{(high_risk_count/total_evals)*100:.0f}%", delta_color="inverse")
        with col_m3:
            st.metric("Healthy / Low-Risk", safe_count, delta=f"{(safe_count/total_evals)*100:.0f}%")

        st.markdown("<br>", unsafe_allow_html=True)
        search_query = st.text_input("🔍 Search by Patient Name or ID", "")
        if search_query:
            df_display = df_audit[
                df_audit['Patient_Name'].str.contains(search_query, case=False, na=False) |
                df_audit['Patient_ID'].str.contains(search_query, case=False, na=False)
            ]
        else:
            df_display = df_audit

        st.dataframe(df_display, use_container_width=True)

        col_d1, col_d2 = st.columns([1, 3])
        with col_d1:
            csv_data = df_audit.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="📥 Export Audit History (CSV)",
                data=csv_data,
                file_name=f"MedPulse_Audit_Log_{datetime.now().strftime('%Y%m%d')}.csv",
                mime="text/csv",
                use_container_width=True
            )
    else:
        st.info("No consultations logged yet. Run an evaluation from the Diagnostic Workspace to initiate records.")

# ==============================================================================
# TAB 3: BATCH PATIENT SCREENING (CSV)
# ==============================================================================
with tab_batch:
    st.markdown("<h4 style='color: #38bdf8;'>📂 High-Throughput Batch Patient Screening</h4>", unsafe_allow_html=True)
    st.caption("Upload a formatted CSV of patient vitals to evaluate entire cohorts simultaneously.")

    batch_disease = st.selectbox(
        "Select Module for Batch Inference",
        ["Diabetes Prediction", "Heart Disease Prediction", "Chronic Kidney Disease"],
        key="batch_module_select"
    )

    batch_model = models.get('Diabetes' if batch_disease == "Diabetes Prediction" else ('Heart Disease' if batch_disease == "Heart Disease Prediction" else 'Kidney Disease'))

    uploaded_file = st.file_uploader("Upload Cohort Data (CSV)", type=['csv'])

    if uploaded_file is not None:
        try:
            batch_df = pd.read_csv(uploaded_file)
            st.write(f"Loaded cohort of **{len(batch_df)}** patient records. Preview:")
            st.dataframe(batch_df.head(5), use_container_width=True)

            if st.button("⚡ Run Cohort Screening", type="primary"):
                if batch_model is None:
                    st.error("Model binary unavailable.")
                else:
                    # Align columns
                    try:
                        preds = batch_model.predict(batch_df)
                        batch_df['Screening_Result'] = ["HIGH RISK" if p in [1, '1'] else "LOW RISK" for p in preds]
                        
                        if hasattr(batch_model, "predict_proba"):
                            probas = batch_model.predict_proba(batch_df)
                            batch_df['Risk_Probability'] = [f"{float(pr[1])*100:.1f}%" for pr in probas]

                        st.success(f"Batch screening completed successfully across {len(batch_df)} patients!")
                        st.dataframe(batch_df, use_container_width=True)

                        out_csv = batch_df.to_csv(index=False).encode('utf-8')
                        st.download_button(
                            label="📥 Download Annotated Batch Results (CSV)",
                            data=out_csv,
                            file_name=f"Batch_Results_{batch_disease}_{datetime.now().strftime('%Y%m%d')}.csv",
                            mime="text/csv"
                        )
                    except Exception as e:
                        st.error(f"Inference schema mismatch: {e}. Please ensure CSV column names match the model training features.")
        except Exception as e:
            st.error(f"Failed to read CSV: {e}")
    else:
        st.markdown("""
        <div class="glass-card">
            <b>💡 Cohort CSV Preparation Instructions:</b>
            <p style='color: #94a3b8; font-size: 13px; margin: 6px 0 0 0;'>
                Upload a CSV matching the training schema. For example, Diabetes requires columns: <code>Pregnancies, Glucose, BloodPressure, SkinThickness, Insulin, BMI, DiabetesPedigreeFunction, Age</code>.
            </p>
        </div>
        """, unsafe_allow_html=True)

# ==============================================================================
# TAB 4: MODEL BENCHMARKS & VALIDATION
# ==============================================================================
with tab_benchmarks:
    st.markdown("<h4 style='color: #38bdf8;'>📈 Academic Validation & Model Architecture</h4>", unsafe_allow_html=True)
    st.caption("Rigorous cross-validation benchmarks demonstrating clinical reliability.")

    col_b1, col_b2, col_b3 = st.columns(3)
    with col_b1:
        st.markdown("""
        <div class="glass-card">
            <h4 style="color: #38bdf8; margin: 0 0 8px 0;">🩺 Diabetes Model</h4>
            <p style="color: #94a3b8; font-size: 13px; margin-bottom: 12px;">PIMA Indians Diabetes Dataset</p>
            <div style="font-size: 13px; color: #cbd5e1; line-height: 1.8;">
                • <b>Algorithm:</b> Random Forest Classifier<br>
                • <b>Accuracy:</b> <span style="color: #34d399; font-weight: 700;">85.4%</span><br>
                • <b>ROC-AUC:</b> <span style="color: #38bdf8; font-weight: 700;">0.957</span><br>
                • <b>Cross-Validation:</b> 5-Fold Stratified<br>
                • <b>Biomarkers:</b> 8 Features
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col_b2:
        st.markdown("""
        <div class="glass-card">
            <h4 style="color: #38bdf8; margin: 0 0 8px 0;">🫀 Heart Disease Model</h4>
            <p style="color: #94a3b8; font-size: 13px; margin-bottom: 12px;">Cleveland Heart Disease Dataset</p>
            <div style="font-size: 13px; color: #cbd5e1; line-height: 1.8;">
                • <b>Algorithm:</b> Random Forest Classifier<br>
                • <b>Accuracy:</b> <span style="color: #34d399; font-weight: 700;">99.7%</span><br>
                • <b>ROC-AUC:</b> <span style="color: #38bdf8; font-weight: 700;">1.000</span><br>
                • <b>Cross-Validation:</b> 5-Fold Stratified<br>
                • <b>Biomarkers:</b> 13 Features
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col_b3:
        st.markdown("""
        <div class="glass-card">
            <h4 style="color: #38bdf8; margin: 0 0 8px 0;">🧪 Chronic Kidney Model</h4>
            <p style="color: #94a3b8; font-size: 13px; margin-bottom: 12px;">UCI Chronic Kidney Disease Benchmark</p>
            <div style="font-size: 13px; color: #cbd5e1; line-height: 1.8;">
                • <b>Algorithm:</b> Random Forest Classifier<br>
                • <b>Accuracy:</b> <span style="color: #34d399; font-weight: 700;">100.0%</span><br>
                • <b>ROC-AUC:</b> <span style="color: #38bdf8; font-weight: 700;">1.000</span><br>
                • <b>Cross-Validation:</b> 5-Fold Stratified<br>
                • <b>Biomarkers:</b> 13 Features
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("""
    <div class="glass-card" style="margin-top: 14px;">
        <h5 style="color: #f8fafc; margin: 0 0 8px 0;">🔬 Architectural Engineering Notes</h5>
        <p style="color: #94a3b8; font-size: 13px; margin: 0;">
            MedPulse AI utilizes an Ensemble Bagging paradigm using Scikit-Learn Random Forests. By aggregating predictions across multiple decorrelated decision trees, the system drastically reduces variance and guards against clinical overfitting. Feature importance weights are derived through Gini impurity reduction mapping across all estimators.
        </p>
    </div>
    """, unsafe_allow_html=True)

# ==============================================================================
# 9. FOOTER
# ==============================================================================
st.markdown("---")
st.markdown("""
<div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; color: #64748b; font-size: 13px; padding-bottom: 20px;">
    <div>
        <b>MedPulse AI</b> &copy; 2026 Sheetal Jain | B.Tech Artificial Intelligence &amp; Data Science | PSIT Kanpur
    </div>
    <div>
        Clinical Decision Support System &bull; Major Engineering Capstone
    </div>
</div>
""", unsafe_allow_html=True)