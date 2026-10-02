"""
inspect_data.py -- verification finale dyal Phase 1 (Etude & collecte)
9bel ma nbdaw Phase 2 (Data Engineering).

Khddemha mn jouj root dyal medai/ (fin kayn folder data/):
    python inspect_data.py
"""

import pandas as pd
from pathlib import Path

RAW = Path("data/raw")
EXTERNAL = Path("data/external")

# les fichiers "plats" (CSV wahda wahda) -- DODa 3andha script khas taht
flat_files = [
    RAW / "dataset.csv",
    RAW / "symptom_Description.csv",
    RAW / "symptom_precaution.csv",
    RAW / "Symptom-severity.csv",
    RAW / "Symptom2Disease.csv",
    EXTERNAL / "drugs_side_effects_drugs_com.csv",
    EXTERNAL / "medicines.csv",
]

for f in flat_files:
    print("=" * 70)
    print(f)

    if not f.exists():
        print("  ** MA KAYNACH ** -- chek smiya dyal fichier w path")
        continue

    try:
        df = pd.read_csv(f)
    except UnicodeDecodeError:
        df = pd.read_csv(f, encoding="latin1")
        print("  (UTF-8 ma khdemch, tfetha b encoding latin1)")

    print(f"shape: {df.shape}")
    print(f"columns: {list(df.columns)}")

    missing = df.isna().sum()
    missing = missing[missing > 0]
    if len(missing):
        print(f"missing values:\n{missing}")
    else:
        print("missing values: 0")

    print(df.head(2))
    print()

# DODa -- repo kamel, machi CSV wahda -- nchoufou chno kayn fih 9bel manqerrewh
print("=" * 70)
print("DODa (external/dataset-main/) -- fichiers li kayn:")
doda_dir = EXTERNAL / "dataset-main"
if doda_dir.exists():
    for item in sorted(doda_dir.rglob("*")):
        if item.is_file():
            print(" ", item.relative_to(doda_dir))
else:
    print("  ** MA KAYNACH **")

doda = Path("data/external/dataset-main")
health = pd.read_csv(doda / "semantic categories" / "health.csv")
body = pd.read_csv(doda / "semantic categories" / "humanbody.csv")

print("health.csv:", health.shape, list(health.columns))
print(health.head(10))
print()
print("humanbody.csv:", body.shape, list(body.columns))
print(body.head(10))