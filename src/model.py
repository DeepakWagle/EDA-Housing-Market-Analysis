from pathlib import Path
import joblib
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, mean_absolute_error
import numpy as np

PROJECT_ROOT = Path(__file__).resolve().parents[1]
MODELS_DIR = PROJECT_ROOT / "data" / "models"
MODELS_DIR.mkdir(parents=True, exist_ok=True)

def train_baseline(X_train, y_train):
    model = LinearRegression()
    model.fit(X_train, y_train)
    return model

def evaluate(model, X, y):
    preds = model.predict(X)
    return {
        "rmse": np.sqrt(mean_squared_error(y, preds)),
        "mae": mean_absolute_error(y, preds)
    }

def save_model(model, filename):
    path = MODELS_DIR / filename
    joblib.dump(model, path)
    print(f"✅ Model saved at: {path}")
