"""
check_disease_names.py -- Phase 2: sewb l check dyal diseases (l'ewel
mra dert comparaison case-sensitive b ghalat -- "allergy" != "Allergy"
walakin nafss disease, script li fat ma kanich knormalizi ism dyal
disease b7al li kanit kandir m3a symptomes).

Khddemha mn root dyal medai/ (mora ma dert process_symptom2disease.py):
    python check_disease_names.py
"""

import pandas as pd
from pathlib import Path

PROCESSED = Path("data/processed")
RAW = Path("data/raw")

s2d = pd.read_csv(RAW / "Symptom2Disease.csv").drop(columns=["Unnamed: 0"])
s2d["label"] = s2d["label"].str.strip()

disease_symptoms = pd.read_csv(PROCESSED / "disease_symptoms_long.csv")

known_norm = {d.lower(): d for d in disease_symptoms["Disease"]}
s2d_norm = {d.lower(): d for d in s2d["label"].unique()}

casing_matches = sorted(set(s2d_norm) & set(known_norm))
truly_new = sorted(set(s2d_norm) - set(known_norm))

print(f"Correspondances b ghi casse mokhtalfa ({len(casing_matches)}):")
for norm in casing_matches:
    print(f"  '{s2d_norm[norm]}'  <->  '{known_norm[norm]}'")

print(f"\nJdad b jed, 0 correspondance hta b casse ({len(truly_new)}):")
for norm in truly_new:
    print(f"  '{s2d_norm[norm]}'")
