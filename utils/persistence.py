# utils/persistence.py
# Sauvegarde / chargement JSON simple

import json
import os

def ensure_parent_dir(path: str):
    parent = os.path.dirname(path)
    if parent and not os.path.exists(parent):
        os.makedirs(parent, exist_ok=True)

def save_json(path: str, data: dict):
    """Sauvegarde un dict en JSON (avec création auto du dossier)."""
    ensure_parent_dir(path)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def load_json(path: str) -> dict:
    """Charge un dict depuis un fichier JSON (retourne {} si absent)."""
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}
