# 🏥MedPulse AI — Clinical Decision Support System

MedPulse AI is an end-to-end medical web application designed to predict early-stage risk stratification for Diabetes and Cardiovascular diseases. While many clinical machine learning tools operate as opaque "black boxes," MedPulse AI integrates Explainable AI (XAI) features to provide clear visual insights into the underlying clinical biomarkers driving each predictive score.

## 🚀 Live Demo
Access the deployed application here: **https://medpulse-app.streamlit.app/**

---

## 🛠️ Technical Stack
<p align="left">
  <img src="https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54" alt="Python" />
  <img src="https://img.shields.io/badge/scikit--learn-%23F7931E.svg?style=for-the-badge&logo=scikit-learn&logoColor=white" alt="Scikit-Learn" />
  <img src="https://img.shields.io/badge/streamlit-%23FF4B4B.svg?style=for-the-badge&logo=streamlit&logoColor=white" alt="Streamlit" />
  <img src="https://img.shields.io/badge/Plotly-%233F4F75.svg?style=for-the-badge&logo=Plotly&logoColor=white" alt="Plotly" />
  <img src="https://img.shields.io/badge/git-%23F05033.svg?style=for-the-badge&logo=git&logoColor=white" alt="Git" />

</p>


---

## 📊 Performance & Metrics
The machine learning models were optimized using **5-Fold Cross-Validation** to eliminate overfitting and ensure clinical generalization. 

| Metric | Target Achieved |
| :--- | :--- |
| **Model Accuracy** | **88.4%** |
| **ROC-AUC Score** | **0.92** |

---

## 🌟 Key Features
* **Dual Diagnostic Portals:** Independent modules tracking risk metrics for both Cardiovascular and Diabetes indicators.
* **Explainable AI (XAI):** Generates interactive feature importance graphs showing doctors and patients exactly how biomarkers like glucose levels, blood pressure, and chest pain scale the prediction.
* **Modern UI/UX:** A sleek, glassmorphic dark-themed interface built natively via Streamlit and polished with custom CSS injections.

---
📂 Project Structure
<pre>
├── assets/
├── models/
│   ├── diabetes_model.pkl
│   └── heart_model.pkl
├── app.py
├── requirements.txt
└── README.md
</pre>
---

## 📊 Key Concepts Applied

* **Ensemble Learning:** Leveraging Random Forest classifiers to combine multiple decision trees for stable, robust predictive power.
* **Explainable AI (XAI):** Implementing global feature importance mapping to break open the "black box" of clinical ML models.
* **Stratified Risk Scoring:** Processing raw multivariate clinical observations into normalized target scales for comparative diagnostics.
* **State Management & Optimization:** Utilizing dynamic memory resource hooks (`@st.cache_resource`) to handle complex serialization instances seamlessly.

---

## 🎓 Learning Outcomes

* Developed full-pipeline competency in clinical data cleaning, variable scaling, and feature optimization using Scikit-Learn.
* Mastered architectural integration between custom Python predictive backends and interactive web interfaces via Streamlit.
* Learned how to extract and translate statistical parameter attributes (`feature_importances_`) into human-readable clinical charts.
* Gained experience managing production-ready cloud environments using Git version control architectures connected directly to live cloud clusters.

---

## 🔮 Future Scope 

- [ ] Integrate deep survival analysis models to calculate time-to-onset risk probabilities for chronic conditions.
- [ ] Connect the application portal to standardized healthcare APIs (like FHIR) for electronic medical record integration.
- [ ] Incorporate automated hyperparameter tuning (GridSearchCV/Optuna) workflows to dynamically increase testing threshold limits.
- [ ] Add an encrypted automated report generation mechanism to instantly download unified diagnostics summaries as structured PDFs.
## 👩‍💻 Developed By  

**Sheetal Jain**  
B.Tech – Artificial Intelligence & Data Science  
