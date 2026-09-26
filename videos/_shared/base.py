"""Base Scene subclasses with the Bits of Chris defaults baked in."""
from __future__ import annotations

from dataclasses import dataclass

from manim import (
    DOWN,
    UP,
    FadeIn,
    FadeOut,
    Line,
    Rectangle,
    Scene,
    Text,
    ThreeDScene,
    VGroup,
    config,
    logger,
)

from videos._shared import style as S


def _caption_text(text: str, scale: float = S.CAPTION_SCALE) -> Text:
    t = Text(text, font=S.FONT, weight="MEDIUM").scale(scale)
    t.set_color(S.FG)
    return t


class _BocMixin:
    """Shared helpers. Composed into BocScene and Boc3DScene below."""

    def beat(self, kind: str = "BEAT") -> None:
        """Wait one of the three canonical durations: QUICK / BEAT / HOLD."""
        d = {"QUICK": S.QUICK, "BEAT": S.BEAT, "HOLD": S.HOLD}[kind]
        self.wait(d)

    def caption(self, text: str, fixed_in_frame: bool = False) -> Text:
        """Top-center caption. Returns the mobject; you fade it in/out yourself.

        For 3D scenes, pass fixed_in_frame=True so the caption ignores camera
        rotation. Boc3DScene.caption() does this automatically.
        """
        t = _caption_text(text).to_edge(UP)
        if fixed_in_frame:
            self.add_fixed_in_frame_mobjects(t)
            t.set_opacity(0)  # caller fades it in
        return t

    def show_caption(self, text: str, fixed_in_frame: bool = False) -> Text:
        """Caption + fade in. Returns the mobject so you can fade it out later."""
        t = self.caption(text, fixed_in_frame=fixed_in_frame)
        if fixed_in_frame:
            self.play(t.animate.set_opacity(1), run_time=S.QUICK)
        else:
            self.play(FadeIn(t), run_time=S.QUICK)
        return t

    def hide_caption(self, t: Text) -> None:
        self.play(FadeOut(t), run_time=S.QUICK)


class BocScene(_BocMixin, Scene):
    """2D scene with BG_DEEP background and FG default text."""

    def setup(self) -> None:
        config.background_color = S.BG_DEEP
        self.camera.background_color = S.BG_DEEP


class Boc3DScene(_BocMixin, ThreeDScene):
    """3D scene with BG_DEEP background and our default camera orientation."""

    def setup(self) -> None:
        config.background_color = S.BG_DEEP
        self.camera.background_color = S.BG_DEEP
        self.set_camera_orientation(phi=S.CAM_PHI, theta=S.CAM_THETA)

    def caption(self, text: str, fixed_in_frame: bool = True) -> Text:
        # 3D captions default to fixed-in-frame.
        return super().caption(text, fixed_in_frame=fixed_in_frame)

    def show_caption(self, text: str, fixed_in_frame: bool = True) -> Text:
        return super().show_caption(text, fixed_in_frame=fixed_in_frame)


# --- Shorts (9:16) ------------------------------------------------------------


@dataclass(frozen=True)
class SafeBounds:
    """Safe-area edges in scene units (origin at frame center)."""

    left: float
    right: float
    bottom: float
    top: float

    @property
    def width(self) -> float:
        return self.right - self.left

    @property
    def height(self) -> float:
        return self.top - self.bottom

    @property
    def center(self) -> tuple[float, float]:
        return ((self.left + self.right) / 2, (self.bottom + self.top) / 2)


def safe_bounds(
    frame_w: float = S.SHORT_FRAME_W,
    frame_h: float = S.SHORT_FRAME_H,
    top: float = S.SHORT_SAFE_TOP,
    bottom: float = S.SHORT_SAFE_BOTTOM,
    left: float = S.SHORT_SAFE_LEFT,
    right: float = S.SHORT_SAFE_RIGHT,
) -> SafeBounds:
    """The part of a Short not covered by the YouTube UI. Pure; unit-tested."""
    return SafeBounds(
        left=-frame_w / 2 + left * frame_w,
        right=frame_w / 2 - right * frame_w,
        bottom=-frame_h / 2 + bottom * frame_h,
        top=frame_h / 2 - top * frame_h,
    )


def caption_band(safe: SafeBounds) -> SafeBounds:
    """Lower third of the safe area: where Short captions live."""
    return SafeBounds(safe.left, safe.right, safe.bottom, safe.bottom + safe.height / 3)


def stage_bounds(safe: SafeBounds) -> SafeBounds:
    """Upper two thirds of the safe area: where the visual lives."""
    return SafeBounds(safe.left, safe.right, safe.bottom + safe.height / 3, safe.top)


def split_caption(text: str) -> list[str]:
    """Break a caption into two lines with the most even character counts.

    Used when a caption is wider than the safe area: two big lines beat one
    shrunken line on a phone. Single words stay on one line. Pure; tested.
    """
    words = text.split()
    if len(words) < 2:
        return [text]
    best = min(
        range(1, len(words)),
        key=lambda i: abs(len(" ".join(words[:i])) - len(" ".join(words[i:]))),
    )
    return [" ".join(words[:best]), " ".join(words[best:])]


def hold_remaining(now: float, t: float, frame_rate: float) -> float:
    """Seconds to wait so scene time reaches t. 0 if already there (< 1 frame)."""
    remaining = t - now
    return remaining if remaining >= 1.0 / frame_rate else 0.0


def _rect(b: SafeBounds) -> Rectangle:
    """Invisible layout rectangle: use with move_to / align_to / next_to."""
    r = Rectangle(width=b.width, height=b.height, stroke_opacity=0, fill_opacity=0)
    return r.move_to([*b.center, 0])


def short_caption(text: str) -> VGroup:
    """Caption mobject for a Short, already placed in the caption band.

    2 to 4 words. Too wide for the safe area -> two balanced lines; still too
    wide (one long word) -> shrinks to fit. A BG_DEEP stroke behind the
    glyphs keeps it legible over busy frames. Shared by BocShortScene.caption
    and tools/assemble.py (burned-in VO captions), so both land in the same
    place at the same size.
    """
    band = caption_band(safe_bounds())
    t = VGroup(_caption_text(text, scale=S.SHORT_CAPTION_SCALE))
    if t.width > band.width:
        t = VGroup(*[
            _caption_text(line, scale=S.SHORT_CAPTION_SCALE) for line in split_caption(text)
        ]).arrange(DOWN, buff=0.25)
    if t.width > band.width:
        t.scale_to_fit_width(band.width)
    t.set_stroke(S.BG_DEEP, width=10, background=True)
    return t.move_to([*band.center, 0])


class BocShortScene(BocScene):
    """9:16 YouTube Short: 1080x1920 at 30 fps, frame 9 x 16 units.

    Resolution is forced in __init__, not setup() or manim.cfg:
    - Scene.__init__ builds the camera and file writer from `config`, so
      setup() runs too late (the pixel buffer is already 16:9).
    - A manim.cfg would have to be copied into every video folder, and the
      -ql/-qm/-qh flags override its pixel size.
    So every render of a Short is 1080x1920@30 whatever -q flag you pass;
    it lands in media/videos/<file>/1920p30/.

    Layout helpers (all invisible Rectangles, never added to the scene):
      self.safe     area not covered by the YouTube UI
      self.stage    upper two thirds of safe: put the visual here
      self.band     lower third of safe: captions go here
    Backgrounds and big shapes may bleed past `safe` to fill the frame; text
    and the magenta hero must stay inside it.
    """

    def __init__(self, *args, **kwargs):
        config.pixel_width = S.SHORT_W
        config.pixel_height = S.SHORT_H
        config.frame_rate = S.SHORT_FPS
        config.frame_height = S.SHORT_FRAME_H
        config.frame_width = S.SHORT_FRAME_W
        super().__init__(*args, **kwargs)

    def setup(self) -> None:
        super().setup()
        self.safe_bounds = safe_bounds()
        self.safe = _rect(self.safe_bounds)
        self.stage = _rect(stage_bounds(self.safe_bounds))
        self.band = _rect(caption_band(self.safe_bounds))

    def caption(self, text: str, fixed_in_frame: bool = False) -> VGroup:
        """Big caption centered in the lower third of the safe area."""
        return short_caption(text)

    def hold_until(self, t: float) -> None:
        """Wait until scene time reaches t seconds (e.g. the beat's VO length).

        End every Short beat with hold_until(BEAT_SECONDS) so the render is
        exactly as long as its VO line. Warns if the scene already overran.
        """
        now = self.renderer.time
        if now > t + 1.0 / config.frame_rate:
            logger.warning(f"hold_until({t}): scene already at {now:.2f}s, over by {now - t:.2f}s")
        wait = hold_remaining(now, t, config.frame_rate)
        if wait:
            self.wait(wait)

    def show_guides(self) -> VGroup:
        """Debug overlay: dims the UI-covered zones and outlines stage/band.

        Call once at the top of construct() while laying out; delete before
        the final render.
        """
        fw, fh = config.frame_width, config.frame_height
        b = self.safe_bounds
        zones = [  # (left, right, bottom, top) in scene units
            (-fw / 2, fw / 2, b.top, fh / 2),              # top bar
            (-fw / 2, fw / 2, -fh / 2, b.bottom),          # bottom description
            (b.right, fw / 2, b.bottom, b.top),            # right action rail
            (-fw / 2, b.left, b.bottom, b.top),            # left gutter
        ]
        dims = VGroup(*[
            _rect(SafeBounds(*z)).set_fill(S.MUTED, opacity=S.OP_GHOST) for z in zones
        ])
        band_line = Line(
            [b.left, self.band.get_top()[1], 0], [b.right, self.band.get_top()[1], 0],
            color=S.FG_DIM, stroke_width=S.STROKE_AXIS,
        ).set_opacity(S.OP_AXIS)
        guides = VGroup(dims, band_line).set_z_index(100)
        self.add(guides)
        return guides
