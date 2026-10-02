"""
Setup script dyal MedAI -- ykhalq structure dyal project kifma katgoul
le cahier des charges (section 24).

Usage:
    python setup_project.py
(khddmha mn jouj l folder li bghiti tkhalq fih medai/, masalan Desktop
aw wa7ed dossier "projets")
"""

from pathlib import Path

BASE = Path("medai")

# Chaque folder kayna3ss wahed l etape f pipeline (section 5 dyal cahier):
# preprocessing -> nlp -> models -> prediction -> safety -> database
folders = [
    "data/raw",          # datasets kima jaw (bla ma tbeddel walo fihom)
    "data/processed",    # ba3d cleaning/normalisation
    "data/external",     # sources external (drug info, translations...)
    "notebooks",         # EDA, preprocessing, training, evaluation
    "src/preprocessing",
    "src/nlp",
    "src/models",
    "src/prediction",
    "src/safety",
    "src/database",
    "api",               # FastAPI app (Phase 8)
    "frontend",          # Streamlit prototype (Phase 9)
    "models",            # saved model artifacts (.pkl, .joblib...)
    "tests",             # pytest
]

for folder in folders:
    (BASE / folder).mkdir(parents=True, exist_ok=True)

# __init__.py bach src/* ykono packages Python vrai qualifiés
# (bila hadchi, "from src.nlp import ..." ghaydi error)
init_targets = [
    "src", "src/preprocessing", "src/nlp", "src/models",
    "src/prediction", "src/safety", "src/database", "tests",
]
for folder in init_targets:
    (BASE / folder / "__init__.py").touch(exist_ok=True)

# fichiers dyal base -- khawi daba, ghan3mrohom step by step
(BASE / "api" / "main.py").touch(exist_ok=True)
(BASE / "frontend" / "app.py").touch(exist_ok=True)
(BASE / "Dockerfile").touch(exist_ok=True)

# requirements minimal l Phase 1/2 bark (data study + cleaning).
# ghadi nzidou scikit-learn/xgboost f Phase 3, fastapi f Phase 8, etc.
# -- bla ma nthaqlou l install b library li mazal ma khddamnahach.
(BASE / "requirements.txt").write_text(
    "pandas\nnumpy\npython-dotenv\njupyter\n"
)

(BASE / "README.md").write_text(
    "# MedAI\n\n"
    "Systeme multilingue d'analyse des symptomes et de prediction de "
    "conditions medicales.\n"
    "Prototype academique -- PAS un outil de diagnostic.\n"
)

# n7dou data/ w venv/ mn git -- data kbira/privee w venv local bark
(BASE / ".gitignore").write_text(
    "venv/\n__pycache__/\n*.pyc\n"
    "data/raw/\ndata/processed/\n"
    ".env\n.ipynb_checkpoints/\n"
)

print(f"Structure created f: {BASE.resolve()}")
