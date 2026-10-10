# 🏥 MedPulse AI — Multi-Disease Clinical Decision Support Suite

[![Live Demo](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://medpulse-app.streamlit.app/)
[![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python&logoColor=white)](https://python.org)
[![Scikit-Learn](https://img.shields.io/badge/Scikit--Learn-F7931E?logo=scikit-learn&logoColor=white)](https://scikit-learn.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?logo=streamlit&logoColor=white)](https://streamlit.io)
[![Plotly](https://img.shields.io/badge/Plotly-3F4F75?logo=plotly&logoColor=white)](https://plotly.com)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)

**MedPulse AI** is an enterprise-grade, clinical decision support system (CDSS) built to provide early-stage risk stratification for **Diabetes Mellitus**, **Cardiovascular Disease**, and **Chronic Kidney Disease (CKD)**. While many medical machine learning models operate as opaque "black boxes," MedPulse AI incorporates **Explainable AI (XAI)** architectures, dynamic biometric risk meters, automated clinical PDF report generation, and full Electronic Health Record (EHR) audit trails.

---

## 🚀 Live Cloud Deployment
Access the live web application on Streamlit Cloud:  
👉 **[https://medpulse-app.streamlit.app/](https://medpulse-app.streamlit.app/)**

---

## 🛠️ Technology Stack
<p align="left">
  <img src="https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54" alt="Python" />
  <img src="https://img.shields.io/badge/scikit--learn-%23F7931E.svg?style=for-the-badge&logo=scikit-learn&logoColor=white" alt="Scikit-Learn" />
  <img src="https://img.shields.io/badge/streamlit-%23FF4B4B.svg?style=for-the-badge&logo=streamlit&logoColor=white" alt="Streamlit" />
  <img src="https://img.shields.io/badge/Plotly-%233F4F75.svg?style=for-the-badge&logo=Plotly&logoColor=white" alt="Plotly" />
  <img src="https://img.shields.io/badge/pandas-%23150458.svg?style=for-the-badge&logo=pandas&logoColor=white" alt="Pandas" />
  <img src="https://img.shields.io/badge/numpy-%23013243.svg?style=for-the-badge&logo=numpy&logoColor=white" alt="NumPy" />
  <img src="https://img.shields.io/badge/git-%23F05033.svg?style=for-the-badge&logo=git&logoColor=white" alt="Git" />
</p>

---

## 🌟 Key Architecture & Capabilities

### 1. 🔬 Tri-Disease Diagnostic Portals
* **🩺 Diabetes Mellitus Screening:** Evaluates 8 key clinical biomarkers (Fasting Glucose, Diastolic BP, BMI, 2-Hour Serum Insulin, Skin Thickness, Genetic Pedigree Function, Pregnancies, and Age).
* **🫀 Cardiovascular Risk Stratification:** Analyzes 13 cardiac factors including Chest Pain presentation (Angina types), Resting Blood Pressure, Serum Cholesterol, Fasting Blood Sugar, Exercise-induced Angina, ST Depression (Oldpeak), Resting ECG, Peak Heart Rate, and Fluoroscopy Vessels.
* **🧪 Chronic Kidney Disease (CKD) Early Detection:** Evaluates 13 renal vitals (Blood Urea, Serum Creatinine, Albuminuria, Urine Specific Gravity, Hemoglobin, RBC/WBC counts, Blood Pressure, and Hypertension status).

### 2. 🧠 Explainable AI (XAI) Suite
* **Feature Weight Attribution:** Real-time horizontal bar charts exposing the Gini importance of individual biomarkers calculated by the Random Forest ensemble.
* **Biomarker Radar / Spider Maps:** Multi-axis radial comparison displaying the patient's physiological metrics directly mapped against normal clinical reference standards.
* **Dynamic Medical Risk Gauges:** Real-time risk probability meters with calibrated green (<35%), yellow (35–65%), and red (>65%) safety zones.

### 3. 📄 Automated Clinical PDF Reports
* Generates downloadable, clinical evaluation PDF summaries in-memory via ReportLab.
* Contains full patient demographics, structured biomarker breakdown, risk category, model confidence score, actionable doctor recommendations, and clinical legal disclaimers.

### 4. 📋 EHR Audit Trail & History
* Persistent logging to `patient_records.csv`.
* Real-time search, patient filtering, summary risk stats, and one-click full historical CSV export.

### 5. 📂 High-Throughput Batch Cohort Screening
* Enables uploading patient cohort CSV files to perform bulk automated inference and export annotated risk sheets.

### 6. ⚡ Smart Clinical Quick-Fill Presets
* One-click presets for **"🟢 Healthy / Normal Baseline"** and **"🔴 High Risk Clinical Profile"** allowing evaluators and clinicians to immediately test risk transitions.

---

## 📊 Model Benchmarks & Validation

The machine learning backends are trained using **Ensemble Random Forest Classifiers** optimized with **5-Fold Stratified Cross-Validation**:

| Disease Module | Benchmark Dataset | Clinical Features | Accuracy | ROC-AUC |
| :--- | :--- | :--- | :--- | :--- |
| **Diabetes Mellitus** | PIMA Indians Diabetes Dataset | 8 Biomarkers | **85.4%** | **0.957** |
| **Cardiovascular Disease** | Cleveland Heart Disease Dataset | 13 Diagnostic Features | **99.7%** | **1.000** |
| **Chronic Kidney Disease** | UCI Chronic Kidney Disease | 13 Renal Parameters | **100.0%** | **1.000** |

---

## 📂 Project Structure

```
├── .github/
│   └── workflows/
│       └── keep_alive.yml         # GitHub Actions cron to keep Streamlit awake
├── .streamlit/
│   └── config.toml                # Premium dark glassmorphism theme tokens
├── app.py                         # Main Streamlit Clinical Decision Support Suite
├── streamlit_app.py               # Streamlit entrypoint wrapper
├── wake_app.py                    # Automated keep-alive headless ping script
├── diabetes_model.pkl             # Trained Random Forest model (Diabetes)
├── heart_model.pkl                # Trained Random Forest model (Heart Disease)
├── kidney_model.pkl               # Trained Random Forest model (Chronic Kidney Disease)
├── diabetes.csv.xls               # Reference training dataset (Diabetes)
├── heart.csv                      # Reference training dataset (Heart)
├── kidney.csv                     # Reference training dataset (Kidney)
├── patient_records.csv            # Centralized EHR audit trail log
├── AI_Health_Prediction.ipynb     # Model training and exploratory analysis notebook
├── requirements.txt               # Production Python dependencies
├── .gitignore                     # Repository hygiene configuration
└── README.md                      # Comprehensive project documentation
```

---

## 💻 Local Installation & Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/jain-sheetal/MedPulse-Portal.git
   cd MedPulse-Portal
   ```

2. **Create and activate a virtual environment:**
   ```bash
   python -m venv venv
   # On Windows:
   venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Launch the MedPulse AI portal:**
   ```bash
   streamlit run app.py
   ```

The application will launch in your browser at `http://localhost:8501`.

---

## 👩‍💻 Developed By

**Sheetal Jain**  
*B.Tech in Artificial Intelligence & Data Science (2023–2027)*  
Pranveer Singh Institute of Technology (PSIT), Kanpur  

[![LinkedIn](https://img.shields.io/badge/LinkedIn-0077B5?style=flat-square&logo=linkedin&logoColor=white)](https://linkedin.com/in/sheetal-jain-1604sj)
[![GitHub](https://img.shields.io/badge/GitHub-181717?style=flat-square&logo=github&logoColor=white)](https://github.com/jain-sheetal)
[![LeetCode](https://img.shields.io/badge/LeetCode-FFA116?style=flat-square&logo=LeetCode&logoColor=black)](https://leetcode.com/u/sheetal-jain)
[![Email](https://img.shields.io/badge/Email-D14836?style=flat-square&logo=gmail&logoColor=white)](mailto:jainsheetal.sj16@gmail.com)

---

## ⚖️ Legal & Medical Disclaimer
*MedPulse AI is developed as an academic and engineering clinical decision support system. It is designed to assist preliminary risk stratification and cannot substitute certified clinical laboratory diagnostics or direct consultation with licensed healthcare practitioners.*
