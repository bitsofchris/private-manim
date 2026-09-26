# Shorts runbook: co-generated explainer Shorts

**Name:** shorts-runbook
**Description:** The end-to-end process for turning a written post into a
sub-60-second 9:16 YouTube Short where Chris records the voice once and
Claude generates every visual in Manim. Covers the research the standards
came from, the tools, the step order, and the checks that catch problems
before a human has to.
**When to use:** any time a post or lecture note is done and you want a
Short from it. Also the reference for "why is this constant this value".
**How it works:** audio first. The voice sets the clock; every scene is
rendered to the exact length of its VO window; captions are burned in from
the transcript. Below, in order.

Proven on `videos/004-backprop-short/` (2026-09-26): 120 s raw take →
59.8 s finished Short in one session, no re-record.

---

## 0. Why this shape (the research)

Two inputs decided the format. Both are written up in more detail in
`videos/_shared/ANIMATION_RULES.md` and `docs/plans/shorts-pipeline.md`.

**The channel's own data.** Comparing the 84K-view Short (PyTorch Neural
Networks Made Simple) with a 2K-view Short on the same topic:

| | 84K | 2K |
|---|---|---|
| First frame | zoomed code, bright, moving | near-black, tiny floating window |
| Captions | big, burned in, 2–3 words per beat | none |
| Frame fill | edge to edge | ~45 % black |
| Hook | weak spoken, strong visual | strong spoken, weak visual |

Lesson: what is *visible* in frame 0 and readable while muted decides
retention. Craft, with luck on top.

**Explanatory-animation research** (Tversky congruence/apprehension, Mayer's
multimedia principles, Heer & Robertson on animated transitions, Grant
Sanderson and Kurzgesagt on process). The rules that changed how we build:

- Animate a change only when the narration names it. Otherwise nothing moves.
- One kind of change per `play`. Moves the viewer must track get ≥ 1 s.
- A mobject that stands for a thing keeps its identity: `Transform` it,
  never fade-swap it for a lookalike.
- Make the visual change land on the word that names it.
- Never put the narration on screen. Captions are 2–4 key words.

**YouTube Shorts UI safe zones** (multiple 2026 sources, values vary; we
took the conservative envelope): top 120–380 px, bottom 300–380 px,
right ~120 px, left ~60 px on a 1080×1920 frame. Caption guidance: 2–5
words, 48–70 px, err larger. Ours (in `style.py`):

| Constant | Value | Pixels |
|---|---|---|
| `SHORT_SAFE_TOP` | 0.12 | 230 |
| `SHORT_SAFE_BOTTOM` | 0.20 | 384 |
| `SHORT_SAFE_RIGHT` | 0.12 | 130 |
| `SHORT_SAFE_LEFT` | 0.06 | 65 |
| `SHORT_CAPTION_SCALE` | 1.3 | ~72 px caps; 3-word captions fit one line |
| `SHORT_LABEL_SCALE` | 1.3 | ~1/20 of frame height, the phone-legible floor |

Verified by compositing rendered captions over a real frame with the dead
zones shaded (see step 7).

---

## 1. Storyboard from the post (Claude, 5 min)

- Pick the 5–8 concepts the post already animates in your head. One idea
  per Short.
- Write `videos/NNN-slug/storyboard.md`: a table `beat | VO | visual`.
- **VO uses the author's own sentences.** Cut and reorder; never reword.
  Target 130–150 spoken words for ~55 s.
- The visual column maps each beat to a reusable element (neuron, tiny
  net, loss bowl, computational graph, code block). Reuse across posts.

## 2. Record once (Chris, 3 min)

- QuickTime Player → New Audio Recording → Maximum quality, good mic.
- Read the script in one pass. Pause ~1 s between beats. Flub? Pause and
  re-read the sentence; the cut step handles it.
- Save as `vo_raw.m4a` in the video folder. Do not re-record for length.

## 3. Clean the audio (Claude, 10 s)

```
tools/enhance_vo.sh vo_raw.m4a vo_clean.wav
```

High-pass 80 Hz → FFT denoise → de-ess → 3:1 compressor → loudnorm to
−14 LUFS / −1.5 dBTP (YouTube's target). Covers ~90 % of what Descript's
Studio Sound does; it will not remove reverb or a barking dog.

## 4. Transcribe (Claude, 30 s)

MacWhisper ships a CLI. No install needed:

```
MW=/Applications/MacWhisper.app/Contents/MacOS/mw
$MW transcribe --model whisper-cpp:ggml-model-whisper-small --language en \
   --no-speakers --format txt --timestamps --end-timestamps --milliseconds \
   -o transcript.txt vo_clean.wav
```

Gotchas:
- It will **not overwrite** an existing `-o` file and fails silently with
  `2>/dev/null`. `rm` the old file first.
- Word-level timestamps and JSON need MacWhisper Pro. Segment-level is
  enough for cutting; sub-clip transcription (step 5) refines boundaries.

## 5. Tighten (Claude + Chris, the only judgment step)

1. Read the transcript. Mark: flubs, repeated ideas, clauses that don't
   earn their seconds. Propose whole-phrase cuts with per-beat second
   counts. **Chris approves the cut list.** Under 60 s is the constraint.
2. Find cut boundaries:
   - `ffmpeg silencedetect` (`-35dB`, `d=0.45`) gives the pause map.
   - A cut that falls mid-phrase: extract the 2–5 s region, transcribe
     just that clip (`mw` on the sub-clip gives finer segments), and run
     silencedetect at `-40dB d=0.04` for micro-pauses.
3. Apply:

```
tools/tighten_vo.py vo_clean.wav --out vo_final.wav --map timemap.json \
    --max-gap 0.25 --remove 22.8-26.45 --remove 41.2-43.8 ...
```

   Drops the ranges, pads each kept piece 80 ms, caps every pause, 8 ms
   fades at each join, writes an old→new time map.
4. **Verify by re-transcribing `vo_final.wav`.** Fragments show up as odd
   words ("'cause we then", "with work", "or that"). Nudge the boundary
   50–200 ms and repeat. Expect 2–3 rounds.
5. Still over? `atempo=1.03` is inaudible and buys 3 %. Re-run loudnorm
   after it.

Then rewrite `storyboard.md` with the final beat table: master start,
length, scene file, VO. Beat lengths are the contract for step 6.

## 6. Generate the beats (Claude, parallel agents, ~10 min)

- One scene file per beat, `BocShortScene`, ending in
  `self.hold_until(DURATION)` so the render is exactly the VO window.
- Give each agent: its beat's VO text with scene-local second cues, the
  visual brief, the audio-first contract, and "no in-scene captions, no
  edits under `_shared/`". Group beats that share a visual (bowl, graph)
  onto one agent with a local `_bowl.py` / `_graph.py` module.
- Agents should place cues from the audio itself (silencedetect + energy
  envelope), not only from the brief; that beat the estimates every time.
- Render: `cd videos/NNN-slug && uv run --no-sync manim -qh 0N_beat.py Class`.
  Output: `media/videos/0N_beat/1920p30/Class.mp4`.

Known Manim 0.18.1 traps (details in `videos/_shared/STYLE.md`): negative
`z_index` hides a mobject while it animates; `LaggedStart` over `Create`
of children already in the scene draws nothing; `FadeIn` in the same
`play` as `TransformFromCopy` can stack above it; `set_opacity` on a
stroke-only VMobject fills it. No LaTeX on this machine: `Text` only.

## 7. Captions and assembly (Claude, 1 min)

```
tools/captions_from_transcript.py transcript_final.txt captions.json   # ≤3 words each
# beats.json: ordered {clip, end} per beat; ends must sum to the VO length
tools/assemble.py beats.json --vo vo_final.wav --captions captions.json \
    -o media/short.mp4
```

Captions are rasterized by Manim (same font, size and band as in-scene
captions) and overlaid with ffmpeg, because Homebrew ffmpeg lacks libass
and drawtext. One caption source per Short: burned from the VO, never
also drawn in scenes.

## 8. Review (Claude, then Chris)

- `tools/review_frames.sh media/short.mp4` for contact sheets; or three
  20 s sheets at 300 px wide, one frame every 2 s, which shows the whole
  Short on one screen each.
- Check at that size: text legible, nothing in the dead zones, one magenta
  hero per beat, first frame moving, last frame still and clean, captions
  never two lines for more than a beat.
- Dead-zone proof: overlay a caption PNG on a real frame and `drawbox`
  the four zones at 25 % red. If text touches red, fix the constant.
- Chris: watch it on a phone with sound, then muted. Listen once at the
  splice points.

## 9. Publish (Chris, 2 min)

The channel's own evidence: the 84K Short is titled in plain words a
beginner would search ("... Made Simple (Beginner Friendly)"); the 2K
Short on the same topic led with a gimmick ("in 60 Seconds: The 5 Parts").
General guidance agrees: keyword in the first 30–40 characters, title
under ~50 so the feed doesn't truncate it, first 100 characters of the
description carry the takeaway, 3–5 hashtags at the end, tags barely matter.

**The rule:** *Say the concept in plain words a beginner would type, then
promise it's simple.* One idea, no clever hook in the title; the visual
is the hook.

- Title: `<Concept> Made Simple (Beginner Friendly)` or
  `How <thing> works: <Concept> Made Simple`. ≤ 50 characters.
- Description: line 1 is the one-sentence takeaway (≤ 100 chars). Then
  2–3 lines saying what's shown, in order. Then the post link. Then the
  channel sign-off. Then 3–5 hashtags.
- Pinned comment: the post link plus one question that invites a reply.
- Per-video copy lives in `videos/NNN-slug/publish.md`.

---

## Tools (all under `tools/`, tests under `tests/`)

| Tool | Does | Tested |
|---|---|---|
| `enhance_vo.sh` | ffmpeg voice cleanup chain to −14 LUFS | manual |
| `tighten_vo.py` | range cuts, pause capping, time map | yes |
| `captions_from_transcript.py` | MacWhisper txt → captions.json | yes |
| `assemble.py` | concat beats, mux VO, burn captions | yes |
| `review_frames.sh` | contact sheets at phone size | manual |
| `videos/_shared/to_gif.sh` | mp4 → email-safe looping GIF (blog embeds) | manual |

Run everything: `uv run --no-sync python -m unittest discover -s tests`.

## What we'd change next time

- Get word-level timestamps (MacWhisper Pro, or a one-off `mlx-whisper`
  run) so captions break at phrase boundaries instead of every 3 words,
  and so cut boundaries need fewer rounds.
- Install Inter (`brew install --cask font-inter`); Pango is falling back.
- Consider `S.BEAT` = 0.9 s for Shorts (research says ~1 s for tracked
  motion; 0.6 s reads as a flicker at phone size).
- A hook beat that also states the title on screen over the moving visual
  is the one thing the 84K Short does that ours doesn't yet.
