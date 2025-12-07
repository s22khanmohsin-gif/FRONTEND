"""
Re-save the model with compatible package versions for Hugging Face deployment.

This script fixes the MT19937 BitGenerator incompatibility by re-serializing
the model using numpy 1.23.5 and joblib 1.2.0.
"""

import joblib
import warnings

warnings.filterwarnings('ignore')

print("=" * 60)
print("MODEL RE-SERIALIZATION SCRIPT")
print("=" * 60)

# Check installed versions
print("\nChecking package versions...")
try:
    import numpy
    import sklearn
    import xgboost
    print(f"NumPy: {numpy.__version__}")
    print(f"scikit-learn: {sklearn.__version__}")
    print(f"XGBoost: {xgboost.__version__}")
    print(f"Joblib: {joblib.__version__}")
except ImportError as e:
    print(f"Missing package: {e}")
    print("\nPlease install required packages:")
    print("   pip install numpy==1.23.5 joblib==1.2.0 scikit-learn==1.6.1 xgboost==1.7.5")
    exit(1)

# Load original model
print("\nLoading original model...")
try:
    model = joblib.load("model_pruned_float16.pkl")
    print("Model loaded successfully!")
except Exception as e:
    print(f"Failed to load model: {e}")
    print("\nMake sure 'model_pruned_float16.pkl' is in the current directory")
    exit(1)

# Save with compatible environment
print("\nRe-saving model with compatible packages...")
try:
    joblib.dump(model, "model_fixed.pkl", compress=('zlib', 3))
    print("Model saved as 'model_fixed.pkl'")
except Exception as e:
    print(f"Failed to save model: {e}")
    exit(1)

# Verify the new model loads correctly
print("\nVerifying new model file...")
try:
    test_model = joblib.load("model_fixed.pkl")
    print("New model loads successfully!")
    
    # Check if it's the same type
    print(f"Model type: {type(test_model).__name__}")
    
except Exception as e:
    print(f"Verification failed: {e}")
    exit(1)

print("\n" + "=" * 60)
print("SUCCESS! Model re-serialization complete.")
print("=" * 60)
print("\nNext steps:")
print("1. Upload 'model_fixed.pkl' to your Hugging Face Space")
print("2. Update app.py to use 'model_fixed.pkl' instead of 'model_pruned_float16.pkl'")
print("3. Rebuild your Space")
print("\nYour model will then load successfully!")
