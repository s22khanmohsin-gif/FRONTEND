import os
import joblib
import numpy as np
import logging
import traceback
from flask import Flask, request, jsonify, render_template

# ---------------------------------------
# LOGGING CONFIGURATION
# ---------------------------------------
# This ensures logs appear in Gunicorn/Hugging Face console
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
MODEL_PATH = "/var/data/model_fixed.pkl"
LOCAL_MODEL_PATH = "model_fixed.pkl"

model = None

try:
    if os.path.exists(MODEL_PATH):
        logger.info(f"Loading model from {MODEL_PATH}...")
        model = joblib.load(MODEL_PATH)
    elif os.path.exists(LOCAL_MODEL_PATH):
        logger.info(f"Loading model from {LOCAL_MODEL_PATH}...")
        model = joblib.load(LOCAL_MODEL_PATH)
    elif os.path.exists("model_pruned_float16.pkl"):
        # Fallback to original if fixed doesn't exist
        logger.warning("Fixed model not found, attempting to load original model...")
        model = joblib.load("model_pruned_float16.pkl")
    else:
        logger.error("Model file not found!")
    
    if model:
        logger.info("Model loaded successfully!")
except Exception as e:
    logger.error(f"Failed to load model: {e}")
    logger.error(traceback.format_exc())

# ---------------------------------------
# Feature Configuration
# ---------------------------------------
# NOTE: These MUST match exactly what the model was trained on.
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

def normalize(value, feature_name):
    """Safely converts and normalizes input values."""
    try:
        if feature_name in SCALERS:
            config = SCALERS[feature_name]

            # Handle Min-Max Scaling (numeric inputs)
            if isinstance(config, dict) and 'min' in config:
                if value is None or value == "":
                    return 0.0
                val = float(value)
                return (val - config['min']) / (config['max'] - config['min'])

            # Handle Categorical Mapping (string inputs)
            elif isinstance(config, dict):
                # Ensure value matches key perfectly, default to 0.0
                return config.get(str(value), 0.0)

        # Default fallback for unconfigured features
        if value is None or value == "":
            return 0.0
        return float(value)
        
    except Exception as e:
        logger.warning(f"Normalization failed for {feature_name} with value '{value}': {e}")
        return 0.0

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/predict", methods=["POST"])
def predict():
    try:
        if not model:
            logger.error("Attempted prediction but model is not loaded.")
            return jsonify({"error": "Model not loaded service side"}), 500

        data = request.json
        logger.info(f"Received Prediction Request. Data keys: {list(data.keys())}")
        logger.debug(f"Full Data: {data}")

        input_vector = []
        
        # Build input vector in exact order
        for feature in MODEL_FEATURES:
            raw_val = data.get(feature)
            norm_val = normalize(raw_val, feature)
            
            # Clamp value between 0 and 1
            norm_val = max(0.0, min(1.0, norm_val))
            
            input_vector.append(norm_val)
            logger.debug(f"Feature '{feature}': Raw='{raw_val}' -> Norm={norm_val:.4f}")

        logger.info(f"Final Input Vector (Length {len(input_vector)}): {input_vector}")

        # --- MODEL PREDICTION ---
        # Reshape to 2D array: (1, n_features)
        input_array = [input_vector]
        
        try:
            # Predict probability
            prediction_prob = model.predict_proba(input_array)[0][1]
            # Predict class
            prediction_class = int(model.predict(input_array)[0])
            
            logger.info(f"Prediction Success: Class={prediction_class}, Prob={prediction_prob:.4f}")

            return jsonify({
                "probability": float(prediction_prob),
                "class": prediction_class,
                "risk_level": "High" if prediction_prob > 0.5 else "Low"
            })

        except ValueError as ve:
            logger.error(f"Shape/Value Error during prediction: {ve}")
            # This often happens if feature count mismatch
            logger.error(f"Expected model features vs provided vector length mismatch?")
            raise ve

    except Exception as e:
        logger.exception("CRITICAL ERROR IN /PREDICT ENDPOINT")
        return jsonify({
            "error": "Internal Server Error", 
            "message": str(e),
            "traceback": traceback.format_exc()
        }), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 7860))
    app.run(host="0.0.0.0", port=port)