# KROK 0 — IMPORTY

import pandas as pd
import numpy as np
import os
from google.colab import files

# KROK 1 — WGRANIE PLIKU

uploaded = files.upload()
file_name = list(uploaded.keys())[0]

os.makedirs("results", exist_ok=True)

print(f"Processing file: {file_name}")

# KROK 2 — WCZYTANIE DANYCH

if file_name.endswith(".csv"):
    df = pd.read_csv(file_name)
elif file_name.endswith(".xlsx"):
    df = pd.read_excel(file_name)
else:
    raise ValueError("Unsupported file format. Use CSV or XLSX.")

# KROK 3 — WYBÓR KOLUMN NUMERYCZNYCH

numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()

if len(numeric_cols) < 2:
    raise ValueError("At least 2 numeric columns are required.")

# KROK 4 — BASELINE (MEDIANA + IQR)

baseline = {}
for col in numeric_cols:
    q1 = df[col].quantile(0.25)
    q3 = df[col].quantile(0.75)
    iqr = q3 - q1
    median = df[col].median()

    baseline[col] = {
        "median": median,
        "iqr": iqr if iqr != 0 else 1  # zabezpieczenie
    }

# KROK 5 — RISK SCORE

def calculate_risk_score(row):
    scores = []

    for col in numeric_cols:
        deviation = abs(row[col] - baseline[col]["median"]) / baseline[col]["iqr"]
        scores.append(deviation)

    avg_deviation = np.mean(scores)

    # Skalowanie do 0–100
    risk_score = min(100, avg_deviation * 25)
    return round(risk_score, 1)

df["risk_score"] = df.apply(calculate_risk_score, axis=1)

# KROK 6 — DECYZJA

def decision_label(score):
    if score >= 70:
        return "HIGH RISK"
    elif score >= 40:
        return "MEDIUM RISK"
    else:
        return "LOW RISK"

df["decision"] = df["risk_score"].apply(decision_label)

# KROK 7 — POWÓD (REASON)

def build_reason(row):
    reasons = []

    for col in numeric_cols:
        deviation = abs(row[col] - baseline[col]["median"]) / baseline[col]["iqr"]
        if deviation > 2:
            reasons.append(f"{col} significantly above normal range")

    if not reasons:
        return "Within expected operational range"

    return "; ".join(reasons)

df["reason"] = df.apply(build_reason, axis=1)

# KROK 8 — ZAPIS WYNIKU

output_file = f"results/decision_output_{file_name}"
df.to_excel(output_file, index=False)

print("Processing completed.")
print(f"Result saved to: {output_file}")

# PODGLĄD NAJWAŻNIEJSZYCH REKORDÓW

df.sort_values("risk_score", ascending=False).head(10)
