from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent
BRAIN_FILE = BASE_DIR / "knowledge" / "Cérebro_Robbie.txt"


def carregar_cerebro():
    with open(BRAIN_FILE, "r", encoding="utf-8") as arquivo:
        return arquivo.read()