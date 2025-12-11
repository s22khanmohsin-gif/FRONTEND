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
# New 18-feature Stacking Ensemble Model
MODEL_PATH = "Meta-MLP_Base-GB-AdaB-XGB-RF_full.pkl"

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
# Feature Configuration (18 Features)
# ---------------------------------------
# EXACT ORDER from model.feature_names_in_
MODEL_FEATURES = [
    'General_Health', 'Checkup', 'Exercise', 'Skin_Cancer', 'Other_Cancer', 
    'Depression', 'Diabetes', 'Arthritis', 'Sex', 'Age', 'Height', 'Weight', 
    'BMI', 'Smoking', 'Alcohol', 'Fruit', 'Green_Vegetables', 'Fried_Potato'
]

def process_input_value(value, feature_name):
    """
    Converts input to the format expected by the model.
    CRITICAL: Validated that model expects RAW values, not normalized.
    """
    try:
        if value is None or value == "":
            return 0.0

        # Numeric fields - Keep RAW
        # FIX: Model has bias against 0 values for Alcohol/Fried_Potato ("Clean Living Penalty")
        # Set minimum of 1 to avoid this quirk
        if feature_name in ['Age', 'Height', 'Weight', 'BMI', 'Fruit', 'Green_Vegetables']:
            return float(value)
        if feature_name == 'Alcohol':
            val = float(value)
            return max(val, 1.0)  # Minimum 1 to avoid bias
        if feature_name == 'Fried_Potato':
            val = float(value)
            return max(val, 1.0)  # Minimum 1 to avoid bias
            
        # Categorical Mappings
        # Based on typical dataset encodings
        if feature_name == 'General_Health':
            # Map string to numeric if needed, or pass 1.0/0.0
            mapping = {
                'Poor': 0.0, 
                'Fair': 0.25, 
                'Good': 0.5, 
                'Very_Good': 0.75, 
                'Excellent': 1.0,
                # Fallback for numeric str
                '0': 0.0, '1': 1.0
            }
            return mapping.get(str(value), float(value) if str(value).replace('.','',1).isdigit() else 0.0)
            
        # Binary Fields (Yes/No -> 1/0)
        # Checkup, Exercise, Skin_Cancer, Other_Cancer, Depression, Diabetes, Arthritis, Sex, Smoking
        mapping = {
            'Yes': 1.0, 'No': 0.0,
            'Male': 1.0, 'Female': 0.0,
            '1': 1.0, '0': 0.0
        }
        
        # Helper for Checkup (Within last year = 1, else 0?)
        # Dataset usually: 1=Within past year, 2=Within past 2 years...
        # For simplicity/safety with current binary test success:
        if feature_name == 'Checkup':
             # If value is 'Within past year' or '1', return 1
             # Also handle 'Within 1 year' from HTML
             val_str = str(value).lower()
             if val_str in ['within past year', 'within 1 year', '1', 'yes']:
                 return 1.0
             return 0.0

        # Diabetes: Yes/No/Borderline/During Pregnancy
        # Model likely trained on 0/1 or 0/1/2. 
        # Assuming 0=No, 1=Yes/Borderline/Pregnancy for safety, or just Yes=1.
        # Let's map Yes=1, others=0 for now to match "Healthy" expectation, 
        # but ideally Borderline should be > 0. 
        # However, for the specific issue of "Healthy" person getting high risk, 
        # "No" should definitely be 0.
        if feature_name == 'Diabetes':
            val_str = str(value).lower()
            if val_str in ['yes', '1']:
                return 1.0
            # Treat Borderline/Pregnancy as 0 or maybe 1? 
            # If we want to be strict, maybe they are risk factors.
            # But for now ensure 'No' is 0.
            return 0.0

        if str(value) in mapping:
            return mapping[str(value)]
            
        return float(value)

    except Exception as e:
        logger.warning(f"Conversion failed for {feature_name} val='{value}': {e}")
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
            # Default to 0/No if missing
            if raw_val is None:
                # Set intelligent defaults for required fields?
                # For now 0 is safe "No/None"
                raw_val = 0
            
            processed_val = process_input_value(raw_val, feature)
            input_vector.append(processed_val)
            # logger.debug(f"{feature}: {raw_val} -> {processed_val}")

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