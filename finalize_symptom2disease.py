"""
finalize_symptom2disease.py -- Phase 2: ysed khدmة Symptom2Disease.

1. Ywaحد l'ecriture dyal 21 disease li kانو ghi b casse mختلفة (ex.
   "allergy" -> "Allergy") 3la l forme li kaynة f les 41 "officiels".
2. Ykhrej l 3 diseases li b jed jdad (0 description, 0 precaution, 0
   structured symptoms f dataset.csv) l fichier a part -- machi
   msaحhom, ghi khrejhom mn l track li 3ndo Knowledge Base kaملة.

Khddemha mn root dyal medai/ (mora ma dert check_disease_names.py):
    python finalize_symptom2disease.py
"""

import pandas as pd
from pathlib import Path

PROCESSED = Path("data/processed")

s2d = pd.read_csv(PROCESSED / "symptom2disease_tagged.csv")
disease_symptoms = pd.read_csv(PROCESSED / "disease_symptoms_long.csv")

known_norm = {d.lower(): d for d in disease_symptoms["Disease"]}


def canon(label):
    # ila l9a correspondance (hta b casse mkhتlfa), yrja3 l forme officielle
    # ila ma l9اch walou (3 diseases li b jed jdad), ykhلي kima hiya
    return known_norm.get(label.lower(), label)


s2d["label"] = s2d["label"].apply(canon)

out_of_scope = {
    "dimorphic hemorrhoids",
    "gastroesophageal reflux disease",
    "peptic ulcer disease",
}
mask_oos = s2d["label"].str.lower().isin(out_of_scope)

s2d_scope = s2d[~mask_oos].reset_index(drop=True)
s2d_oos = s2d[mask_oos].reset_index(drop=True)

s2d_scope.to_csv(PROCESSED / "symptom2disease_tagged.csv", index=False)
s2d_oos.to_csv(PROCESSED / "symptom2disease_out_of_scope.csv", index=False)

print(f"dakhel scope (41 diseases 'officiels'): {len(s2d_scope)} lignes, {s2d_scope['label'].nunique()} diseases")
print(f"khrjin l barra (0 Knowledge Base): {len(s2d_oos)} lignes")
print(f"  {sorted(s2d_oos['label'].unique())}")
