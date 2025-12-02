import os
import joblib
import numpy as np
import pandas as pd
from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

# Load the model
MODEL_PATH = 'Meta-MLP_Base-GB-AdaB-XGB-RF_reduced.pkl'
try:
    model = joblib.load(MODEL_PATH)
    print(f"Model loaded successfully from {MODEL_PATH}")
except Exception as e:
    print(f"Error loading model: {e}")
    model = None

# Feature configuration
# The model expects these 9 features in this order:
MODEL_FEATURES = ['Weight', 'Height', 'Green_Vegetables', 'General_Health', 'Fruit', 
                  'Fried_Potato', 'BMI', 'Age', 'Alcohol']

# Assumed Min/Max for normalization (based on typical health data ranges)
# We map User Input -> [0, 1]
SCALERS = {
    'Weight': {'min': 30, 'max': 150}, # kg
    'Height': {'min': 120, 'max': 220}, # cm
    'BMI': {'min': 15, 'max': 50},
    'Age': {'min': 18, 'max': 80},
    'Fruit': {'min': 0, 'max': 30}, # servings/month
    'Green_Vegetables': {'min': 0, 'max': 30},
    'Fried_Potato': {'min': 0, 'max': 30},
    'Alcohol': {'min': 0, 'max': 30},
    # Categorical/Ordinal mappings (User Input Value -> Normalized Value)
    'General_Health': {
        'Poor': 0.0, 'Fair': 0.25, 'Good': 0.5, 'Very_Good': 0.75, 'Excellent': 1.0
    },
    'Checkup': {
        'Never': 0.0, '5+ years': 0.25, '2-5 years': 0.5, '1-2 years': 0.75, 'Within 1 year': 1.0
    },
    'Diabetes': {
        'No': 0.0, 'Borderline': 0.33, 'During Pregnancy': 0.66, 'Yes': 1.0
    },
    # Binary features are already 0 or 1
}

def normalize(value, feature_name):
    if feature_name in SCALERS:
        config = SCALERS[feature_name]
        if isinstance(config, dict) and 'min' in config:
            # Numerical scaling
            try:
                val = float(value)
                return (val - config['min']) / (config['max'] - config['min'])
            except:
                return 0.0
        elif isinstance(config, dict):
            # Categorical mapping
            return config.get(value, 0.0)
    
    # Default for binary or unknown
    try:
        return float(value)
    except:
        return 0.0

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    if not model:
        return jsonify({'error': 'Model not loaded'}), 500

    data = request.json
    print("Received data:", data)

    # Prepare input vector for the model (9 features)
    input_vector = []
    for feature in MODEL_FEATURES:
        raw_val = data.get(feature)
        norm_val = normalize(raw_val, feature)
        # Clamp values between 0 and 1 just in case
        norm_val = max(0.0, min(1.0, norm_val))
        input_vector.append(norm_val)
    
    print("Input vector:", input_vector)

    try:
        # Predict
        prediction_prob = model.predict_proba([input_vector])[0][1] # Probability of Class 1 (Disease)
        prediction_class = int(model.predict([input_vector])[0])
        
        return jsonify({
            'probability': float(prediction_prob),
            'class': prediction_class,
            'risk_level': 'High' if prediction_prob > 0.5 else 'Low'
        })
    except Exception as e:
        print(f"Prediction error: {e}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
