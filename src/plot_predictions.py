"""Plot cross-validated parity and residuals from train_evaluate.py output."""
from __future__ import annotations

import argparse
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--predictions", type=Path, default=Path("outputs/cv_predictions.csv"))
    parser.add_argument("--output", type=Path, default=Path("outputs/parity_residuals.pdf"))
    args = parser.parse_args()
    df = pd.read_csv(args.predictions)
    plt.rcParams.update({"font.family": "serif", "mathtext.fontset": "stix", "pdf.fonttype": 42})
    fig, axes = plt.subplots(2, 2, figsize=(9, 7), constrained_layout=True)
    for j, (target, label) in enumerate([("er", r"$\varepsilon_r$"), ("tan_delta", r"$\tan\delta$")]):
        actual = df[f"{target}_true"].to_numpy()
        predicted = df[f"{target}_cv_pred"].to_numpy()
        ax = axes[0, j]
        ax.scatter(actual, predicted, s=12, alpha=0.65)
        lo = min(actual.min(), predicted.min()) * (0.9 if j else 0.99)
        hi = max(actual.max(), predicted.max()) * (1.1 if j else 1.01)
        ax.plot([lo, hi], [lo, hi], "k--", lw=1)
        if j:
            ax.set_xscale("log")
            ax.set_yscale("log")
        ax.set_xlabel("True " + label)
        ax.set_ylabel("Predicted " + label)
        ax.grid(alpha=0.2)
        ax = axes[1, j]
        residual = (np.log10(predicted) - np.log10(actual)) if j else (predicted - actual)
        ax.scatter(actual, residual, s=12, alpha=0.65)
        ax.axhline(0, color="black", ls="--", lw=1)
        if j:
            ax.set_xscale("log")
        ax.set_xlabel("True " + label)
        ax.set_ylabel(r"$\log_{10}(\hat y/y)$" if j else "Prediction − true")
        ax.grid(alpha=0.2)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(args.output, bbox_inches="tight")
    plt.close(fig)
    print(f"Saved {args.output}")


if __name__ == "__main__":
    main()
