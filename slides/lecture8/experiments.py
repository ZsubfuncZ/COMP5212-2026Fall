#!/usr/bin/env python3
"""Reproducible K-means lecture experiments.

The script writes vector (PDF) and raster (PNG) figures to ``assets/实验图``
and a machine-readable record of all parameters and metrics to
``experiment-results.json``.  It deliberately keeps the random seed used for
the JL projection separate from the seed used by K-means.
"""

from __future__ import annotations

import hashlib
import json
import os
import platform
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

os.environ.setdefault("MPLCONFIGDIR", "work/mplconfig")

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import scipy
import sklearn
from matplotlib.colors import ListedColormap
from matplotlib.ticker import MaxNLocator
from scipy.optimize import linear_sum_assignment
from sklearn.cluster import KMeans
from sklearn.datasets import load_sample_image, make_circles, make_moons
from sklearn.metrics import adjusted_rand_score
from sklearn.preprocessing import StandardScaler
import threadpoolctl
from threadpoolctl import threadpool_limits


ROOT = Path(__file__).resolve().parent
FIG_DIR = ROOT / "assets" / "实验图"
RESULT_PATH = ROOT / "experiment-results.json"

# Colors used by the supplied lecture template, with two quiet companions for
# multi-class plots.  The first three colors are kept stable across figures.
ORANGE = "#FF5500"
GREEN = "#4C7954"
GRAYBLUE = "#6F8296"
LIGHTGREEN = "#A8C9A0"
LIGHTGRAY = "#D9E1E8"
INK = "#1E2428"
PALETTE = [ORANGE, GREEN, GRAYBLUE, "#B98B37", "#8B5E83", "#2A788E"]


def _style() -> None:
    """Set a readable, template-compatible matplotlib style."""

    plt.rcParams.update(
        {
            "font.family": "DejaVu Sans",
            "font.size": 12,
            "axes.titlesize": 15,
            "axes.labelsize": 13,
            "axes.titleweight": "bold",
            "axes.edgecolor": "#AAB3BA",
            "axes.linewidth": 0.8,
            "xtick.labelsize": 11,
            "ytick.labelsize": 11,
            "legend.fontsize": 10,
            "figure.facecolor": "white",
            "axes.facecolor": "white",
            "savefig.facecolor": "white",
            "pdf.fonttype": 42,
            "ps.fonttype": 42,
        }
    )


def _save(fig: plt.Figure, stem: str) -> dict[str, str]:
    """Save a figure in both vector and raster formats."""

    FIG_DIR.mkdir(parents=True, exist_ok=True)
    png = FIG_DIR / f"{stem}.png"
    pdf = FIG_DIR / f"{stem}.pdf"
    fig.savefig(png, dpi=220, bbox_inches="tight")
    fig.savefig(pdf, bbox_inches="tight")
    plt.close(fig)
    return {"png": str(png.relative_to(ROOT)), "pdf": str(pdf.relative_to(ROOT))}


def _mapped_labels(labels: np.ndarray, centers: np.ndarray, reference: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    """Map arbitrary K-means label IDs to the nearest reference IDs."""

    costs = np.linalg.norm(centers[:, None, :] - reference[None, :, :], axis=2)
    rows, cols = linear_sum_assignment(costs)
    mapping = {int(r): int(c) for r, c in zip(rows, cols)}
    mapped = np.array([mapping[int(label)] for label in labels], dtype=int)
    return mapped, centers[rows[np.argsort(cols)]] if len(rows) else centers


def run_scale_experiment() -> dict:
    """Compare raw and standardized K-means assignments on the same axes."""

    rng = np.random.default_rng(1206)
    latent_centers = np.array([[-3.0, -1.0], [0.0, -1.0], [0.0, 1.45]])
    n_per = 150
    latent = np.vstack(
        [center + rng.normal(scale=[0.52, 0.34], size=(n_per, 2)) for center in latent_centers]
    )
    y_true = np.repeat(np.arange(len(latent_centers)), n_per)
    scales = np.array([1.0, 8.0])
    X = latent * scales

    raw = KMeans(n_clusters=3, n_init=10, random_state=17).fit(X)
    scaler = StandardScaler().fit(X)
    standardized = KMeans(n_clusters=3, n_init=10, random_state=17).fit(scaler.transform(X))
    raw_labels = raw.labels_
    std_labels = standardized.labels_
    raw_mapped, _ = _mapped_labels(raw_labels, raw.cluster_centers_, latent_centers * scales)
    std_centers_original = scaler.inverse_transform(standardized.cluster_centers_)
    std_mapped, _ = _mapped_labels(std_labels, std_centers_original, latent_centers * scales)
    std_center_order = np.zeros(3, dtype=int)
    # Order the inverse-transformed centers by the reference cluster ID.
    costs = np.linalg.norm(std_centers_original[:, None, :] - (latent_centers * scales)[None, :, :], axis=2)
    rows, cols = linear_sum_assignment(costs)
    for r, c in zip(rows, cols):
        std_center_order[c] = r
    raw_center_order = np.zeros(3, dtype=int)
    rows, cols = linear_sum_assignment(np.linalg.norm(raw.cluster_centers_[:, None, :] - (latent_centers * scales)[None, :, :], axis=2))
    for r, c in zip(rows, cols):
        raw_center_order[c] = r
    raw_centers_plot = raw.cluster_centers_[raw_center_order]
    std_centers_plot = std_centers_original[std_center_order]

    fig, axes = plt.subplots(1, 2, figsize=(12.2, 5.2), sharex=True, sharey=True)
    for ax, labels, centers, title, ari in [
        (axes[0], raw_mapped, raw_centers_plot, "Raw coordinates", adjusted_rand_score(y_true, raw_labels)),
        (axes[1], std_mapped, std_centers_plot, "After StandardScaler", adjusted_rand_score(y_true, std_labels)),
    ]:
        for cluster_id in range(3):
            mask = labels == cluster_id
            ax.scatter(X[mask, 0], X[mask, 1], s=16, alpha=0.66, color=PALETTE[cluster_id], linewidths=0)
            ax.scatter(
                centers[cluster_id, 0], centers[cluster_id, 1], marker="X", s=145,
                color=PALETTE[cluster_id], edgecolor="white", linewidth=1.4, zorder=4,
            )
        ax.set_title(f"{title}\nARI vs. generating labels = {ari:.3f}")
        ax.set_xlabel("feature 1")
        ax.grid(alpha=0.16)
        # Keep the original coordinates (the y axis is intentionally scaled),
        # but let each panel use its available width so tick labels remain
        # legible in a lecture slide.
        ax.set_aspect("auto")
        ax.xaxis.set_major_locator(MaxNLocator(nbins=4))
        ax.tick_params(axis="x", labelsize=10)
    axes[0].set_ylabel("feature 2 (8× scale)")
    fig.suptitle("Scale changes the Euclidean geometry", color=ORANGE, fontsize=18, fontweight="bold", y=1.03)
    fig.text(0.5, -0.02, "Synthetic data · identical original coordinates in both panels · X markers are fitted centroids", ha="center", fontsize=10.5, color="#4E5B64")
    fig.tight_layout()
    paths = _save(fig, "01_scale_raw_vs_standardized")
    return {
        "figure": paths,
        "parameters": {"seed": 1206, "n_per_cluster": n_per, "n_clusters": 3, "feature_scales": scales.tolist(), "kmeans_n_init": 10, "kmeans_seed": 17},
        "metrics": {"raw_ari": float(adjusted_rand_score(y_true, raw_labels)), "standardized_ari": float(adjusted_rand_score(y_true, std_labels)), "raw_inertia": float(raw.inertia_), "standardized_inertia_in_scaled_space": float(standardized.inertia_)},
        "note": "Colors are label-matched to the generating clusters for visual comparison; the assignments are from fitted KMeans runs.",
    }


def run_shape_experiment() -> dict:
    """Show K-means assignments on non-convex synthetic shapes."""

    moon_x, moon_y = make_moons(n_samples=600, noise=0.065, random_state=7)
    circle_x, circle_y = make_circles(n_samples=600, factor=0.42, noise=0.055, random_state=8)
    runs = [("Two moons", moon_x, moon_y), ("Concentric circles", circle_x, circle_y)]
    fig, axes = plt.subplots(1, 2, figsize=(12.0, 5.2))
    metrics = {}
    for ax, (name, X, y_true) in zip(axes, runs):
        km = KMeans(n_clusters=2, n_init=10, random_state=0).fit(X)
        ari = adjusted_rand_score(y_true, km.labels_)
        metrics[name.lower().replace(" ", "_")] = {"n_samples": int(len(X)), "noise": 0.065 if name == "Two moons" else 0.055, "factor": 0.42 if name != "Two moons" else None, "ari": float(ari), "inertia": float(km.inertia_)}
        for c in range(2):
            mask = km.labels_ == c
            ax.scatter(X[mask, 0], X[mask, 1], s=15, color=PALETTE[c], alpha=0.72, linewidths=0)
        ax.scatter(km.cluster_centers_[:, 0], km.cluster_centers_[:, 1], marker="X", s=130, color=INK, edgecolor="white", linewidth=1.2, zorder=4)
        ax.set_title(f"{name}\nK-means ARI = {ari:.3f}")
        ax.set_xlabel("feature 1")
        ax.set_aspect("equal", adjustable="box")
        ax.grid(alpha=0.16)
    axes[0].set_ylabel("feature 2")
    fig.suptitle("A Voronoi partition cannot follow every shape", color=ORANGE, fontsize=18, fontweight="bold", y=1.03)
    fig.text(0.5, -0.02, "Synthetic data · colors are K-means assignments (n_clusters = 2, n_init = 10, seed = 0)", ha="center", fontsize=10.5, color="#4E5B64")
    fig.tight_layout()
    paths = _save(fig, "02_shape_failure_kmeans")
    return {"figure": paths, "parameters": {"n_clusters": 2, "n_init": 10, "kmeans_seed": 0}, "metrics": metrics, "note": "The figure shows K-means only; ARI is a diagnostic against the synthetic generating labels, not a training objective."}


def _psnr(mse: float, max_value: float = 255.0) -> float:
    return float(10.0 * np.log10((max_value**2) / mse)) if mse > 0 else float("inf")


def run_image_experiment() -> dict:
    """Quantize sklearn's real china.jpg with K-means color palettes."""

    image = load_sample_image("china.jpg")
    image_path = Path(sklearn.__file__).resolve().parent / "datasets" / "images" / "china.jpg"
    readme_path = image_path.parent / "README.txt"
    license_text = readme_path.read_text(encoding="utf-8") if readme_path.exists() else ""
    image_hash = hashlib.sha256(image_path.read_bytes()).hexdigest()
    original = image.astype(np.float64)
    pixels = original.reshape(-1, 3)
    train_size = 10_000
    sample_rng = np.random.default_rng(0)
    train_idx = np.sort(sample_rng.choice(len(pixels), size=train_size, replace=False))
    train = pixels[train_idx]
    ks = [4, 16, 64]
    quantized_images = [image]
    records = []
    with threadpool_limits(limits=1):
        for k in ks:
            km = KMeans(n_clusters=k, n_init=10, random_state=0).fit(train)
            all_labels = km.predict(pixels)
            reconstruction = km.cluster_centers_[all_labels].reshape(original.shape)
            mse = float(np.mean((original - reconstruction) ** 2))
            train_mse = float(np.mean((train - km.cluster_centers_[km.labels_]) ** 2))
            quantized_images.append(np.clip(np.rint(reconstruction), 0, 255).astype(np.uint8))
            records.append({"k": k, "mse_all_pixels": mse, "psnr_db_all_pixels": _psnr(mse), "train_mse": train_mse, "inertia_train": float(km.inertia_), "n_iter": int(km.n_iter_), "n_unique_colors_in_reconstruction": int(np.unique(all_labels).size)})
    fig, axes = plt.subplots(1, 4, figsize=(15.8, 4.55))
    labels = ["Original", "K = 4", "K = 16", "K = 64"]
    axes[0].imshow(quantized_images[0])
    axes[0].set_title("Original\nchina.jpg")
    for ax, im, label, rec in zip(axes[1:], quantized_images[1:], labels[1:], records):
        ax.imshow(im)
        ax.set_title(f"{label}\nMSE = {rec['mse_all_pixels']:.2f}")
    for ax in axes:
        ax.axis("off")
    fig.suptitle("K-means color quantization", color=ORANGE, fontsize=18, fontweight="bold", y=1.03)
    fig.text(0.5, -0.015, "Real image from scikit-learn sample data · 10,000 training pixels (seed = 0) · MSE evaluated on all 273,280 pixels", ha="center", fontsize=10.2, color="#4E5B64")
    fig.tight_layout()
    paths = _save(fig, "03_image_color_quantization_china")
    return {"figure": paths, "source": {"image_path": str(image_path), "sha256": image_hash, "readme_path": str(readme_path), "license_and_attribution": license_text.strip(), "license_url": "https://creativecommons.org/licenses/by/2.0/", "attribution_url": "https://www.flickr.com/photos/danielbuechele/", "retrieved_source_url": "https://www.flickr.com/photos/danielbuechele/6061409035/sizes/z/in/photostream/"}, "parameters": {"image_shape": list(image.shape), "train_pixels": train_size, "sampling_seed": 0, "ks": ks, "kmeans_n_init": 10, "kmeans_seed": 0, "evaluation": "all pixels", "rounding_for_display": "nearest uint8 only after metric calculation"}, "metrics": records}


def _pairwise_squared_distances(X: np.ndarray) -> np.ndarray:
    norms = np.einsum("ij,ij->i", X, X)
    d2 = norms[:, None] + norms[None, :] - 2.0 * (X @ X.T)
    d2 = np.maximum(d2, 0.0)
    upper = np.triu_indices(X.shape[0], k=1)
    return d2[upper]


def _sse_from_labels(X: np.ndarray, labels: np.ndarray, n_clusters: int) -> float:
    centers = np.vstack([X[labels == c].mean(axis=0) for c in range(n_clusters)])
    residual = X - centers[labels]
    return float(np.einsum("ij,ij->", residual, residual))


def _jl_summary(values: list[float]) -> dict[str, float]:
    arr = np.asarray(values, dtype=np.float64)
    return {"mean": float(np.mean(arr)), "median": float(np.median(arr)), "p95": float(np.quantile(arr, 0.95)), "max": float(np.max(arr))}


def run_jl_experiment() -> dict:
    """Project a high-dimensional synthetic mixture and audit K-means geometry."""

    data_seed = 20261006
    rng = np.random.default_rng(data_seed)
    n_clusters, n_per, d = 5, 120, 512
    n = n_clusters * n_per
    # Random directions make the cluster centers non-axis-aligned.  The
    # moderate radius/noise ratio gives a nontrivial, but readable, mixture.
    directions = rng.normal(size=(n_clusters, d))
    directions /= np.linalg.norm(directions, axis=1, keepdims=True)
    centers = directions * 8.0
    y_true = np.repeat(np.arange(n_clusters), n_per)
    X = centers[y_true] + rng.normal(scale=0.40, size=(n, d))
    projection_seeds = [11, 29, 47]
    kmeans_seeds = [31415, 27182, 16180]
    dimensions = [16, 32, 64, 128]

    with threadpool_limits(limits=1):
        baseline = KMeans(n_clusters=n_clusters, n_init=10, random_state=2718).fit(X)
        baseline_single = []
        for seed in range(10):
            one = KMeans(n_clusters=n_clusters, n_init=1, random_state=seed).fit(X)
            baseline_single.append({"seed": seed, "inertia": float(one.inertia_), "ari": float(adjusted_rand_score(y_true, one.labels_))})
    original_pairwise = _pairwise_squared_distances(X)
    runs = []
    for m in dimensions:
        for projection_seed, kmeans_seed in zip(projection_seeds, kmeans_seeds):
            projection_rng = np.random.default_rng(projection_seed)
            R = projection_rng.normal(size=(m, d)) / np.sqrt(m)
            t0 = time.perf_counter()
            Y = X @ R.T
            projection_seconds = time.perf_counter() - t0
            projected_pairwise = _pairwise_squared_distances(Y)
            relative_distortion = projected_pairwise / original_pairwise - 1.0
            t1 = time.perf_counter()
            with threadpool_limits(limits=1):
                km = KMeans(n_clusters=n_clusters, n_init=10, random_state=kmeans_seed).fit(Y)
            clustering_seconds = time.perf_counter() - t1
            original_sse_from_projected_labels = _sse_from_labels(X, km.labels_, n_clusters)
            runs.append({"m": m, "projection_seed": projection_seed, "kmeans_seed": kmeans_seed, "n_init": 10, "projected_inertia": float(km.inertia_), "original_sse_from_projected_labels": original_sse_from_projected_labels, "sse_ratio_to_full_space_n_init10": float(original_sse_from_projected_labels / baseline.inertia_), "ari_vs_generating_labels": float(adjusted_rand_score(y_true, km.labels_)), "projection_seconds": float(projection_seconds), "clustering_seconds": float(clustering_seconds), "total_seconds": float(projection_seconds + clustering_seconds), "pairwise_relative_distortion": {"signed_mean": float(np.mean(relative_distortion)), "signed_median": float(np.median(relative_distortion)), "absolute_median": float(np.median(np.abs(relative_distortion))), "absolute_p95": float(np.quantile(np.abs(relative_distortion), 0.95)), "absolute_max": float(np.max(np.abs(relative_distortion))), "n_pairs": int(len(relative_distortion))}})

    summary = {}
    for m in dimensions:
        selected = [r for r in runs if r["m"] == m]
        summary[str(m)] = {
            "sse_ratio": _jl_summary([r["sse_ratio_to_full_space_n_init10"] for r in selected]),
            "ari": _jl_summary([r["ari_vs_generating_labels"] for r in selected]),
            "absolute_pairwise_distortion_median": _jl_summary([r["pairwise_relative_distortion"]["absolute_median"] for r in selected]),
            "absolute_pairwise_distortion_p95": _jl_summary([r["pairwise_relative_distortion"]["absolute_p95"] for r in selected]),
            "projection_seconds": _jl_summary([r["projection_seconds"] for r in selected]),
            "clustering_seconds": _jl_summary([r["clustering_seconds"] for r in selected]),
        }

    fig, axes = plt.subplots(1, 3, figsize=(14.5, 4.75))
    x = np.array(dimensions)
    for m in dimensions:
        selected = [r for r in runs if r["m"] == m]
        axes[0].scatter([m] * len(selected), [r["sse_ratio_to_full_space_n_init10"] for r in selected], color=ORANGE, s=48, zorder=3)
        axes[1].scatter([m] * len(selected), [r["pairwise_relative_distortion"]["absolute_p95"] for r in selected], color=GREEN, s=48, zorder=3)
        axes[1].scatter([m] * len(selected), [r["pairwise_relative_distortion"]["absolute_median"] for r in selected], color=GRAYBLUE, s=34, zorder=3)
    axes[0].axhline(1.0, color=INK, linestyle="--", linewidth=1.1, label="full-space n_init=10")
    axes[0].set_title("Original-space SSE\nfrom projected labels")
    axes[0].set_ylabel("SSE / full-space baseline")
    axes[0].set_xlabel("projection dimension m")
    axes[0].set_xticks(x)
    axes[0].grid(alpha=0.18)
    axes[0].legend(frameon=False, loc="best")
    axes[1].set_title("JL pairwise distortion\n600 points → 179,700 pairs")
    axes[1].set_ylabel("absolute relative error")
    axes[1].set_xlabel("projection dimension m")
    axes[1].set_xticks(x)
    axes[1].grid(alpha=0.18)
    axes[1].legend(["p95", "median"], frameon=False, loc="best")
    axes[2].plot(x, [summary[str(m)]["projection_seconds"]["median"] for m in x], marker="o", color=ORANGE, linewidth=2, label="projection")
    axes[2].plot(x, [summary[str(m)]["clustering_seconds"]["median"] for m in x], marker="o", color=GREEN, linewidth=2, label="K-means")
    axes[2].set_title("Measured wall-clock time")
    axes[2].set_ylabel("seconds (median of 3 seeds)")
    axes[2].set_xlabel("projection dimension m")
    axes[2].set_xticks(x)
    axes[2].grid(alpha=0.18)
    axes[2].legend(frameon=False, loc="best")
    fig.suptitle("JL projection as a high-dimensional K-means diagnostic", color=ORANGE, fontsize=18, fontweight="bold", y=1.03)
    fig.text(0.5, -0.02, "Synthetic data · n = 600, d = 512, K = 5 · 3 projection seeds · K-means n_init = 10 · no global-optimum claim", ha="center", fontsize=10.0, color="#4E5B64")
    fig.tight_layout()
    paths = _save(fig, "04_jl_kmeans_high_dimensional")

    return {"figure": paths, "parameters": {"data_seed": data_seed, "n": n, "d": d, "n_clusters": n_clusters, "n_per_cluster": n_per, "center_radius": 8.0, "cluster_noise_std": 0.40, "projection_dimensions": dimensions, "projection_seeds": projection_seeds, "kmeans_seeds": kmeans_seeds, "projection": "Gaussian R entries N(0, 1/m)"}, "baseline": {"kmeans_n_init": 10, "kmeans_seed": 2718, "inertia": float(baseline.inertia_), "ari_vs_generating_labels": float(adjusted_rand_score(y_true, baseline.labels_)), "single_initialization_runs": baseline_single}, "runs": runs, "summary_by_m": summary, "notes": ["For each projected clustering, labels are used to recompute means in the original 512-D space before reporting original-space SSE.", "Pairwise distortion enumerates all 179,700 unordered sample pairs.", "Projection and K-means optimization seeds are recorded separately; timing is an observed run measurement, not a speed guarantee."]}


def main() -> None:
    _style()
    FIG_DIR.mkdir(parents=True, exist_ok=True)
    with threadpool_limits(limits=1):
        scale = run_scale_experiment()
        shapes = run_shape_experiment()
        image = run_image_experiment()
        jl = run_jl_experiment()
    results = {
        "metadata": {
            "generated_at_utc": datetime.now(timezone.utc).isoformat(),
            "script": str(Path(__file__).relative_to(ROOT)),
            "python": sys.version,
            "platform": platform.platform(),
            "numpy": np.__version__,
            "scikit_learn": sklearn.__version__,
            "scipy": scipy.__version__,
            "matplotlib": matplotlib.__version__,
            "threadpoolctl": threadpoolctl.__version__,
            "palette": {"orange": ORANGE, "green": GREEN, "gray_blue": GRAYBLUE},
            "threadpool_limit": 1,
            "reproducibility": "Run with /opt/anaconda3/bin/python3 and MPLCONFIGDIR=work/mplconfig.",
        },
        "figures": {"scale": scale["figure"], "shape_failure": shapes["figure"], "image_color_quantization": image["figure"], "jl": jl["figure"]},
        "scale_experiment": scale,
        "shape_failure_experiment": shapes,
        "image_color_quantization_experiment": image,
        "jl_experiment": jl,
    }
    RESULT_PATH.write_text(json.dumps(results, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({"results": str(RESULT_PATH), "figures": results["figures"], "image_metrics": image["metrics"], "jl_summary": jl["summary_by_m"]}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
