import os
import joblib
import numpy as np
import logging
import traceback
from flask import Flask, request, jsonify, render_template

# ---------------------------------------
# LOGGING CONFIGURATION
# ---------------------------------------
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger(__name__)

app = Flask(__name__, template_folder="templates", static_folder="static")

# ----------------------------
# MODEL LOADING
# ----------------------------
# 18-feature Model
MODEL_PATH = "model_fixed.pkl"

model = None

try:
    if os.path.exists(MODEL_PATH):
        logger.info(f"Loading model from {MODEL_PATH}...")
        model = joblib.load(MODEL_PATH)
        logger.info("Model loaded successfully!")
    else:
        # Fallback to verify logic even if file missing specific path
        logger.error(f"Model file {MODEL_PATH} not found!")
except Exception as e:
    logger.error(f"Failed to load model: {e}")
    logger.error(traceback.format_exc())

# ---------------------------------------
# Feature Configuration (9 Features)
# ---------------------------------------
# EXACT ORDER from model.feature_names_in_
MODEL_FEATURES = [
    'Weight', 'Height', 'Green_Vegetables', 'General_Health',
    'Fruit', 'Fried_Potato', 'BMI', 'Age', 'Alcohol'
]

SCALERS = {
    'Weight': {'min': 30, 'max': 150},
    'Height': {'min': 120, 'max': 220},
    'BMI': {'min': 15, 'max': 50},
    'Age': {'min': 18, 'max': 80},
    'Fruit': {'min': 0, 'max': 30},
    'Green_Vegetables': {'min': 0, 'max': 30},
    'Fried_Potato': {'min': 0, 'max': 30},
    'Alcohol': {'min': 0, 'max': 30},
    'General_Health': {
        'Poor': 0.0, 'Fair': 0.25, 'Good': 0.5, 'Very_Good': 0.75, 'Excellent': 1.0
    }
}

def process_input_value(value, feature_name):
    """
    Normalizes input values based on the scalers configuration.
    Features are scaled to 0-1 range.
    """
    if feature_name in SCALERS:
        config = SCALERS[feature_name]

        # Numeric Range Scaling
        if isinstance(config, dict) and 'min' in config:
            try:
                val = float(value)
                # Clip to min/max before scaling? Or just raw scaling?
                # The previous code did: (val - min) / (max - min)
                norm_val = (val - config['min']) / (config['max'] - config['min'])
                return max(0.0, min(1.0, norm_val)) # Build-in clip to 0-1
            except:
                return 0.0

        # Categorical Mapping
        elif isinstance(config, dict):
            return config.get(str(value), 0.0)

    try:
        return float(value)
    except:
        return 0.0

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/calculate")
def calculate():
    return render_template("calculate.html")

@app.route("/recommendation/<int:level>")
def recommendation(level):
    return render_template("recommendation.html", level=level)

@app.route("/predict", methods=["POST"])
def predict():
    try:
        if not model:
            return jsonify({"error": "Model not loaded"}), 500

        data = request.json
        logger.info(f"Received Prediction Request: {data}")

        input_vector = []
        
        for feature in MODEL_FEATURES:
            raw_val = data.get(feature)
            processed_val = process_input_value(raw_val, feature)
            input_vector.append(processed_val)

        logger.info(f"Input Vector: {input_vector}")

        # Reshape for prediction
        input_array = [input_vector]
        
        # Predict
        prediction_prob = model.predict_proba(input_array)[0][1]
        prediction_class = int(model.predict(input_array)[0])
        
        logger.info(f"Result: Class={prediction_class}, Prob={prediction_prob:.4f}")

        # Map probability to risk level 1-5
        if prediction_prob <= 0.2:
            risk_level = 1
        elif prediction_prob <= 0.4:
            risk_level = 2
        elif prediction_prob <= 0.6:
            risk_level = 3
        elif prediction_prob <= 0.8:
            risk_level = 4
        else:
            risk_level = 5

        return jsonify({
            "probability": float(prediction_prob),
            "class": prediction_class,
            "risk_level": risk_level
        })

    except Exception as e:
        logger.error(f"Prediction Error: {e}")
        return jsonify({"error": str(e)}), 500

@app.route("/test", methods=["GET"])
def test_model():
    """Automated health check"""
    # ... (Keep existing simple test structure updated for 18 feats if needed)
    return jsonify({"status": "running"})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 7860))
    app.run(host="0.0.0.0", port=port)