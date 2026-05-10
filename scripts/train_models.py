"""Train and save PM2.5 forecast models from the local SQLite database.

Outputs:
  models/xgb_h6.joblib     — XGBoost, +6 h horizon
  models/ridge_h12.joblib  — Ridge,    +12 h horizon
  models/ridge_h24.joblib  — Ridge,    +24 h horizon
  models/feature_cols.json — ordered list of feature columns

Usage:
  uv run python scripts/train_models.py
"""

from __future__ import annotations

import json
from pathlib import Path

import joblib
import numpy as np

from src.features.pipeline import build_feature_matrix
from src.models.baselines import train_ridge
from src.models.xgboost_model import train as train_xgb

HORIZONS = {6: "xgb", 12: "ridge", 24: "ridge"}
MODELS_DIR = Path(__file__).resolve().parent.parent / "models"
MODELS_DIR.mkdir(exist_ok=True)

FEATURE_EXCLUDE = {"pm25", "cams_pm25"}


def get_feature_cols(df):
    return [c for c in df.columns if c not in FEATURE_EXCLUDE]


def main():
    print("Building feature matrix from DB…")
    df = build_feature_matrix()
    print(f"  {len(df):,} rows, {df.index[0]} → {df.index[-1]}")

    feat_cols = get_feature_cols(df)
    print(f"  {len(feat_cols)} features")

    # Save feature column list
    (MODELS_DIR / "feature_cols.json").write_text(json.dumps(feat_cols))

    # 80/20 temporal split
    split = int(len(df) * 0.80)
    train_df = df.iloc[:split]

    X_train = train_df[feat_cols]

    for h, model_type in HORIZONS.items():
        # Target: pm25 value h hours ahead
        y_train = train_df["pm25"].shift(-h).dropna()
        X_h = X_train.loc[y_train.index]

        print(f"\nTraining {model_type.upper()} h={h}…")
        if model_type == "xgb":
            model = train_xgb(X_h, y_train)
        else:
            model = train_ridge(X_h, y_train, alpha=1.0)

        out = MODELS_DIR / f"{model_type}_h{h}.joblib"
        joblib.dump(model, out)
        print(f"  Saved → {out.relative_to(Path.cwd())}")

        # Quick sanity check on train set
        preds = model.predict(X_h)
        rmse = np.sqrt(np.mean((preds - y_train.values) ** 2))
        print(f"  Train RMSE: {rmse:.2f} μg/m³")

    print("\nDone.")


if __name__ == "__main__":
    main()
