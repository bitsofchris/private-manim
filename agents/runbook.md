# Shorts runbook: co-generated explainer Shorts

**Name:** shorts-runbook
**Description:** The end-to-end process for turning a written post into a
sub-60-second 9:16 YouTube Short where Chris records the voice once and
Claude generates every visual, in Manim or HyperFrames (`AGENTS.md`,
"Which engine"). Covers the research the standards
came from, the tools, the step order, and the checks that catch problems
before a human has to.
**When to use:** any time a post or lecture note is done and you want a
Short from it. Also the reference for "why is this constant this value".
**How it works:** audio first. The voice sets the clock; every scene is
rendered to the exact length of its VO window; captions are burned in from
the transcript. Below, in order.

Proven on `videos/004-backprop-short/` (2026-09-26): 120 s raw take →
59.8 s finished Short in one session, no re-record.
Repeated on `videos/006-diagram-grammar/` + `007-diagram-to-pytorch/`
(2026-10-01): two takes recorded in Descript with Studio Sound (so step 3
is loudnorm only), 74.8 s → 53.8 s and 69.2 s → 42.7 s with no phrase
cuts, 14 beats built by 7 parallel agents off one shared diagram module.

---

## Why this shape (the research)

Two inputs decided the format. Both are written up in more detail in
`agents/animation-rules.md`, `agents/research/` and `agents/archive/shorts-pipeline.md`.

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

## 0. Start of a session

Read `AGENTS.md`. Open (or create) `videos/NNN-slug/` with the next number.
Write the preflight: THE QUESTION in the viewer's words, WHO IS ASKING,
THE ANSWER IN ONE SENTENCE. Put those three lines at the top of
`storyboard.md`; every beat is checked against them.

The hook, from the research in `agents/research/2026-10-03-shorts-craft.md`:
frame 0 is the finished visual already working (not a title, not a word
cloud, not a lead-in). With VO there is no question text: the band belongs
to the burned-in captions (AGENTS.md rule 6), and the answer is spoken in
the first second anyway. A VO-less clip may put the question, 5–8 words, in
the band. The first spoken line is the answer, never the question, so a
viewer who leaves at two seconds still has it (how: step 1, "VO line 1").
The last line is the one-sentence takeaway over the final visual, no
outro, no call to action.

## 1. Storyboard from the post (Claude, 5 min)

- Pick the 5–8 concepts the post already animates in your head. One idea
  per Short.
- **Pick the engine** by the rule in `AGENTS.md` ("Which engine") and make
  it the first line of `storyboard.md`: `ENGINE: manim`, `ENGINE:
  hyperframes`, or `ENGINE: mixed` with an engine column in the beat
  table. Decide now: it changes which parts the visual column can name
  and which brief the beat agents get.
- Write `videos/NNN-slug/storyboard.md`: a table `beat | VO | visual`.
- **VO line 1 is THE ANSWER from the preflight, not THE QUESTION.** The
  question lives in the on-screen band and is never spoken. Line 1 is the
  answer in plain words plus why it matters: "A vector is just a list of
  numbers, and it's the key to the math behind AI." Check before handing
  the script to Chris: if line 1 ends in "?" or starts with What / How /
  Why / Ever wondered, rewrite it.
- **VO uses the author's own sentences.** Cut and reorder; never reword.
  Target 130–150 spoken words for ~55 s. Mark the last line "if time":
  takes run long and the tail is what gets dropped.
- The visual column names parts from `agents/parts.md` to reuse, the one
  magenta hero, and where things sit (top / middle / bottom of the stage,
  and a rough row count, so the layout is decided before any code).
- **Ledger.** One short list at the top of the storyboard of everything
  that must be identical across beats: the example ("I can't log in"),
  the choices ("bug / query / spam"), names, numbers. Parallel agents copy
  from it; nothing is invented per beat.
- The example must be a real instance of the idea (a decision someone
  would make, a figure from the actual paper), not a placeholder.

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

If the take already went through Descript Studio Sound, skip the chain
and only normalize (a second denoise/compress pass dulls it):

```
ffmpeg -i vo_raw.m4a -af "loudnorm=I=-14:TP=-1.5:LRA=9" -ar 48000 -ac 1 vo_clean.wav
```

## 4. Transcribe (Claude, 30 s)

MacWhisper ships a CLI (Chris has Pro). No install needed. Two models, two
jobs (measured on ep03 against 14 cues found by hand, 2026-10-11):

| Model | Job | Why |
|---|---|---|
| Parakeet v3 | every transcript a person reads: the take (here), the cut checks (step 5), the spelling reference for captions and word times (step 7) | hears terms better ("row i of w", "i lands", digits, where Whisper wrote "IFW", "eye") and runs a 50 s take in ~1 s |
| Whisper Small | one timing transcript of `vo_final.wav` (step 5), the input to `word_times.py` and `captions_from_transcript.py` | its phrases are tight and ordered; with `word_times.py` it times words to a median 0.045 s (worst 0.24 s). Parakeet's phrases are longer and can overlap (worst 0.63 s through the same tool), and its own word timings run in 80 ms steps and early (median 0.12 s) |

```
MW=/Applications/MacWhisper.app/Contents/MacOS/mw
TXT="--language en --no-speakers --format txt --timestamps --end-timestamps --milliseconds --overwrite"
$MW transcribe --model parakeet-pro:nvidia_parakeet-v3 $TXT -o transcript.txt vo_clean.wav
```

Gotchas:
- Always pass `--model`; the app's default can change under you.
- Without `--overwrite` it refuses an existing `-o` file, silently under
  `2>/dev/null`.
- Whisper.cpp models give no word timings; Parakeet's (`--format json`, a
  `words` array per segment) are too coarse for cues. Word times come from
  `tools/word_times.py` (step 5).

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
4. **Verify by re-transcribing `vo_final.wav`** with Parakeet
   (`-o transcript_final_text.txt`). Fragments show up as odd words
   ("'cause we then", "with work", "or that"). Nudge the boundary 50–200 ms
   and repeat. Expect 2–3 rounds. The last run is the spelling reference
   for step 7.
5. Still over? `atempo=1.03` is inaudible and buys 3 %. Re-run loudnorm
   after it.

Then the timing transcript and word times, once, for every beat agent:

```
$MW transcribe --model whisper-cpp:ggml-model-whisper-small $TXT -o transcript_final.txt vo_final.wav
tools/word_times.py transcript_final.txt vo_final.wav -o words.json
```

It spreads each phrase's words over its span by syllables and places the
boundaries on the envelope's dips (no model, no new dependency). On ep03,
against 14 cues the agents had found by hand, the median error was 0.045 s
and the worst 0.24 s ("stored" after "this": a word that starts with a hiss
straight after another reads late). Fix Whisper's spellings in it as in the
captions.

Then rewrite `storyboard.md` with the final beat table: master start,
length, scene file, VO. Beat lengths are the contract for step 6.

## 6. Generate the beats (Claude, parallel agents, ~10 min)

- Manim beat: one scene file per beat, `BocShortScene`, ending in
  `self.hold_until(DURATION)` so the render is exactly the VO window.
  HyperFrames beat: one folder per beat, `NN_beat/index.html`, whose
  composition lasts exactly `BEAT_SECONDS`.
- Give each agent the brief for its engine, `agents/beat-brief.md`
  (Manim) or `agents/beat-brief-hyperframes.md` (HyperFrames), plus its
  beat's lines: file and class (or folder), `BEAT_SECONDS`, VO with
  master times, the visual brief, the hero. Group beats that share a
  visual onto one agent; write any local part (`_parts.py`) before
  spawning so every agent imports the same one. Check `agents/parts.md` first.
- **Show Chris the canonical frame before spawning agents** when the look
  is new to the repo: render `00_layout/` (the shared parts at rest) and
  send it. ep01 and ep02 each built and assembled a whole Short in a look
  Chris then rejected (the isometric floor; a 3D lattice); one frame
  settles it in one exchange.
- Name two or three finished beats that resemble each agent's brief as
  worked examples (same part, same kind of motion). Examples from our own
  passing scenes do more than rule lists.
- Agents place cues from `words.json` (step 5), master times, and check
  the ones that matter on their window's envelope; a sub-clip
  transcription only for a word that is missing or misheard. Cues from the
  audio beat the brief's estimates every time.
- Render (Manim): `cd videos/NNN-slug && uv run --no-sync manim -qh --disable_caching 0N_beat.py Class`.
  Output: `media/videos/0N_beat/1920p30/Class.mp4`. Agents may render while
  iterating, but the final pass is one sequential run per folder with
  `--disable_caching` (parallel runs race on `media/texts/`, the cache can
  drop a frame).
- Render (HyperFrames): from `videos/NNN-slug/0N_beat/`,
  `npx --yes --prefer-offline hyperframes@0.8.115 render -o ../media/hf/0N_beat.mp4`
  with the env vars in the brief. Output: `media/hf/0N_beat.mp4`. Offline
  (GSAP and Inter come from `videos/_shared/web/vendor/`), 10–20 s a beat.
  A HyperFrames beat with VO draws no captions; `assemble.py` burns them
  and muxes the VO exactly as for Manim beats.
- Only this step differs by engine. Every other step (VO first, tighten,
  captions, assemble, contact-sheet review, hand-off, update pass) is the
  same for both.

Known Manim 0.18.1 traps (details in `agents/style.md`): negative
`z_index` hides a mobject while it animates; `LaggedStart` over `Create`
of children already in the scene draws nothing; `FadeIn` in the same
`play` as `TransformFromCopy` can stack above it; `set_opacity` on a
stroke-only VMobject fills it. No LaTeX on this machine: `Text` only.

## 7. Captions and assembly (Claude, 1 min)

```
tools/captions_from_transcript.py transcript_final.txt captions.json   # ≤3 words each
# beats.json: ordered {clip, end} per beat; ends must sum to the VO length
#   clip is media/videos/<file>/1920p30/<Class>.mp4 (Manim) or media/hf/<beat>.mp4 (HyperFrames)
tools/assemble.py beats.json --vo vo_final.wav --captions captions.json \
    -o media/short.mp4
```

Captions are rasterized by Manim (same font, size and band as in-scene
captions) and overlaid with ffmpeg, because Homebrew ffmpeg lacks libass
and drawtext. Captions are bold on a dark rounded pill
(`short_caption(pill=True)`, the default since 008): diagram labels are
medium weight with no pill, so the two kinds of text never collide even
when a caption sits under white diagram text. One caption source per Short: burned from the VO, never
also drawn in scenes.

Read the generated `captions.json` once: Whisper writes "NX" for N× and
"NN module" for nn.Module; fix the text against `transcript_final_text.txt`
(Parakeet, step 5), the times are fine. Same for the words in `words.json`. A scene
element in the band too (a code card): `agents/style.md`, "Share the band
with a scene element".

## 8. Review (Claude, then Chris)

- `tools/review_frames.sh media/short.mp4` for contact sheets; or three
  20 s sheets at 300 px wide, one frame every 2 s, which shows the whole
  Short on one screen each.
- Check at that size: text legible, nothing in the dead zones, one magenta
  hero per beat, first frame moving, last frame still and clean, captions
  never two lines for more than a beat.
- Dead-zone proof: overlay a caption PNG on a real frame and `drawbox`
  the four zones at 25 % red. If text touches red, fix the constant.
- **Check every cut:** the last frame of beat N beside the first frame of
  beat N+1. Parallel agents rebuild a neighbour's end state from the brief,
  not its render, and drift: ep01 had three cuts where a border colour, an
  arrow's alpha or a label changed at the splice. HyperFrames:
  `tools/seam_check.py beats.json` diffs snapshots of every cut and writes
  the pairs to `media/seams/` (exit code = failing cuts). Manim: grab the
  frames with ffmpeg and look at them side by side at 360 px.
- Chris: watch it on a phone with sound, then muted. Listen once at the
  splice points.
- Fixing what a sheet shows: name the object and the line, fix the line,
  then the block, and only then rebuild the beat. Two review rounds per
  beat; if the same kind of problem comes back, stop and rethink the
  layout rather than nudging it again.
- A rework of several beats: resume the same agents by name with a brief
  that lists only what changed. It cost ep02 a third of a fresh spawn, and
  the agents kept their audio-derived cue times.

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
- No pinned comment (Chris doesn't do them).
- Per-video copy lives in `videos/NNN-slug/publish.md`.

## 10. Hand-off (Claude, when Chris says "done")

The last message of the session is a paste-ready pack, nothing else:

1. **The file**, as a full absolute path (`media/` is gitignored, so the
   folder on disk is the only copy). Upload the mp4 natively to Substack
   Notes; the YouTube link goes in the first reply, not the note.
2. **Title**, the recommended one, in a code block.
3. **Description**, in a code block, exactly as in `publish.md`.
4. **Substack note**, in a code block: the reader's problem in their words,
   the one takeaway, the length in seconds. No links in the note.

Everything is committed before the pack is sent, and anything the
description claims is "on screen" is checked against the final cut.

## 11. Update pass (Claude, when Chris says go)

After the hand-off pack, ask once: "Ready for the update pass?" On yes:

1. **Mine the session.** List every change Chris asked for and every
   workaround or wish an agent reported. For each, decide: rule
   (`agents/style.md`, `agents/animation-rules.md`, `agents/beat-brief.md`,
   this runbook), token (`videos/_shared/style.py`), part (`agents/parts.md`
   and code), tool (`tools/`), or nothing. Make the edits in their one home.
   A new trap is written as trigger, cause, fix, and what the wrong
   version looked like, and only once the fix has actually worked.
2. **Janitor.** `agents/parts.md` use counts, promote at two; finished plans
   to `agents/archive/`; retired scene files to `videos/_graveyard/`;
   `_preview.py` files deleted; `AGENTS.md` and `agents/` re-read for
   anything stale or contradictory (one home per topic, no duplicates).
3. **Changelog.** One line per change in `agents/changelog.md`, with the
   video that forced it.
4. **Commit** the system changes separately from the video, and tell Chris
   what changed in three lines.

## Tools (all under `tools/`, tests under `tests/`)

| Tool | Does | Tested |
|---|---|---|
| `enhance_vo.sh` | ffmpeg voice cleanup chain to −14 LUFS | manual |
| `tighten_vo.py` | range cuts, pause capping, time map | yes |
| `captions_from_transcript.py` | MacWhisper txt → captions.json | yes |
| `assemble.py` | concat beats, mux VO, burn captions | yes |
| `review_frames.sh` | contact sheets at phone size | manual |
| `seam_check.py` | HyperFrames cuts: snapshot both sides, pixel-diff, side-by-side PNGs | yes |
| `word_times.py` | each word's start from the phrase transcript and the envelope → `words.json` | yes |
| `videos/_shared/to_gif.sh` | mp4 → email-safe looping GIF (blog embeds) | manual |

Run everything: `uv run --no-sync python -m unittest discover -s tests`.
