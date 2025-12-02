import pandas as pd

csv_path = 'CVD_preprocessed.csv'
try:
    df = pd.read_csv(csv_path)
    features_of_interest = ['Weight', 'Height', 'Green_Vegetables', 'General_Health', 'Fruit', 'Fried_Potato', 'BMI', 'Age', 'Alcohol']
    
    print("--- Unique values for model features ---")
    for col in features_of_interest:
        if col in df.columns:
            print(f"\n{col}:")
            print(df[col].unique()[:20]) # Show first 20 unique values
            print(f"Type: {df[col].dtype}")
        else:
            print(f"\n{col} NOT FOUND in CSV")

    print("\n--- First 5 rows of all columns ---")
    print(df.head())

except Exception as e:
    print(f"Error: {e}")
