import re
import pandas as pd
from pathlib import Path

DATA_DIR = Path(__file__).parent.parent / "data"

def load_raw(name):
    path = DATA_DIR / "raw" / name
    return pd.read_csv(path)

def load_processed(name):
    path = DATA_DIR / "processed" / name
    return pd.read_csv(path)

def save_processed(df, name):
    path = DATA_DIR / "processed"
    path.mkdir(parents=True, exist_ok=True)
    df.to_csv(path / name, index=False)

def normalize_cols(df):
    def clean(c):
        c = c.strip().lower()
        c = c.replace("(", "").replace(")", "")
        c = re.sub(r"[^0-9a-z]+", "_", c)
        c = re.sub(r"_+", "_", c).strip("_")
        return c
    return df.rename(columns={c: clean(c) for c in df.columns})

def _is_float_like(x):
    try:
        float(x)
        return True
    except:
        return False

def parse_price_indian(value):
    if pd.isna(value):
        return None
    s = str(value).strip().lower().replace(",", "").replace(" ", "")
    # clean number
    if s.replace(".", "").isdigit():
        return float(s)
    # lac
    if "lac" in s:
        num = s.replace("lac", "")
        try:
            return float(num) * 100000
        except:
            return None
    # cr (crore)
    if "cr" in s:
        num = s.replace("cr", "")
        try:
            return float(num) * 10000000
        except:
            return None
    # fallback: try to extract numeric part
    m = re.search(r"([0-9]*\.?[0-9]+)", s)
    return float(m.group(1)) if m else None

def parse_area_to_sqft(val):
    if pd.isna(val):
        return None
    s = str(val).strip().lower().replace(",", "")
    # if range like '400-450 sqft', take mean
    if "-" in s:
        parts = [p for p in s.split("-") if p.strip()]
        nums = []
        for p in parts:
            m = re.search(r"([0-9]*\.?[0-9]+)", p)
            if m:
                nums.append(float(m.group(1)))
        if nums:
            num = sum(nums) / len(nums)
        else:
            return None
    else:
        m = re.search(r"([0-9]*\.?[0-9]+)", s)
        if not m:
            return None
        num = float(m.group(1))

    # unit detection
    if any(tok in s for tok in ["sqm", "sq.m", "sqmt", "m2", "sq.mtr", "square meter", "square metres", "sqmeter"]):
        return num * 10.7639
    if any(tok in s for tok in ["sqyd", "sqyrd", "sq.yd", "sqyard", "square yard", "yard", "yd"]):
        return num * 9.0
    if any(tok in s for tok in ["sqft", "sq.ft", "sq. ft", "sft", "sf", "square feet", "sqfeet"]):
        return num
    return num
