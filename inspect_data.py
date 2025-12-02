import pandas as pd
import pickle
import os

csv_path = 'CVD_preprocessed.csv'
pkl_path = 'Meta-MLP_Base-GB-AdaB-XGB-RF_reduced.pkl'

print(f"--- Inspecting {csv_path} ---")
try:
    df = pd.read_csv(csv_path, nrows=2)
    print("Columns:", df.columns.tolist())
    print("Number of columns:", len(df.columns))
except Exception as e:
    print(f"Error reading CSV: {e}")

import joblib

print(f"\n--- Inspecting {pkl_path} ---")
try:
    model = joblib.load(pkl_path)
    print("Model type:", type(model))
    if hasattr(model, 'n_features_in_'):
        print("n_features_in_:", model.n_features_in_)
    if hasattr(model, 'feature_names_in_'):
        print("feature_names_in_:", model.feature_names_in_)
except Exception as e:
    print(f"Error reading PKL with joblib: {e}")
