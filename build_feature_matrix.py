"""
build_feature_matrix.py -- Phase 3 (Baseline ML), 1ere brique: matrice
binaire par INSTANCE (machi par disease).

MOHIM: disease_symptoms_long.csv (41 satr) mezyan l reference/knowledge
view, walakin ma sale7ch l training -- fiha ghi 1 satr = 1 disease (41
exemple total, 1 bark par classe). dataset.csv l asli fih ~4920 satr =
~120 "cas" (instance) par disease, kol wahd b combinaison mختلفة dyal
symptomes -- hadi li khassna l ML b jed.

Khddemha mn root dyal medai/:
    python build_feature_matrix.py
"""

import pandas as pd
from pathlib import Path

RAW = Path("data/raw")
PROCESSED = Path("data/processed")

dataset = pd.read_csv(RAW / "dataset.csv")
symptom_translations = pd.read_csv(PROCESSED / "symptom_translations.csv")


def normalize(series):
    return (
        series.str.strip()
        .str.lower()
        .str.replace("_", " ", regex=False)
        .str.replace(r"\s+", " ", regex=True)
    )


dataset["Disease"] = dataset["Disease"].str.strip()
dataset["instance_id"] = dataset.index  # kol satr f dataset.csv = 1 cas

symptom_cols = [c for c in dataset.columns if c.startswith("Symptom_")]

long_df = dataset.melt(
    id_vars=["instance_id", "Disease"],
    value_vars=symptom_cols,
    value_name="symptom_raw",
).dropna(subset=["symptom_raw"])

long_df["normalized_expression"] = normalize(long_df["symptom_raw"])

merged = long_df.merge(
    symptom_translations[["symptom_id", "normalized_expression"]],
    on="normalized_expression",
    how="left",
)

n_unmatched = int(merged["symptom_id"].isna().sum())
if n_unmatched:
    print(f"ATTENTION: {n_unmatched} unmatched -- khass ykon 0 (dir fix_typo.py/fix_missing_symptom.py 9bel)")

# pivot l matrice binaire: 1 instance (satr asli) = 1 satr, 1 symptom_id = 1 colonne
matrix = (
    merged.assign(present=1)
    .pivot_table(index=["instance_id", "Disease"], columns="symptom_id", values="present", fill_value=0)
    .reset_index()
)
matrix.columns.name = None

symptom_id_cols = [c for c in matrix.columns if c.startswith("S")]
matrix[symptom_id_cols] = matrix[symptom_id_cols].astype(int)

out_path = PROCESSED / "ml_feature_matrix.csv"
matrix.to_csv(out_path, index=False)

print(f"saved -> {out_path}")
print(f"shape: {matrix.shape}  ({len(matrix)} instances x {len(symptom_id_cols)} symptomes)")
print(f"diseases: {matrix['Disease'].nunique()}")
print(f"\ninstances par disease (min/mean/max): "
      f"{matrix['Disease'].value_counts().min()} / "
      f"{matrix['Disease'].value_counts().mean():.1f} / "
      f"{matrix['Disease'].value_counts().max()}")
print()
print(matrix.iloc[:5, :8])
