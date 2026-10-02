"""
fix_typo.py -- Phase 2: sewb l typo f S091 ("ofurine" bla espace, source
file nafso) w msah S133 (dupliqué li zad b ghalat script li fat).

Khddemha mn root dyal medai/ (mora ma dert fix_missing_symptom.py):
    python fix_typo.py
Mnbad 3awd: python reshape_dataset.py
"""

import pandas as pd
from pathlib import Path

PROCESSED = Path("data/processed")
path = PROCESSED / "symptom_translations.csv"
symptom_translations = pd.read_csv(path)

# 1. sewb l typo f S091 (source file fiha "ofurine" bla espace)
symptom_translations.loc[
    symptom_translations["symptom_id"] == "S091",
    ["canonical_name", "normalized_expression"],
] = "foul smell of urine"

# 2. msah S133 (dupliqué li zad b ghalat, 7it kanet already S091)
symptom_translations = symptom_translations[symptom_translations["symptom_id"] != "S133"]

# 3. check systematique: chkoun kayb9a identique ila 7yedna les espaces
#    (nafss pattern li dar l mochkil -- momken kayn chi wahed akhor)
check = symptom_translations.copy()
check["no_space"] = check["normalized_expression"].str.replace(" ", "", regex=False)
dupes = check[check.duplicated("no_space", keep=False)].sort_values("no_space")

symptom_translations.to_csv(path, index=False)
print(f"sewbna S091, msahna S133 -- daba {len(symptom_translations)} symptomes.")
print(f"\nchi doublon akhor b nafss pattern (espace)? {'LA -- walo' if dupes.empty else ''}")
if not dupes.empty:
    print(dupes[["symptom_id", "normalized_expression"]].to_string(index=False))
