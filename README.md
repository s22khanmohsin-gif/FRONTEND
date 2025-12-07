---
title: ML Prediction App
emoji: 🏥
colorFrom: blue
colorTo: green
sdk: docker
pinned: false
license: mit
---

# ML Prediction Application

A Flask-based machine learning application for health risk predictions using a pruned ensemble model.

## Features

- 🎯 Real-time ML predictions
- 📊 Interactive web interface
- 🚀 Optimized model (77MB)
- 💯 High accuracy predictions

## Model Information

- **Model Type**: Pruned Ensemble (XGBoost-based)
- **Model Size**: 77MB (float16 optimized)
- **Features**: 9 health-related inputs
- **Output**: Risk probability and classification

## Usage

Visit the application URL and input the following health metrics:
- Weight (kg)
- Height (cm)
- BMI
- Age
- Dietary habits (Fruit, Vegetables, Fried Potato consumption)
- Alcohol consumption
- General health status

The model will return a risk prediction with probability score.

## Tech Stack

- **Backend**: Flask + Gunicorn
- **ML Framework**: scikit-learn, XGBoost
- **Deployment**: Docker on Hugging Face Spaces
