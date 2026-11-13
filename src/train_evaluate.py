"""Cross-validated inverse regression on the published fixed-geometry DRA dataset.

Method follows the model configuration and fold-wise scaling in Sensor_vF.ipynb.
No HFSS installation or proprietary simulation files are required.
"""
from __future__ import annotations

import argparse
import json
import warnings
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.exceptions import ConvergenceWarning
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import KFold
from sklearn.neural_network import MLPRegressor
from sklearn.preprocessing import StandardScaler

FEATURES = ["f_res_ghz", "s11_min_db", "q_factor", "re_z11_ohm", "im_z11_ohm"]
TARGETS = ["er", "tan_delta"]
SEED = 42
HIDDEN = (128, 64, 64, 32)


def load_data(path: Path) -> pd.DataFrame:
    df = pd.read_csv(path)
    required = FEATURES + TARGETS
    if df.empty or any(col not in df.columns for col in required):
        raise ValueError(f"Dataset must contain: {required}")
    if df[required].isna().any().any():
        raise ValueError("Dataset has missing model inputs or targets")
    if (df["tan_delta"] <= 0).any() or (df["q_factor"] <= 0).any():
        raise ValueError("tan_delta and q_factor must be positive")
    return df


def cross_validated_predictions(df: pd.DataFrame) -> pd.DataFrame:
    X = df[FEATURES].copy()
    X["q_factor"] = np.log10(X["q_factor"].clip(lower=1e-6))
    X = X.to_numpy(dtype=float)
    cv = KFold(n_splits=10, shuffle=True, random_state=SEED)
    result = pd.DataFrame({"er_true": df["er"], "tan_delta_true": df["tan_delta"]})

    for target in TARGETS:
        y = df[target].to_numpy(dtype=float)
        if target == "tan_delta":
            y = np.log10(y.clip(min=1e-6))
        pred = np.empty(len(y), dtype=float)
        for train, test in cv.split(X):
            scaler_x = StandardScaler().fit(X[train])
            scaler_y = StandardScaler().fit(y[train].reshape(-1, 1))
            if target == "er":
                model = MLPRegressor(hidden_layer_sizes=HIDDEN, solver="lbfgs",
                                     max_iter=2000, random_state=SEED)
            else:
                model = MLPRegressor(hidden_layer_sizes=HIDDEN, max_iter=5000,
                                     early_stopping=True, validation_fraction=0.1,
                                     n_iter_no_change=50, random_state=SEED)
            with warnings.catch_warnings():
                warnings.simplefilter("ignore", ConvergenceWarning)
                model.fit(scaler_x.transform(X[train]),
                          scaler_y.transform(y[train].reshape(-1, 1)).ravel())
            pred[test] = scaler_y.inverse_transform(
                model.predict(scaler_x.transform(X[test])).reshape(-1, 1)
            ).ravel()
        if target == "tan_delta":
            pred = 10.0 ** pred
        result[f"{target}_cv_pred"] = pred
    return result


def metrics(predictions: pd.DataFrame) -> dict:
    out = {}
    for target in TARGETS:
        actual = predictions[f"{target}_true"].to_numpy()
        predicted = predictions[f"{target}_cv_pred"].to_numpy()
        values = {
            "mae": float(mean_absolute_error(actual, predicted)),
            "rmse": float(np.sqrt(mean_squared_error(actual, predicted))),
            "r2": float(r2_score(actual, predicted)),
        }
        if target == "tan_delta":
            values["mae_log10"] = float(np.mean(np.abs(np.log10(predicted) - np.log10(actual))))
        out[target] = values
    return out


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data", type=Path, default=Path(__file__).resolve().parents[1] / "data" / "dataset.csv")
    parser.add_argument("--output", type=Path, default=Path("outputs"))
    parser.add_argument("--check", action="store_true", help="Check dataset integrity without training")
    args = parser.parse_args()
    df = load_data(args.data)
    print(f"Validated {len(df)} responses; {len(FEATURES)} features; 2 targets")
    if args.check:
        print("PASS: required columns, positivity, and missing values")
        return
    args.output.mkdir(parents=True, exist_ok=True)
    predictions = cross_validated_predictions(df)
    predictions.to_csv(args.output / "cv_predictions.csv", index=False)
    scores = metrics(predictions)
    (args.output / "cv_metrics.json").write_text(json.dumps(scores, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(scores, indent=2))
    print(f"Saved predictions and metrics to {args.output}")


if __name__ == "__main__":
    main()
