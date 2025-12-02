import pandas as pd

csv_path = 'CVD_preprocessed.csv'
try:
    df = pd.read_csv(csv_path)
    
    print("--- Feature Statistics ---")
    for col in df.columns:
        unique_vals = sorted(df[col].unique())
        if len(unique_vals) < 20:
            print(f"\n{col} (Categorical/Ordinal?):")
            print(unique_vals)
        else:
            print(f"\n{col} (Numerical?):")
            print(f"Min: {df[col].min()}, Max: {df[col].max()}")
            # print(f"Sample values: {unique_vals[:5]} ... {unique_vals[-5:]}")

except Exception as e:
    print(f"Error: {e}")
