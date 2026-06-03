---
title: Crime Forecaster
emoji: 🔍
colorFrom: indigo
colorTo: blue
sdk: docker
app_port: 7860
pinned: false
license: mit
short_description: AI-powered crime type prediction using Chicago crime data
---

# 🔍 Crime Forecaster — AI-Powered Crime Type Prediction

[![Hugging Face Spaces](https://img.shields.io/badge/Live%20Demo-%F0%9F%A4%97%20Hugging%20Face%20Space-blue?style=for-the-badge)](https://huggingface.co/spaces/Hamzasajjad38/Crime-Forecaster)
[![Kaggle Notebook](https://img.shields.io/badge/Notebook-Kaggle-20BEFF?style=for-the-badge&logo=kaggle)](https://www.kaggle.com/code/hamzasajjad321/ml-dl-chicago-crime-type-prediction)

A machine learning web application that predicts the most likely **type of crime** based on location, time, and situational factors — trained on **7+ million** real crime records from the City of Chicago (2001–2017).

![Python](https://img.shields.io/badge/Python-3.12-blue?logo=python)
![Flask](https://img.shields.io/badge/Flask-3.0-black?logo=flask)
![scikit-learn](https://img.shields.io/badge/scikit--learn-1.6-orange?logo=scikit-learn)
![TensorFlow](https://img.shields.io/badge/TensorFlow-2.x-ff6f00?logo=tensorflow)

---

## 🎯 What It Does

Enter situational details like **latitude/longitude**, **date & time**, **district**, and **location type** — and the model predicts which crime type is most likely to occur under those conditions.

**Example predictions:** Theft, Battery, Criminal Damage, Narcotics, Assault, Burglary, and more.

---

## 🧠 Models & Accuracy

| Model | Accuracy | Precision | Recall | F1-Score |
|---|---|---|---|---|
| Random Forest | 99.7% | 99.7% | 99.7% | 99.7% |
| MLP Neural Network | 98.9% | 98.9% | 98.9% | 98.9% |
| K-Nearest Neighbors | 72.0% | 71.0% | 72.0% | 71.0% |
| **Voting Ensemble (Deployed)** | **99.7%** | **99.7%** | **99.7%** | **99.7%** |
| LSTM (Time-Series) | 69.0% | 51.0% | 71.0% | 59.0% |

The deployed model is a **Voting Ensemble** combining Random Forest, MLP, and KNN via hard voting.

---

## 📁 Dataset

- **Source:** [Crimes in Chicago — Kaggle](https://www.kaggle.com/datasets/currie32/crimes-in-chicago)
- **Size:** ~7.9 million records across 23 columns
- **Time Span:** 2001–2017
- **Target Variable:** `Primary Type` (crime category)

---

## 📓 Kaggle Notebook

The complete training notebook with EDA, preprocessing, model training, and evaluation is available on Kaggle:

🔗 **[ML & DL Chicago Crime Type Prediction — Kaggle](https://www.kaggle.com/code/hamzasajjad321/ml-dl-chicago-crime-type-prediction)**

---

## 🛠️ Tech Stack

| Category | Tools |
|---|---|
| Backend | Python, Flask |
| ML Models | scikit-learn (Random Forest, MLP, KNN, VotingClassifier) |
| Deep Learning | TensorFlow / Keras (LSTM) |
| Frontend | HTML, CSS, Bootstrap 5, Leaflet.js |
| Deployment | Docker, Gunicorn, Hugging Face Spaces |

---

## 📂 Project Structure

```
├── app.py                  # Flask application
├── Dockerfile              # Docker config for HF Spaces
├── requirements.txt        # Python dependencies
├── models/                 # Trained model & preprocessing artifacts
│   ├── crime_model_v2.pkl
│   ├── feature_encoders_v2.pkl
│   ├── feature_columns_v2.pkl
│   ├── scaler_v2.pkl
│   ├── target_encoder_v2.pkl
│   └── district_options.pkl
├── templates/              # HTML templates (Jinja2)
│   ├── layout.html
│   ├── index.html
│   ├── predictor.html
│   ├── dataset.html
│   ├── model-tech.html
│   ├── about.html
│   └── team.html
└── static/
    ├── css/style.css
    └── images/             # EDA charts, model diagrams, team photos
```

---

## 🚀 Run Locally

```bash
# Clone the repo
git clone https://huggingface.co/spaces/YOUR_USERNAME/crime-forecaster
cd crime-forecaster

# Install dependencies
pip install -r requirements.txt

# Run the app
python app.py
```

Then open **http://127.0.0.1:5000** in your browser.

---

## 📜 License

This project is licensed under the MIT License.
