"""Transformer decoder block diagram in house style, parametric and reusable.

**Name:** transformer diagram
**Description:** The de facto visual grammar of AI architecture figures
(Figure 1 of "Attention Is All You Need", every Raschka diagram), redrawn
with our mobjects so a scene can light up one mark at a time. Bottom to top:
Embed -> [Attention -> (+) -> FFN -> (+)] with an N x bracket -> Linear head.
The (+) is the residual add (the paper's "Add & Norm"; labels at phone size
are too wide to say so on the figure, the VO does). Flow arrows are teal (tensors you can
see); every mark starts FG_DIM so the scene chooses the one magenta hero.
**When to use:** any Short or scene that reads, builds, or maps a transformer
block diagram (videos 006 "how to read it", 007 "how it maps to PyTorch").
**How it works:** `build_block(stage)` lays the column out to fit `stage`
(height from `stack_rows`, a pure function) and returns a `BlockDiagram`
VGroup whose named parts (`boxes`, `adds`, `flow`, `skips`, `bracket`,
`block`) are what a beat colors. `GPT_SOURCE` + `MARK_LINES` is the matching
PyTorch, kept here so the diagram and the code can never drift apart.
"""
from __future__ import annotations

from textwrap import dedent

from manim import (
    DOWN,
    LEFT,
    RIGHT,
    UP,
    Arrow,
    Brace,
    Circle,
    Line,
    Mobject,
    RoundedRectangle,
    Text,
    VGroup,
    VMobject,
)

from videos._shared import style as S

# Row order, bottom to top. "add" rows are the (+) nodes.
ROWS = ["embed", "attn", "add1", "ffn", "add2", "head"]
BOX_LABEL = {"embed": "Embed", "attn": "Attention", "ffn": "FFN", "head": "Linear"}
WIDEST_LABEL = "Attention"   # every box is sized to this so the column is uniform
REPEAT_LABEL = "N×"
BLOCK_ROWS = ("attn", "add1", "ffn", "add2")   # what the N× bracket spans

BOX_PAD = 0.12            # label-to-border padding inside a box
BOX_PAD_W = 0.3           # horizontal padding around the widest label
ADD_RADIUS = 0.34
SKIP_OFFSET = 0.7         # how far right of the column the skip path runs
BRACKET_BUFF = 0.15       # brace-to-block and label-to-brace spacing
EDGE_WIDTH = S.STROKE_AXIS * 3
ARROW_TIP = 0.28
MIN_GAP = 0.3             # smallest row gap we accept before the layout is too tall


def stack_rows(heights: list[float], bottom: float, top: float) -> list[float]:
    """Centres of rows stacked bottom->top with equal gaps filling [bottom, top].

    Pure; unit-tested. Raises if the rows do not fit with MIN_GAP between them.
    """
    if not heights:
        raise ValueError("no rows")
    span = top - bottom
    gaps = len(heights) - 1
    gap = (span - sum(heights)) / gaps if gaps else 0.0
    if gaps and gap < MIN_GAP:
        raise ValueError(f"rows need {sum(heights) + gaps * MIN_GAP:.2f}, have {span:.2f}")
    centres, y = [], bottom
    for h in heights:
        centres.append(y + h / 2)
        y += h + gap
    return centres


def label(text: str, color: str = S.FG) -> Text:
    return Text(text, font=S.FONT, weight="MEDIUM").scale(S.SHORT_LABEL_SCALE).set_color(color)


def op_box(text: str, width: float, height: float) -> VGroup:
    """One operation / layer: rounded panel with its name. `.box`, `.name`."""
    name = label(text)
    box = RoundedRectangle(
        corner_radius=0.2, width=width, height=height,
        fill_color=S.BG_PANEL, fill_opacity=1, stroke_color=S.FG_DIM, stroke_width=EDGE_WIDTH,
    )
    g = VGroup(box, name.move_to(box))
    g.box, g.name = box, name
    return g


def add_node() -> VGroup:
    """The (+) residual add. `.circle`, `.plus`."""
    circle = Circle(radius=ADD_RADIUS, color=S.FG_DIM, stroke_width=EDGE_WIDTH,
                    fill_color=S.BG_DEEP, fill_opacity=1)
    plus = VGroup(
        Line(LEFT * ADD_RADIUS * 0.55, RIGHT * ADD_RADIUS * 0.55),
        Line(DOWN * ADD_RADIUS * 0.55, UP * ADD_RADIUS * 0.55),
    ).set_stroke(S.FG_DIM, width=EDGE_WIDTH)
    g = VGroup(circle, plus)
    g.circle, g.plus = circle, plus
    return g


def flow_arrow(start, end) -> Arrow:
    """A tensor moving to the next op: teal, same shape on every main-line arrow."""
    return Arrow(start, end, color=S.DATA, stroke_width=EDGE_WIDTH, buff=0,
                 max_tip_length_to_length_ratio=1, tip_length=ARROW_TIP)


def skip_path(branch, into, x_out: float) -> VMobject:
    """Residual path: leaves the column at `branch`, runs up at `x_out`, enters
    the (+) at `into` from the right. Solid, FG_DIM, like the paper figure."""
    pts = [branch, [x_out, branch[1], 0], [x_out, into[1], 0], into]
    path = VMobject().set_points_as_corners(pts)
    return path.set_stroke(S.FG_DIM, width=EDGE_WIDTH)


class BlockDiagram(VGroup):
    """The whole column. Named parts a beat can recolor (one magenta hero each):

    boxes    VGroup of op_box (embed, attn, ffn, head)
    adds     VGroup of add_node (add1, add2)
    flow     VGroup of teal main-line arrows, bottom to top
    skips    VGroup of the two residual paths
    bracket  VGroup(Brace, "N×" label) on the left of the repeated block
    block    VGroup of everything the bracket spans (the repeated unit)
    rows     dict row name -> mobject
    """


def build_block(stage: Mobject) -> BlockDiagram:
    """Lay the diagram out to fill `stage` (an invisible layout Rectangle)."""
    ref = label(WIDEST_LABEL)
    width, height = ref.width + 2 * BOX_PAD_W, ref.height + 2 * BOX_PAD
    rows: dict[str, VGroup] = {}
    for r in ROWS:
        rows[r] = add_node() if r.startswith("add") else op_box(BOX_LABEL[r], width, height)
    ys = stack_rows([rows[r].height for r in ROWS], stage.get_bottom()[1], stage.get_top()[1])
    # Bracket on the left, skip path on the right; centre the whole width.
    bracket_w = BRACKET_BUFF * 2 + 0.25 + label(REPEAT_LABEL).width
    cx = stage.get_center()[0] + (bracket_w - SKIP_OFFSET) / 2
    for r, y in zip(ROWS, ys):
        rows[r].move_to([cx, y, 0])

    flow = VGroup(*[
        flow_arrow(rows[a].get_top(), rows[b].get_bottom()) for a, b in zip(ROWS, ROWS[1:])
    ])
    x_out = cx + width / 2 + SKIP_OFFSET
    skips = VGroup(
        skip_path(_mid(rows["embed"].get_top(), rows["attn"].get_bottom()),
                  rows["add1"].get_right(), x_out),
        skip_path(_mid(rows["add1"].get_top(), rows["ffn"].get_bottom()),
                  rows["add2"].get_right(), x_out),
    )
    block = VGroup(*[rows[r] for r in BLOCK_ROWS],
                   *flow[ROWS.index("attn"):ROWS.index("add2")], *skips)
    brace = Brace(VGroup(*[rows[r] for r in BLOCK_ROWS]), LEFT, buff=BRACKET_BUFF,
                  color=S.FG_DIM)
    bracket = VGroup(brace, label(REPEAT_LABEL, S.FG_DIM).next_to(brace, LEFT, buff=BRACKET_BUFF))

    d = BlockDiagram(flow, skips, *rows.values(), bracket)
    d.boxes = VGroup(*[rows[r] for r in ROWS if not r.startswith("add")])
    d.adds = VGroup(rows["add1"], rows["add2"])
    d.flow, d.skips, d.bracket, d.block, d.rows = flow, skips, bracket, block, rows
    return d


def _mid(a, b):
    return [(a[0] + b[0]) / 2, (a[1] + b[1]) / 2, 0]


# --- The matching PyTorch (video 007) -----------------------------------------
# Norms left out on purpose: the diagram shows (+), and every line here is a
# mark on the figure. ~21 lines, <= 40 columns.
GPT_SOURCE = dedent("""
    class Block(nn.Module):
        def __init__(self, d):
            self.attn = Attention(d)
            self.ffn = FeedForward(d)

        def forward(self, x):
            x = x + self.attn(x)
            x = x + self.ffn(x)
            return x

    class GPT(nn.Module):
        def __init__(self, d, n):
            self.embed = Embedding(d)
            self.blocks = [Block(d)] * n
            self.head = Linear(d, vocab)

        def forward(self, ids):
            x = self.embed(ids)
            for block in self.blocks:
                x = block(x)
            return self.head(x)
""").strip("\n")

# Diagram mark -> 1-based lines of GPT_SOURCE. The contract between the two.
MARK_LINES = {
    "box": [3, 4, 13, 14, 15],   # a box is a module built in __init__
    "arrow": [7, 8, 18, 21],     # an arrow is the order of calls in forward()
    "skip": [7, 8],              # the bypass arrow is the x that is added back
    "add": [7, 8],               # (+) is x = x + sublayer(x)
    "repeat": [19, 20],          # N× is the for loop over blocks
    "inset": list(range(1, 10)),  # the zoomed-in block is its own class
}
