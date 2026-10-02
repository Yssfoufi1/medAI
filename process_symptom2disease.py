"""
process_symptom2disease.py -- Phase 2, 3eme brique: Symptom2Disease.csv
(texte libre, 1200 lignes).

Hna machi exact-match b7al dataset.csv -- houma phrases naturelles, so
kanqelbo b naive substring search: wach kol symptome canonique (ism
dyalo b l kamel, b7al "skin rash") kayban l-interieur dyal text.

ATTENTION: hadi ghi baseline Phase 2, machi NLP real. Ghadi tfewwet
beaucoup dyal symptomes li makatbanch b nafss les mots exacts (b7al
"pain in my joints" machi "joint pain") -- Phase 4 ghadi tsewb hadchi
b synonymes/embeddings. Daba bghina ghi coverage initiale.

Khddemha mn root dyal medai/:
    python process_symptom2disease.py
"""

import pandas as pd
from pathlib import Path

RAW = Path("data/raw")
PROCESSED = Path("data/processed")

s2d = pd.read_csv(RAW / "Symptom2Disease.csv")
s2d = s2d.drop(columns=["Unnamed: 0"])
s2d["label"] = s2d["label"].str.strip()

symptom_translations = pd.read_csv(PROCESSED / "symptom_translations.csv")
disease_symptoms = pd.read_csv(PROCESSED / "disease_symptoms_long.csv")

# 1. wach les diseases dyal Symptom2Disease homa nafss les 41 li 3ndna,
#    wla kayn jdad (extension dyal taxonomie)?
known_diseases = set(disease_symptoms["Disease"])
s2d_diseases = set(s2d["label"])

print(f"Diseases f Symptom2Disease: {len(s2d_diseases)}")
print(f"Diseases li 3ndna already (dataset.csv): {len(known_diseases)}")
new_diseases = sorted(s2d_diseases - known_diseases)
print(f"Jdad (f Symptom2Disease bark): {len(new_diseases)}")
if new_diseases:
    print(" ", new_diseases)
missing = sorted(known_diseases - s2d_diseases)
print(f"Ma jawch f Symptom2Disease (f les 41 bark): {len(missing)}")
print()

# 2. naive extraction: substring search (case-insensitive) dyal kol
#    phrase canonique dakhel kol text
canonical_phrases = symptom_translations["normalized_expression"].tolist()
canonical_ids = symptom_translations["symptom_id"].tolist()


def extract_symptoms(text):
    text_low = text.lower()
    return [sid for phrase, sid in zip(canonical_phrases, canonical_ids) if phrase in text_low]


s2d["detected_symptom_ids"] = s2d["text"].apply(extract_symptoms)
s2d["n_detected"] = s2d["detected_symptom_ids"].apply(len)

n_zero = int((s2d["n_detected"] == 0).sum())
print(f"lignes b 0 symptome detecte (naive): {n_zero} / {len(s2d)}  ({n_zero / len(s2d):.1%})")
print(f"moyenne symptomes detectes par ligne: {s2d['n_detected'].mean():.2f}")
print()
print(s2d[["label", "text", "n_detected"]].head(8).to_string())

out_path = PROCESSED / "symptom2disease_tagged.csv"
s2d.to_csv(out_path, index=False)
print(f"\nsaved -> {out_path}  shape={s2d.shape}")
