#!/usr/bin/env bash
# Render all 16 pickle-pirate scenes at the given quality (default -ql, fast).
# Usage:
#   bash videos/_shared/render_pickle_pirate.sh           # -ql (default, 480p15)
#   bash videos/_shared/render_pickle_pirate.sh -qm       # 720p30
#   bash videos/_shared/render_pickle_pirate.sh -qh       # 1080p60 (slow)
set -euo pipefail

QUALITY="${1:--ql}"

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "$REPO_ROOT/videos/pickle-pirate-gemma"

declare -a SCENES=(
  "01_steering_vector_addition.py:SteeringVectorAddition"
  "02_alpha_sweep_morph.py:AlphaSweepMorph"
  "03_pca_with_steering_arrow.py:PCAWithSteeringArrow"
  "04_concept_composition.py:ConceptComposition"
  "05_layer_sweep_landscape.py:LayerSweepLandscape"
  "06_cold_open.py:ColdOpen"
  "06b_third_way.py:ThirdWay"
  "07_setup.py:Setup"
  "08_closing.py:Closing"
  "blog01_concept_space.py:ConceptSpace"
  "blog01b_token_vs_concept.py:TokenVsConcept"
  "blog02_king_queen.py:KingQueen"
  "blog03_mean_diff.py:MeanDiff"
  "blog04_santa_cruz.py:SantaCruz"
  "blog05_superposition.py:Superposition"
  "blog06_pickle_ladder.py:PickleLadder"
  "blog07_composition.py:Composition"
)

failed=()
for pair in "${SCENES[@]}"; do
  file="${pair%:*}"
  cls="${pair#*:}"
  echo
  echo "=== Rendering $file :: $cls ($QUALITY) ==="
  if ! uv run manim "$QUALITY" "$file" "$cls"; then
    failed+=("$pair")
  fi
done

echo
if [ ${#failed[@]} -eq 0 ]; then
  echo "All ${#SCENES[@]} scenes rendered successfully."
else
  echo "FAILED (${#failed[@]}/${#SCENES[@]}): ${failed[*]}"
  exit 1
fi
