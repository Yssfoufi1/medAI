"""
fix_missing_symptom.py -- Phase 2, ta2akkod + sewb l symptome li ban
unmatched (Section 7 step 9, "verifier les incoherences").

Machi ghi n-hardcodi valeur mkheمmna: njibo l forme raw exacte mn
dataset.csv b nafsha, w nzidoha l symptom_translations.csv b symptom_id
jdid ila mkanتش already.

Khddemha mn root dyal medai/ (mora ma dert reshape_dataset.py):
    python fix_missing_symptom.py
Mnbad 3awd python reshape_dataset.py bach disease_symptoms_long.csv
ykon kaml (l disease li fiha had symptome ghadi tzid l symptom_id
li jdid f la liste dyalha).
"""

import pandas as pd
from pathlib import Path

RAW = Path("data/raw")
PROCESSED = Path("data/processed")

symptom_translations = pd.read_csv(PROCESSED / "symptom_translations.csv")

# 1. ta2akkod: wach kayn chi entree 9riba (urine/smell) already f la table
near = symptom_translations[
    symptom_translations["normalized_expression"].str.contains("urine|smell", case=False, na=False)
]
print("Entrees 9rab (urine/smell) deja f la table:")
print(near[["symptom_id", "normalized_expression"]].to_string(index=False) if len(near) else "  (walo)")

# 2. njibo l forme RAW exacte mn dataset.csv (bla ma nkhemmnoha)
dataset = pd.read_csv(RAW / "dataset.csv")
symptom_cols = [c for c in dataset.columns if c.startswith("Symptom_")]
raw_values = pd.melt(dataset, value_vars=symptom_cols, value_name="symptom_raw")["symptom_raw"].dropna()

target_norm = "foul smell of urine"
raw_match = raw_values[raw_values.str.strip().str.lower().str.replace("_", " ", regex=False) == target_norm]
raw_form = raw_match.iloc[0] if len(raw_match) else target_norm
print(f"\nvaleur raw dyalha f dataset.csv: '{raw_form}'  ({len(raw_match)} occurrence(s))")

# 3. zid f la table canonique ila mazal ghayba
if target_norm not in symptom_translations["normalized_expression"].values:
    new_id = f"S{len(symptom_translations) + 1:03d}"
    new_row = pd.DataFrame([{
        "symptom_id": new_id,
        "canonical_name": target_norm,
        "language": "en",
        "expression": raw_form,
        "normalized_expression": target_norm,
        "source": "dataset.csv (Kaggle, itachi9604) -- ghayba mn Symptom-severity.csv, zidat manuellement",
    }])
    symptom_translations = pd.concat([symptom_translations, new_row], ignore_index=True)
    symptom_translations.to_csv(PROCESSED / "symptom_translations.csv", index=False)
    print(f"\nzdna {new_id} l la table (daba {len(symptom_translations)} symptomes).")
else:
    print("\nkayna already, walo matbeddel.")
