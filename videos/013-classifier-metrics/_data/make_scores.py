"""Seeded synthetic scores for the classifier-metrics series.

10,000 requests to a prompt-injection detector: 50 attacks, 9,950 users.
Model A is built so that at threshold T_A exactly 40 attacks and 60 users
score above it (the ledger box: TP 40, FP 60, FN 10, TN 9,890). Model B
is sharper at the very top of its list but weaker in the tail, so its
PR-AUC is higher while its precision at 80% recall is lower (ep 5).

Run from this folder:  ../../../.venv/bin/python make_scores.py
Writes scores.npz (y, a, b) and ledger.json (every number the VO quotes).
"""
import json

import numpy as np
from sklearn.metrics import average_precision_score, roc_auc_score

SEED = 13
N_ATTACK, N_USER = 50, 9_950
T_A = 0.70


def model_a(rng):
    # users: 9,890 below T_A (a pile on the left with a tail), 60 above
    body = rng.beta(2.0, 7.0, size=40_000)
    body = body[body < T_A][: N_USER - 60]
    tail = rng.uniform(T_A + 0.005, 0.93, size=60)
    users = np.concatenate([body, tail])
    # attacks: 40 above T_A, 10 hiding in the user tail
    hi = rng.uniform(T_A + 0.005, 0.99, size=40)
    lo = rng.uniform(0.35, T_A - 0.005, size=10)
    attacks = np.concatenate([hi, lo])
    return attacks, users


def model_b(rng):
    # sharp top: 30 attacks above every user, then a long weak tail
    users = rng.beta(2.0, 7.0, size=N_USER) * 0.9
    top = rng.uniform(0.92, 0.99, size=30)
    rest = rng.uniform(0.05, 0.75, size=20)
    return np.concatenate([top, rest]), users


def counts(y, s, t):
    pred = s > t
    tp = int((pred & (y == 1)).sum()); fp = int((pred & (y == 0)).sum())
    fn = int((~pred & (y == 1)).sum()); tn = int((~pred & (y == 0)).sum())
    return dict(t=round(float(t), 3), tp=tp, fp=fp, fn=fn, tn=tn,
                recall=round(tp / (tp + fn), 3),
                precision=round(tp / max(tp + fp, 1), 3),
                fpr=round(fp / (fp + tn), 4))


def precision_at_recall(y, s, r):
    order = np.argsort(-s)
    hits = np.cumsum(y[order]); k = int(np.searchsorted(hits, r * y.sum())) + 1
    return round(float(hits[k - 1] / k), 3), k


def main():
    rng = np.random.default_rng(SEED)
    a_att, a_usr = model_a(rng)
    b_att, b_usr = model_b(rng)
    y = np.concatenate([np.ones(N_ATTACK), np.zeros(N_USER)]).astype(int)
    a = np.concatenate([a_att, a_usr]); b = np.concatenate([b_att, b_usr])
    np.savez("scores.npz", y=y, a=a, b=b)

    ledger = {
        "seed": SEED,
        "model_a_box": counts(y, a, T_A),
        "threshold_stops_a": [counts(y, a, t) for t in (0.2, 0.4, 0.55, T_A, 0.85)],
        "roc_auc": {"a": round(roc_auc_score(y, a), 3), "b": round(roc_auc_score(y, b), 3)},
        "pr_auc_ap": {"a": round(average_precision_score(y, a), 3),
                      "b": round(average_precision_score(y, b), 3)},
        "precision_at_recall_0.8": {"a": precision_at_recall(y, a, 0.8),
                                    "b": precision_at_recall(y, b, 0.8)},
        "prevalence": N_ATTACK / (N_ATTACK + N_USER),
    }
    with open("ledger.json", "w") as f:
        json.dump(ledger, f, indent=2)
    print(json.dumps(ledger, indent=2))


if __name__ == "__main__":
    main()
