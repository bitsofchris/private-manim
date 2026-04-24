"""Precompute 2D PCA projections of positive/negative activation clouds.

Kept separate so Manim scenes don't repeat the work and stay deterministic.
"""

from __future__ import annotations

import numpy as np
from sklearn.decomposition import PCA

VECTORS_ROOT = "/Users/chris/repos/deep-learning/code/21_steering-harness/results/vectors"


def project(concept: str, layer: int = 21, scale: float = 80.0):
    """Return (pos_2d, neg_2d, pos_mean_2d, neg_mean_2d, var_explained).

    All 2D coords are scaled so ~95% of points fall within roughly [-2, 2]
    on each axis — convenient for Manim's default plane units.
    """
    d = np.load(f"{VECTORS_ROOT}/{concept}/layer_{layer:02d}.npz")
    pos = d["positive_acts"]
    neg = d["negative_acts"]
    X = np.vstack([pos, neg])
    mu = X.mean(axis=0)
    Xc = X - mu
    pca = PCA(n_components=2).fit(Xc)
    P = pca.transform(Xc)
    pos_2d = P[: len(pos)] / scale
    neg_2d = P[len(pos) :] / scale
    pos_mean_2d = pca.transform((d["positive_mean"] - mu).reshape(1, -1))[0] / scale
    neg_mean_2d = pca.transform((d["negative_mean"] - mu).reshape(1, -1))[0] / scale
    return pos_2d, neg_2d, pos_mean_2d, neg_mean_2d, pca.explained_variance_ratio_
