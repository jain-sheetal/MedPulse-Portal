 🏥 MedPulse AI — Clinical Decision Support System

> A machine learning-powered web application for early disease risk prediction, clinical explainability (XAI), and interactive biomarker analysis.

---

## 📌 Overview

**MedPulse AI** is an end-to-end Clinical Decision Support System (CDSS) built as a B.Tech Final Year Engineering Project. The platform assists users and healthcare practitioners by evaluating risk probabilities for **Diabetes** and **Cardiovascular Diseases** using trained machine learning models.

Unlike black-box AI tools, MedPulse AI emphasizes **Explainable AI (XAI)** by providing feature importance rankings, interactive Plotly risk meters, and biomarker spider charts comparing user metrics against healthy reference ranges.

---

## ✨ Key Features

* **Dual Diagnostic Engine:**
  * **Diabetes Diagnostic Module:** Predicts risk based on glucose, BMI, insulin, age, and genetic pedigree indicators.
  * **Heart Disease Diagnostic Module:** Evaluates cardiovascular risk factors including chest pain classification, resting blood pressure, cholesterol, and ST depression.
* **Explainable AI (XAI):** Visual feature importance bar charts breaking down exactly which clinical variables contributed to the model's prediction.
* **Interactive Data Visualizations:**
  * Synchronized Plotly risk gauge meters showing real-time probability scores.
  * Spider/Radar charts evaluating patient vitals against normal healthy baseline thresholds.
* **Patient-Centric Interface:**
  * Plain-English descriptions for complex clinical inputs (e.g., chest pain types).
  * Actionable lifestyle guidance and next steps based on risk stratification outcomes.
* **Modern UI:** Built with Streamlit and styled using custom glassmorphic CSS in dark mode.

---

## 🛠️ Tech Stack & Dependencies

* **Language:** Python 3.10+
* **Frontend/Framework:** [Streamlit](https://streamlit.io/)
* **Machine Learning:** `scikit-learn` (Random Forest Classifier), `numpy`, `pandas`
* **Data Visualization:** `plotly`, `plotly-express`
* **Model Serialization:** `pickle`

---

## 📁 Repository Structure

```text
AI_HEALTH_PROJECT/
│
├── app.py                  # Main Streamlit application script
├── diabetes_model.pkl      # Pre-trained Random Forest model for Diabetes
├── heart_model.pkl         # Pre-trained Random Forest model for Heart Disease
├── requirements.txt        # Python package dependencies
└── README.md               # Project documentation
