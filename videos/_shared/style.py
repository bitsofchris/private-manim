"""Bits of Chris palette + type + motion constants. Single source of truth."""
from __future__ import annotations

from manim import DEGREES

# Palette - sampled from the bitsofchris cover (teal -> indigo -> magenta).
# Two heroes: TEAL is the data you can see, MAGENTA is the structure you reach in for.
BG_DEEP = "#0B0B14"
BG_PANEL = "#14142B"

FG = "#ECEBE4"
FG_DIM = "#8A8FB0"

HERO_TEAL = "#2DD4BF"
HERO_MAGENTA = "#C084FC"

ACCENT_CYAN = "#67E8F9"
ACCENT_PINK = "#F0ABFC"

GRID = "#1F2440"
MUTED = "#4A5070"

# Semantic aliases - prefer these in scene code.
DATA = HERO_TEAL          # the cloud, the observed
STRUCTURE = HERO_MAGENTA  # the discovered direction, PC1, manifold axis
SHADOW = MUTED            # projections, residuals, secondary geometry
HIGHLIGHT = ACCENT_CYAN   # transient sweep / pulse
CALLOUT = ACCENT_PINK     # transient hot annotation

# Typography. Pango falls back gracefully if Inter is not installed; install
# Inter system-wide for the canonical look. Math uses LaTeX defaults.
FONT = "Inter"

CAPTION_SIZE = 36
LABEL_SIZE = 24
MATH_SM = 28
MATH_LG = 44

CAPTION_SCALE = 0.6   # for Text().scale(...) calls in 1080p
LABEL_SCALE = 0.45
TAG_SCALE = 0.45

# Monospace for code blocks. Menlo ships with macOS; Pango falls back otherwise.
FONT_MONO = "Menlo"

# Motion. Three durations. Don't invent new ones.
QUICK = 0.3
BEAT = 0.6
HOLD = 1.2

# Stroke widths.
STROKE_DATA = 0.0           # dots have no stroke
STROKE_STRUCTURE = 5.0      # the hero direction reads thick
STROKE_AXIS = 1.5
STROKE_RESIDUAL = 1.5

# Dot radii.
DOT_DATA = 0.045
DOT_DATA_3D = 0.05
DOT_HERO = 0.06
DOT_GIF = 0.14  # small-format looping GIFs (legible at 640px wide)

# Default opacities.
OP_DATA = 0.85
OP_AXIS = 0.35
OP_GRID = 0.35
OP_GHOST = 0.25  # for ghosted/faded prior states

# 3D camera defaults.
CAM_PHI = 70 * DEGREES
CAM_THETA = -45 * DEGREES
CAM_AMBIENT_RATE = 0.12

# --- Short format (YouTube Shorts, 9:16) -------------------------------------
# Used by BocShortScene. 1 scene unit = SHORT_W / SHORT_FRAME_W = 120 px.
SHORT_W = 1080
SHORT_H = 1920
SHORT_FPS = 30
SHORT_FRAME_W = 9.0
SHORT_FRAME_H = 16.0

# Fractions of the frame covered by the YouTube Shorts UI (title/search bar on
# top, channel name + description at the bottom, like/comment rail on the
# right). Text and the hero must stay inside; backgrounds may bleed through.
SHORT_SAFE_TOP = 0.12
SHORT_SAFE_BOTTOM = 0.20
SHORT_SAFE_RIGHT = 0.12
SHORT_SAFE_LEFT = 0.06   # ~65 px gutter; safe-zone guides put 60 px on the left

# Readable on a phone means text at least ~1/20 of frame height (96 px).
# Scales are for Text(font=S.FONT) at default font_size, measured at 1920 px:
#   caption 1.8 -> capital letters 104 px, full line (with descenders) 135 px
#   label   1.3 -> capital letters  75 px, full line  98 px (the floor)
SHORT_CAPTION_SCALE = 1.3   # ~72 px caps (top of the 48-70 px guidance); 3-word captions fit one line
SHORT_LABEL_SCALE = 1.3     # labels next to the thing they name
SHORT_CODE_FONT_SIZE = 30   # code_block() in a short: ~27 monospace columns fit the safe width
DOT_SHORT = 0.22            # data dot radius in a short (~50 px across)

# Reproducibility default.
SEED = 7

# Content-coded colors. Use ONLY when a scene has categorical semantic meaning
# (pickle vs other-food, three named steering vectors, etc.). For "data" and
# "discovered structure" use S.DATA / S.STRUCTURE instead. Pull these from
# style.py so the same concept reads the same color across every scene.
CONTENT_PICKLE = "#34D399"   # green - "pickle" cluster / pickle direction
CONTENT_OTHER = "#FB923C"    # orange - "other-food" cluster
CONTENT_PIRATE = "#A16207"   # warm brown - pirate steering vector
CONTENT_GOLD = "#E0B040"     # gold - "Golden Gate" callback
CONTENT_RUST = "#C2410C"     # rust - tertiary categorical accent
