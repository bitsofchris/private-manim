#!/usr/bin/env python3
"""Assemble a Short: concat beat renders, mux the VO, burn in captions.

Usage (from the repo root or anywhere):
    uv run --no-sync python tools/assemble.py videos/004-backprop-short/beats.json \\
        --vo videos/004-backprop-short/vo.m4a \\
        --captions videos/004-backprop-short/captions.json \\
        -o videos/004-backprop-short/media/short.mp4
    # --dry-run prints the ffmpeg command instead of running it.

beats.json (paths relative to the json file):
    {"beats": [
        {"clip": "media/videos/01_hook/1920p30/Hook.mp4", "start": 0, "end": 4.0},
        {"clip": "media/videos/02_neuron/1920p30/Neuron.mp4", "end": 7.0}
    ]}
    `start` defaults to 0. `end` is required: the beat's VO length is the
    contract (audio-first), so it is written down, never inferred.

captions.json (seconds on the final, assembled timeline):
    [{"start": 0.0, "end": 1.1, "text": "neural network"}, ...]
    Sorted, non-overlapping, 1 to 4 words each.

Captions are rendered to transparent 1080x1920 PNGs with Manim's own text
engine (Pango, S.FONT, same size and band as BocShortScene.caption) and
overlaid with ffmpeg's `overlay` filter. Why not ASS/drawtext: Homebrew's
ffmpeg is built without libass and freetype, so neither `subtitles` nor
`drawtext` exists; PNG overlays also guarantee burned captions look exactly
like in-scene captions.

Pure logic (parsing, validation, command construction) is stdlib-only and
unit-tested in tests/test_assemble.py. Only render_caption_pngs imports Manim.
"""
from __future__ import annotations

import argparse
import json
import shlex
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]

WIDTH, HEIGHT, FPS = 1080, 1920, 30  # mirrors S.SHORT_W / SHORT_H / SHORT_FPS
MAX_CAPTION_WORDS = 4


@dataclass(frozen=True)
class Beat:
    clip: Path
    start: float
    end: float

    @property
    def duration(self) -> float:
        return self.end - self.start


@dataclass(frozen=True)
class Caption:
    start: float
    end: float
    text: str


# --- parsing ------------------------------------------------------------------


def parse_beats(data: dict, base_dir: Path) -> list[Beat]:
    """beats.json dict -> Beats with clip paths resolved against base_dir."""
    if not isinstance(data, dict) or not isinstance(data.get("beats"), list):
        raise ValueError('beats.json must be an object with a "beats" list')
    if not data["beats"]:
        raise ValueError("beats list is empty")
    beats = []
    for i, b in enumerate(data["beats"]):
        if "clip" not in b or "end" not in b:
            raise ValueError(f"beat {i}: needs 'clip' and 'end'")
        start, end = float(b.get("start", 0.0)), float(b["end"])
        if start < 0 or end <= start:
            raise ValueError(f"beat {i}: need 0 <= start < end, got {start}..{end}")
        beats.append(Beat(clip=(base_dir / b["clip"]).resolve(), start=start, end=end))
    return beats


def parse_captions(data: list, total: float | None = None) -> list[Caption]:
    """captions.json list -> Captions. Enforces sorted, non-overlapping, short."""
    if not isinstance(data, list):
        raise ValueError("captions.json must be a list")
    caps = []
    for i, c in enumerate(data):
        text = str(c.get("text", "")).strip()
        start, end = float(c["start"]), float(c["end"])
        if not text:
            raise ValueError(f"caption {i}: empty text")
        if len(text.split()) > MAX_CAPTION_WORDS:
            raise ValueError(f"caption {i}: {text!r} is over {MAX_CAPTION_WORDS} words")
        if start < 0 or end <= start:
            raise ValueError(f"caption {i}: need 0 <= start < end, got {start}..{end}")
        if caps and start < caps[-1].end:
            raise ValueError(f"caption {i}: starts at {start} before previous ends ({caps[-1].end})")
        if total is not None and end > total + 1e-6:
            raise ValueError(f"caption {i}: ends at {end}, after the video ({total:.2f}s)")
        caps.append(Caption(start, end, text))
    return caps


def total_duration(beats: list[Beat]) -> float:
    return sum(b.duration for b in beats)


# --- ffmpeg command -------------------------------------------------------------


def _num(x: float) -> str:
    """Compact, exact-enough number for filter args (no 1e-05 notation)."""
    return f"{x:.3f}".rstrip("0").rstrip(".") or "0"


def build_filter(beats: list[Beat], captions: list[Caption], first_png_input: int) -> str:
    """filter_complex: trim+normalize each beat, concat, overlay caption PNGs."""
    parts = []
    for i, b in enumerate(beats):
        parts.append(
            f"[{i}:v]trim=start={_num(b.start)}:end={_num(b.end)},setpts=PTS-STARTPTS,"
            f"fps={FPS},scale={WIDTH}:{HEIGHT},setsar=1,format=yuv420p[v{i}]"
        )
    labels = "".join(f"[v{i}]" for i in range(len(beats)))
    parts.append(f"{labels}concat=n={len(beats)}:v=1:a=0[base]")
    prev = "base"
    for k, c in enumerate(captions):
        out = f"c{k}"
        parts.append(
            f"[{prev}][{first_png_input + k}:v]overlay=0:0:"
            f"enable='between(t,{_num(c.start)},{_num(c.end)})'[{out}]"
        )
        prev = out
    parts.append(f"[{prev}]format=yuv420p[vout]")
    return ";".join(parts)


def build_ffmpeg_cmd(
    beats: list[Beat],
    out: Path,
    vo: Path | None = None,
    captions: list[Caption] | None = None,
    caption_pngs: list[Path] | None = None,
) -> list[str]:
    """Full ffmpeg argv. Input order: beat clips, then VO, then caption PNGs."""
    captions = captions or []
    caption_pngs = caption_pngs or []
    if len(captions) != len(caption_pngs):
        raise ValueError("need exactly one PNG per caption")
    cmd = ["ffmpeg", "-y", "-hide_banner", "-loglevel", "error"]
    for b in beats:
        cmd += ["-i", str(b.clip)]
    vo_index = len(beats) if vo else None
    if vo:
        cmd += ["-i", str(vo)]
    first_png = len(beats) + (1 if vo else 0)
    for p in caption_pngs:
        cmd += ["-i", str(p)]
    cmd += ["-filter_complex", build_filter(beats, captions, first_png), "-map", "[vout]"]
    if vo_index is not None:
        cmd += ["-map", f"{vo_index}:a", "-c:a", "aac", "-b:a", "192k"]
    else:
        cmd += ["-an"]
    cmd += [
        "-c:v", "libx264", "-preset", "medium", "-crf", "18", "-pix_fmt", "yuv420p",
        "-r", str(FPS), "-t", _num(total_duration(beats)), "-movflags", "+faststart",
        str(out),
    ]
    return cmd


# --- side effects ---------------------------------------------------------------


def probe_duration(path: Path) -> float:
    r = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(path)],
        capture_output=True, text=True, check=True,
    )
    return float(r.stdout.strip())


def render_caption_pngs(captions: list[Caption], out_dir: Path) -> list[Path]:
    """Rasterize each caption to a transparent full-frame PNG via Manim/Pango."""
    sys.path.insert(0, str(REPO))
    from manim import Camera, config, logger  # noqa: PLC0415 - heavy, only when rendering

    from videos._shared import style as S  # noqa: PLC0415
    from videos._shared.base import short_caption  # noqa: PLC0415

    logger.setLevel("ERROR")  # "font not found" dumps every system font name
    config.pixel_width, config.pixel_height = S.SHORT_W, S.SHORT_H
    config.frame_height, config.frame_width = S.SHORT_FRAME_H, S.SHORT_FRAME_W
    out_dir.mkdir(parents=True, exist_ok=True)
    paths = []
    for k, c in enumerate(captions):
        cam = Camera(background_opacity=0)
        cam.capture_mobject(short_caption(c.text))
        p = out_dir / f"caption_{k:03d}.png"
        cam.get_image().save(p)
        paths.append(p)
    return paths


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("beats", type=Path, help="beats.json")
    ap.add_argument("--vo", type=Path, help="voice-over audio file")
    ap.add_argument("--captions", type=Path, help="captions.json")
    ap.add_argument("-o", "--out", type=Path, required=True, help="output .mp4")
    ap.add_argument("--dry-run", action="store_true", help="print the ffmpeg command only")
    args = ap.parse_args(argv)

    beats = parse_beats(json.loads(args.beats.read_text()), args.beats.parent)
    total = total_duration(beats)
    for b in beats:
        if not b.clip.exists():
            raise SystemExit(f"missing clip: {b.clip}")
    captions = parse_captions(json.loads(args.captions.read_text()), total) if args.captions else []

    if args.vo:
        vo_len = probe_duration(args.vo)
        if abs(vo_len - total) > 0.25:
            print(f"warning: VO is {vo_len:.2f}s but beats sum to {total:.2f}s", file=sys.stderr)

    png_dir = args.out.parent / f".{args.out.stem}_captions"
    pngs = [png_dir / f"caption_{k:03d}.png" for k in range(len(captions))]
    cmd = build_ffmpeg_cmd(beats, args.out, args.vo, captions, pngs)
    if args.dry_run:
        print(shlex.join(cmd))
        return 0
    if captions:
        render_caption_pngs(captions, png_dir)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(cmd, check=True)
    print(f"{args.out}  ({total:.2f}s, {len(beats)} beats, {len(captions)} captions)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
