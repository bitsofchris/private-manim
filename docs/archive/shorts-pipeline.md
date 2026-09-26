# Plan: co-generated Shorts pipeline

Status: complete (2026-09-26). Pilot shipped: videos/004-backprop-short/media/backprop_short.mp4. Process documented in docs/shorts-runbook.md.

## Evidence

Channel "The Augmented" (@BitsOfChris): 6.38K subs, 55 videos.

| Short | Views | Length |
|---|---|---|
| PyTorch Neural Networks Made Simple (Beginner Friendly) | 84K | 58 s |
| PyTorch in 60 Seconds: The 5 Parts of Every Neural Network | 2K | 49 s |
| My Second Brain All in One Organization System | 1.5K | |
| 6 Weeks Studying Neural Networks in 45 seconds | 1.3K | |
| Everything else (PKM, life lessons, AI prompts) | 70 to 600 | |

Signal: concrete ML fundamentals with code or a diagram on screen is the
lane. It outperforms the rest of the channel by 10x to 100x.

Existing repo pipeline (pickle-pirate-gemma): every render is 16:9, the
script was written after the clips existed, and there was no timing or
sync step. That is the gap to close.

## The process (audio first)

1. **Storyboard** `videos/<slug>/storyboard.md`: a beat table.
   `beat | seconds | VO line | what moves on screen | scene class`.
   Target 45 to 58 s, 5 to 8 beats, one idea per short, first frame
   already moving (no title card), last frame loops into the first.
2. **Record VO once**, before animating. Read the VO column in one pass
   into DaVinci or QuickTime. Rough take is fine for timing.
3. **Time it**: `whisper` word timestamps on the VO give each beat its
   real duration. Write those back into the storyboard.
4. **Generate scenes**: one file per beat, subclassing `BocShortScene`
   (9:16). Each scene takes its beat duration so the render matches the
   audio without editing.
5. **Assemble**: `assemble.py` concatenates beats in order, muxes the VO,
   burns large captions (1 to 4 words at a time, from the whisper
   timings), exports 1080x1920. DaVinci is for tweaks only.
6. **Review**: contact-sheet frames at phone size (the check used for the
   backprop GIFs), then a real watch on a phone.
7. **Re-record** the final VO against the animation if the rough take
   was off. Optional.

## Tooling to build (in order)

- [x] `BocShortScene` in `videos/_shared/base.py`: 1080x1920, frame
      width 9, safe-zone guide (top 12%, bottom 20%, right 12% are covered
      by the YouTube UI), larger type scales in `style.py`. Also
      `self.stage` / `self.band`, `hold_until(t)`, `show_guides()`.
- [x] `code_block(...)` helper: Manim `Code` mobject in house colors with a
      `highlight_lines(...)` animation. The 84K short is code on screen.
- [x] Beat library (004: hook net, neuron, tiny net, loss bowl `_bowl.py`, computational graph `_graph.py`):
      code block. Today's five backprop clips are the seed.
- [x] `tools/assemble.py`: ffmpeg concat + VO mux + burned captions
      (PNG overlays rendered by Manim; Homebrew ffmpeg has no libass/drawtext).
      Tests in `tests/test_assemble.py`.
- [x] `tools/review_frames.sh`: contact sheet at 360px wide.
- [x] Timing: MacWhisper CLI segment timestamps + `tools/tighten_vo.py` time map (word-level needs Pro; see runbook).

## Pilot

"Backprop in 60 seconds" from the Substack post. Reuse the five GIF
scenes re-laid-out for 9:16, one beat each, plus a 3 s hook beat.

## Rules of thumb (from what worked)

- Visual carries the idea; the voice narrates what is already moving.
- First second: something moving, no title card.
- One magenta hero per beat (house style already enforces this).
- Big text. Anything under ~40 px tall at 1080 wide is invisible on a phone.
- Captions burned in. Most Shorts are watched muted.
- End on a resting frame that matches the opening so the loop is clean.

## Study list

- 3Blue1Brown: script and VO first, animate to the audio. Watch how
  Grant holds a frame while a sentence lands.
- Karpathy micrograd lecture: pacing of "show code, then show what it does".
- Your own 84K short vs the 2K one: same topic, different hook and title.
  Pull both and compare the first 3 seconds side by side.
- Fireship for cut rhythm only (2 to 3 s per visual change), not tone.
