import pandas as pd
import numpy as np
import re

def safe_div(a, b):
    return np.where((b == 0) | pd.isna(b), np.nan, a / b)

def parse_floor_numeric(x):
    s = str(x).lower()
    if "/" in s:
        try:
            return float(s.split("/")[0])
        except:
            pass
    if "ground" in s:
        return 0.0
    m = re.search(r"(-?\d+)", s)
    return float(m.group(1)) if m else np.nan

def create_features(df):
    # assume price already parsed: amount_in_rupees or price_in_rupees
    price_col = "amount_in_rupees" if "amount_in_rupees" in df.columns else ("price_in_rupees" if "price_in_rupees" in df.columns else None)
    # price per sqft 
    if price_col:
        if "carpet_area_sqft" in df.columns:
            df["price_per_sqft"] = safe_div(df[price_col], df["carpet_area_sqft"])
        elif "super_area_sqft" in df.columns:
            df["price_per_sqft"] = safe_div(df[price_col], df["super_area_sqft"])
        else:
            df["price_per_sqft"] = np.nan

    # area ratio
    if "carpet_area_sqft" in df.columns and "super_area_sqft" in df.columns:
        df["carpet_super_ratio"] = safe_div(df["carpet_area_sqft"], df["super_area_sqft"])

    # floor numeric
    if "floor" in df.columns:
        df["floor_num"] = df["floor"].apply(parse_floor_numeric)

    # numeric bathroom & balcony
    for c in ["bathroom", "balcony"]:
        if c in df.columns:
            df[c] = pd.to_numeric(df[c], errors="coerce")

    # furnishing simplified
    if "furnishing" in df.columns:
        df["furnishing_simple"] = df["furnishing"].astype(str).str.lower().replace({
            "fully furnished":"furnished",
            "semi-furnished":"semi",
            "unfurnished":"unfurnished"
        })

    # car parking flag
    if "car_parking" in df.columns:
        df["car_parking_flag"] = df["car_parking"].astype(str).str.lower().str.contains("open|covered|yes|free|available|1", regex=True)
    else:
        df["car_parking_flag"] = False

    # top-k location to reduce cardinality
    if "location" in df.columns:
        topk = df["location"].value_counts().nlargest(30).index
        df["location_clean"] = df["location"].where(df["location"].isin(topk), other="other")

    # has_plot_area flag if plot_area_sqft exists
    if "plot_area_sqft" in df.columns:
        df["has_plot_area"] = df["plot_area_sqft"].notna()
    else:
        df["has_plot_area"] = False

    return df
