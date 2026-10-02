"""
reshape_dataset.py -- Phase 2, 2eme brique: n7ولو dataset.csv (wide,
Symptom_1..17) l format "long" (Disease, symptom_id), mrebtin b
symptom_translations.csv li bnina f l'étape li fatet.

Khddemha mn root dyal medai/:
    python reshape_dataset.py
"""

import pandas as pd
from pathlib import Path

RAW = Path("data/raw")
PROCESSED = Path("data/processed")

dataset = pd.read_csv(RAW / "dataset.csv")
symptom_translations = pd.read_csv(PROCESSED / "symptom_translations.csv")


def normalize(series):
    # nafss normalisation li khddmna biha f build_symptom_table.py --
    # khassha tkon identique bach l jonction tnjah
    return (
        series.str.strip()
        .str.lower()
        .str.replace("_", " ", regex=False)
        .str.replace(r"\s+", " ", regex=True)
    )


dataset["Disease"] = dataset["Disease"].str.strip()
symptom_cols = [c for c in dataset.columns if c.startswith("Symptom_")]

# wide -> long: kol (Disease, Symptom_N) ykon sطr wahd, ndoro les NaN
# (l ghaleb dyal slots khawyin -- normal, machi kol disease 3ndha 17 symptome)
long_df = dataset.melt(
    id_vars="Disease",
    value_vars=symptom_cols,
    value_name="symptom_raw",
).dropna(subset=["symptom_raw"])

long_df["normalized_expression"] = normalize(long_df["symptom_raw"])

# jonction m3a la table canonique -- howa hna ghadi ybane wach dataset.csv
# kaykhdem b nafss vocabulaire dyal Symptom-severity.csv wla lla
merged = long_df.merge(
    symptom_translations[["symptom_id", "normalized_expression"]],
    on="normalized_expression",
    how="left",
)

n_matched = int(merged["symptom_id"].notna().sum())
n_total = len(merged)
unmatched = sorted(merged[merged["symptom_id"].isna()]["normalized_expression"].unique())

print(f"lignes (disease, symptome) total: {n_total}")
print(f"matched: {n_matched}")
print(f"unmatched: {n_total - n_matched}")
if unmatched:
    print(f"\nsymptomes li ma tl9awch f symptom_translations.csv ({len(unmatched)}):")
    for s in unmatched:
        print(" -", s)
    print("\n(hadi machi erreur -- kaybane lina wach kayn vocabulaire f dataset.csv")
    print(" li machi f Symptom-severity.csv. nchoufouha ensemble f la prochaine étape.)")

# output: Disease + liste dyal symptom_id (bark li matched, dedupliqués)
final = (
    merged[merged["symptom_id"].notna()]
    .groupby("Disease")["symptom_id"]
    .apply(lambda x: sorted(set(x)))
    .reset_index()
    .rename(columns={"symptom_id": "symptom_ids"})
)

out_path = PROCESSED / "disease_symptoms_long.csv"
final.to_csv(out_path, index=False)
print(f"\nsaved -> {out_path}  shape={final.shape}")
print(final.head(10))
