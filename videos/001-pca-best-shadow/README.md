# 001 - PCA: The Best Shadow

60-second explainer short. One idea: **PCA is the best shadow your data can cast.**

Source: [`ideas.md`](../../ideas.md) section "PCA Short - The Best Shadow."

## Scenes

| File | Class | Beat | Duration |
| --- | --- | --- | --- |
| `shadow_3d.py` | `BestShadow` | Hook + magic (3D cloud, shadow on floor, PC-align) | 0-20s |
| `rotation_2d.py` | _(todo)_ | Clarify (2D scatter, axes rotate to PC1/PC2) | 20-45s |
| `swiss_roll.py` | _(todo)_ | Stakes (flat PCA plane slices a swiss roll) | 45-60s |

## Render

```
manim -pql videos/001-pca-best-shadow/shadow_3d.py BestShadow
```

`-pql` = preview + low quality (fast iteration). Swap to `-pqh` for 1080p when shipping.
