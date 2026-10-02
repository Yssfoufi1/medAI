"""
build_symptom_table.py -- Phase 2, 1ere brique: table symptom_translations
(Section 8 dyal cahier) mbeniya 3la Symptom-severity.csv (133 symptomes EN).

Hadi ghadya tkon l "colonne vertebrale" (symptom_id) li ghadi ykhedmo 3liha
kolchi: reshape dyal dataset.csv, ajout Darija/FR mnbad.

Khddemha mn root dyal medai/:
    python build_symptom_table.py
"""

import pandas as pd
from pathlib import Path

RAW = Path("data/raw")
PROCESSED = Path("data/processed")
PROCESSED.mkdir(parents=True, exist_ok=True)

severity = pd.read_csv(RAW / "Symptom-severity.csv")
n_before = len(severity)

# normalisation: underscore -> space, lowercase, espaces zayda -- Section 7 step 6
severity["normalized_expression"] = (
    severity["Symptom"]
    .str.strip()
    .str.lower()
    .str.replace("_", " ", regex=False)
    .str.replace(r"\s+", " ", regex=True)
)

# dedup 3la la version normalisee (deux ecritures dyal nafss symptome
# khassehom ynqedro f nafss symptom_id) -- Section 7 step 3
severity = severity.drop_duplicates(subset="normalized_expression").reset_index(drop=True)
n_after = len(severity)

# symptom_id canonique -- Section 7 step 7 (S001, S002...)
severity["symptom_id"] = [f"S{str(i + 1).zfill(3)}" for i in range(len(severity))]

# table symptom_translations (Section 8): 1 ligne = 1 (symptom_id, langue)
# daba ghi EN -- Darija/FR ghadi yzido s-safs 3la nafss symptom_id mnbad
symptom_translations = pd.DataFrame({
    "symptom_id": severity["symptom_id"],
    "canonical_name": severity["normalized_expression"],
    "language": "en",
    "expression": severity["Symptom"],
    "normalized_expression": severity["normalized_expression"],
    "source": "Symptom-severity.csv (Kaggle, itachi9604)",
})

out_path = PROCESSED / "symptom_translations.csv"
symptom_translations.to_csv(out_path, index=False)

print(f"n avant dedup: {n_before}, n mora: {n_after}  ({n_before - n_after} doublon(s) msso7)")
print(f"saved -> {out_path}  shape={symptom_translations.shape}")
print()
print(symptom_translations.head(15))
