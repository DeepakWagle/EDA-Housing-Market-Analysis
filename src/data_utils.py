import pandas as pd
from pathlib import Path

DATA_DIR = Path(__file__).parent.parent / "data"

def load_raw(csv_name: str):
    path = DATA_DIR / "raw" / csv_name
    df = pd.read_csv(path)
    return df

def save_processed(df: pd.DataFrame, name: str):
    path = DATA_DIR / "processed"
    path.mkdir(parents=True, exist_ok=True)
    df.to_csv(path / name, index=False)
