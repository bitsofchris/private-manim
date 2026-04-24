## 10 visuals worth building

Each one is a single Manim scene. Ordered from simplest intuition → deepest. Pick 4–6 for a first pass.

### 1. The rotation intuition (2D)
Scatter of ~200 correlated points. Overlay the original `x,y` axes (gray). Fit PCA, animate the axes rotating to land on PC1 (max spread) and PC2 (orthogonal). Then rotate the entire point cloud so PC1 becomes horizontal.
- **Teaches:** PCA is a rotation of the coordinate system.
- **Key manim:** `Axes`, `Dot`, `VGroup`, `Rotate`, `ApplyMatrix`, `always_redraw`.

### 2. Projection + residuals
Same 2D cloud. Draw PC1 as an infinite line. For each point drop a dashed perpendicular onto PC1 and mark the projected foot. Sweep the candidate line through angles and show the sum-of-squared-residuals shrinking to a minimum at PC1.
- **Teaches:** PCA = line that minimizes perpendicular distances ≡ maximizes variance along.
- **Key manim:** `Line`, `DashedLine`, `ValueTracker`, `always_redraw`, `DecimalNumber`, `Rotate`.

### 3. Variance-explained bar chart, synced
Right half of the frame: a `BarChart` showing `explained_variance_ratio_`. Left half: the rotating axes from scene 1. As each PC lands, the corresponding bar fills.
- **Teaches:** PCs are ranked; first few capture most of the story.
- **Key manim:** `BarChart`, `AnimationGroup`, `LaggedStart`.

### 4. 3D cloud → camera rotates along PC1 (you already have this)
Real embeddings or synthetic 3-cluster blob. `Dot3D` per point colored by label. Camera rotates. Add a glowing `Arrow3D` pointing along PC1.
- **Teaches:** 3D cluster structure emerges under rotation; PC1 is a narrated direction.
- **Key manim:** `ThreeDScene`, `ThreeDAxes`, `Dot3D`, `set_camera_orientation`, `begin_ambient_camera_rotation`, `Arrow3D`.

### 5. Ellipsoid fit (the "shape" of the data)
3D cloud, then fade in a translucent ellipsoid whose axes = PCs scaled by √eigenvalue. Visually: the ellipsoid IS the covariance.
- **Teaches:** PCA = eigen-decomposition of covariance; the shape of the data is an ellipsoid.
- **Key manim:** `Surface` (parametric `(cos u sin v, sin u sin v, cos v)` scaled + rotated by eigenvectors), `ApplyMatrix`.

### 6. Linear transform = one NN layer
Grid of points under the unit square. Apply `W = eigenvector matrix` via `ApplyMatrix` → grid rotates. Then apply a diagonal scale (eigenvalues) → grid stretches. Caption: "X · W = one dense layer, no activation."
- **Teaches:** PCA as a matrix multiplication; ties to NN mental model.
- **Key manim:** `NumberPlane`, `ApplyMatrix`, `MathTex`.

### 7. Delta vectors → gender axis (the debiasing visual)
Scatter of word embeddings projected to 2D. Draw arrows between `(king→queen)`, `(man→woman)`, `(actor→actress)`. They're roughly parallel. Collect the tails at origin, run PCA on the difference set, reveal PC1 as the gender axis. Fade original cloud; keep the axis.
- **Teaches:** Contrastive / delta-vector trick; why PCA on differences beats PCA on raw embeddings.
- **Key manim:** `Arrow`, `VGroup.animate.shift`, `Transform`, `MathTex`.

### 8. Swiss roll — where PCA breaks
Parametric swiss roll surface with colored points along it. Run PCA → best-fit plane cuts *through* the roll, colors mix. Then run a stylized "unroll" (parameterize by intrinsic coord `u`) → colors separate cleanly.
- **Teaches:** PCA is linear; curved manifolds need nonlinear methods (UMAP / Isomap / autoencoder).
- **Key manim:** `Surface` (parametric), `VMobject.apply_function`, `Transform` from 3D points to their `u` coord on a 1D line.

### 9. Manifold in ambient space (the "thin cone")
Gray dust cloud filling a 3D cube = ambient space. A colored ribbon/curve winding through it = the manifold. Camera zooms. Non-manifold gray points fade out. Caption: "a random point in a 200k-D face space is not a face."
- **Teaches:** Why ambient dim ≫ intrinsic dim; open question from your manifold note made visual.
- **Key manim:** `Dot3D` (opacity tween), `ParametricFunction`, `move_camera`, `FadeOut(lag_ratio=...)`.

### 10. Projection as shadow (3D → 2D)
3D cluster with a light source. Drop a 2D "shadow" onto the PC1–PC2 plane. Rotate the data; watch the shadow change. Then rotate to align with PCs — the shadow becomes maximally spread.
- **Teaches:** Dimensionality reduction = choosing the best shadow.
- **Key manim:** `Dot3D` + companion `Dot` at `(x,y,0)`, `DashedLine` between them, `Rotate`.
