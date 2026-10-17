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

**The channel's own data** (`~/repos/yt-stats`, read 2026-10-11, all 28
Shorts; the full read is the vault note "YouTube Shorts - What's Working -
2026-10-11"):

- 62 % of Shorts views come from YouTube search, 13 % from the Shorts
  feed. The 86K Short (PyTorch Neural Networks Made Simple) is 68 %
  search, 6 % feed: under 1K views a month for six months, then ~5K a
  month once search found it, and 289 of the 330 subscribers Shorts have
  brought in. Its top terms: "pytorch", "neural network", "pytorch full
  course".
- Shorts titled with a phrase people type ("pytorch", "what is jev",
  "zettelkasten") get 50–77 % of views from search and keep growing.
  Clever advice titles get 72–88 % from the feed, ~0 % from search, and
  stop at 300–600 views.
- Code on screen holds people: the three best ML Shorts by retention and
  subscribers show PyTorch code, and 007 (a transformer in 20 lines of
  PyTorch) beats the pure-animation transformer Shorts (005, 009) on
  every rate.

Lesson: a Short here is found by search, so the title and VO line 1 are a
query and its answer. The visual rules below decide whether the people
who arrive stay.

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
THE ANSWER IN ONE SENTENCE, and THE SEARCH PHRASE: the 2–5 words that
person types into YouTube ("pytorch neural network", "what is jev").
Check the phrase in YouTube's search box before writing a beat:

- autocomplete offers it or something close; if not, nobody types it, so
  take the phrase autocomplete does offer;
- the results are about your topic ("ai architecture" returns buildings,
  and 006 drew those searchers);
- when the Short is meant to grow the channel, it is what a learner
  types: a news term brings views without subscribers (008: 1K views,
  0 subs).

Put those four lines at the top of `storyboard.md`; every beat is checked
against them.

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

- **Draft from Chris's own notes, with his writing skills.** Run
  `content-preflight` (the question, who's asking, the answer in one
  sentence), then `notes-to-post` (the reader's wrong belief, one idea,
  one action, Chris's story as the proof, no watering down his words),
  then `effective-writing` for the line edit. The skills live in
  `~/.claude/skills/`. One idea, one action the viewer takes after. A
  paper is one evidence beat at most, never the spine: research notes
  (a series' `key-points.md`) supply evidence, not the script's shape.
  Harness series 012 drafted eps 2, 3, 5, 8, 9 and 10 evidence-first as
  paper tours; Chris threw out ep 2 and they were rebuilt from his notes
  (2026-10-17).
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
- **Line 1 is a reframe the viewer can see, not a definition.** Held
  people: "Every mark on this diagram is a line of PyTorch" (007), "A
  neural network is just a function" (004, and the 2024 Short that opens
  the same way). Lost them: "A transformer takes a sequence of tokens and
  produces updated representations of those tokens" (005, 009: the lowest
  retention of the ML Shorts). If line 1 would fit in a glossary, rewrite
  it. Say the search phrase in line 1 when it fits naturally.
- **VO uses the author's own sentences.** Cut and reorder; never reword.
  Target 130–150 spoken words for ~55 s. Mark one beat *(if time)*, the
  detour the viewer would not miss, because takes run long. Never mark
  the closer, the only "how" beat, or a contrast that stops a wrong
  takeaway (harness ep 4's map → drill → retrieve, ep 6's expert skills).
- **Say each thing once, and get to it fast.** Check every beat before
  handing the script to Chris (from tightening the harness series, 012):
  - Line 1 lands the answer in its first clause. Ep 9's 27-word line 1
    reached "share one notebook" too late; split it.
  - The thing the title names is on screen and said within ~8 s. Setup
    that frame 0 already shows (a tag, the counts) is not spoken. 013
    ep01 shipped only after two late cuts moved "confusion matrix" from
    20.8 s to 6.4 s (48.8 → 34.1 s): the context line, the setup line and
    the restated hook all went.
  - Each beat adds a new fact, example or step. If cutting it loses
    nothing, cut it. No second definition of the term (ep 1 had three,
    ep 4 had three "map" lines).
  - The closer is the viewer's next move, not line 1 again: line 1 says
    what's true, the last line says what to do (ep 3, 5, 6, 10 restated
    line 1). One takeaway, not two (ep 7).
  - A good line that answers a different question goes to the written
    companion: an aside, a hand-off to the next episode (ep 2's "my
    read", ep 3's janitor teaser, 3b's "start simple").
  - Skip what the audience uses daily; start at what they don't know
    (ep 2's "a model can't see your repo").
  - No hedges in the VO. Narrow the claim until it's true; caveats go in
    the notes and the companion (ep 2's "partly, it ran out of room").
  - Steps, lists and code go on screen, not in the VO (ep 6's skill
    steps became its code beat).
  - In a story, keep only the detail the payoff needs; times, counts
    and asides go (ep 9's door story).
  - In a series, each sentence has one home Short (the janitor line was
    in ep 3, 3a and 3b).
  - The title promises what the script delivers (ep 3's "AGENTS.md best
    practices" has one AGENTS.md beat).
- The visual column names parts from `agents/parts.md` to reuse, the one
  magenta hero, and where things sit (top / middle / bottom of the stage,
  and a rough row count, so the layout is decided before any code).
- **Ledger.** One short list at the top of the storyboard of everything
  that must be identical across beats: the example ("I can't log in"),
  the choices ("bug / query / spam"), names, numbers. Parallel agents copy
  from it; nothing is invented per beat.
- The example must be a real instance of the idea (a decision someone
  would make, a figure from the actual paper), not a placeholder.
- **Show the code** when the idea has an implementation. At least one
  beat puts the real lines on screen (`code_block` + `highlight_lines`,
  or the HyperFrames code card), ideally the payoff beat. The channel's
  best-retaining and best-converting Shorts all show code.

## 2. Record once (Chris, 3 min)

- QuickTime Player → New Audio Recording → Maximum quality, good mic.
- Read the script in one pass. Pause ~1 s between beats. Flub? Pause and
  re-read the sentence; the cut step handles it.
- Save as `vo_raw.m4a` in the video folder. Do not re-record for length.
- In a series, record every episode in one file and split it per episode
  (`agents/series.md`, steps 3–4).

## 3. Clean the audio (Claude, 10 s)

```
tools/enhance_vo.sh vo_raw.m4a vo_clean.wav
```

High-pass 80 Hz → loudnorm to −14 LUFS / −1.5 dBTP (YouTube's target).
That is the whole default, for a raw take and for a Descript Studio Sound
take alike: Chris picked it by ear on 013 ep01 over the old chain, whose
fixed denoise (`afftdn nf=-25`, ~30 dB above a quiet room) and 3:1
compressor smeared the voice.

Denoise only when the room is audible (a fan, hiss) and never on a Studio
Sound take: `tools/enhance_vo.sh --denoise vo_raw.m4a vo_clean.wav` sets
the denoiser's floor from the take (`tools/vo_floor.py vo_raw.m4a` prints
it; a quiet room reads −55 to −70 dB) and adds a de-esser. Listen to both
and keep the default unless the noise is plainly worse. It will not remove
reverb or a barking dog.

## 4. Transcribe (Claude, 30 s)

MacWhisper ships a CLI (Chris has Pro). No install needed. Two models, two
jobs (measured on ep03 against 14 cues found by hand, 2026-10-11):

| Model | Job | Why |
|---|---|---|
| Parakeet v3 | every transcript a person reads: the take (here), the cut checks (step 5), the spelling reference for captions and word times (step 7) | hears terms better ("row i of w", "i lands", digits, where Whisper wrote "IFW", "eye") and runs a 50 s take in ~1 s |
| WhisperKit Large v2 | one timing transcript of `vo_final.wav` as JSON (step 5): a start per word from the recognizer, the input to `word_times.py`, which feeds the cues and the captions | ~20 s for 50 s of VO; median 0.07 s, worst 0.20 s against the 14 cues. Measured alongside: Parakeet's own word times (median 0.12 s, in 80 ms steps, early), WhisperKit Small.en (0.08 / 0.22 s, dropped a word), and whisper.cpp Small phrases + the estimator in `word_times.py` (0.045 / 0.24 s, but scored against cues found on the same loudness curve it uses). The estimator stays as the fallback for a segment without word times |

```
MW=/Applications/MacWhisper.app/Contents/MacOS/mw
TXT="--language en --no-speakers --format txt --timestamps --end-timestamps --milliseconds --overwrite"
$MW transcribe --model parakeet-pro:nvidia_parakeet-v3 $TXT -o transcript.txt vo_clean.wav
```

Gotchas:
- Always pass `--model`; the app's default can change under you.
- Without `--overwrite` it refuses an existing `-o` file, silently under
  `2>/dev/null`.
- Only WhisperKit and Parakeet put word times in `--format json` (a
  `words` array per segment); whisper.cpp gives none. A recognizer often
  pins a phrase's first word to the silence before it; `word_times.py`
  moves such a word to where the speech starts.
- A newly downloaded WhisperKit model is unknown to the CLI until the app
  has finished preparing it ("Unknown model"); check `$MW models list`.

## 5. Tighten (Claude + Chris, the only judgment step)

1. Read the transcript. Mark: flubs, repeated ideas, clauses that don't
   earn their seconds. Propose whole-phrase cuts with per-beat second
   counts. **Chris approves the cut list.** Under 60 s is the constraint.
   Send with it, as clips, anything only an ear can settle: a number the
   recognizers hear differently from the script (013 ep04: both heard
   "0.95"; Chris said 0.985) and any line spliced in from elsewhere in the
   take (013 ep04's context splice was approved on paper and cut on the
   first watch).
2. Find cut boundaries:
   - `ffmpeg silencedetect` (`d=0.45`, noise 12 dB above the floor that
     `tools/vo_floor.py` prints, as `--noise auto` sets it) gives the
     pause map.
   - A cut that falls mid-phrase: extract the 2–5 s region, transcribe
     just that clip (`mw` on the sub-clip gives finer segments), and run
     silencedetect at `-40dB d=0.04` for micro-pauses.
3. Apply:

```
tools/tighten_vo.py vo_clean.wav --out vo_final.wav --map timemap.json \
    --max-gap 0.25 --noise auto --level -14 --remove 22.8-26.45 --remove 41.2-43.8 ...
```

   Drops the ranges, pads each kept piece 80 ms (never back into a removed
   range, so a mid-phrase cut stays cut), caps every pause, 8 ms fades at
   each join, writes an old→new time map, then levels the result to −14
   LUFS (cutting pauses moves it: 013 ep01 went to −15.9). `--noise auto`
   puts the pause threshold 12 dB above the take's noise floor; a fixed
   `-35dB` clipped word tails on 013 ep01 ("attacks" → "attacked").
   A cut inside a phrase: put its edges at the envelope dips around the
   words, not at the recognizer's word times (013 ep01: "flags" started
   30 ms before its WhisperKit time, and "here's" lost its "h" at 20 ms).
   End the Short, and every kept piece, where the sentence ends in the
   take: check the next word in the master transcript. 012 ep03 stopped at
   "knowledge base" where the take went on "for research…"; the voice
   never fell and Chris heard it as cut off.
4. **Verify by re-transcribing `vo_final.wav`** with Parakeet
   (`-o transcript_final_text.txt`). Fragments show up as odd words
   ("'cause we then", "with work", "or that"). Nudge the boundary 50–200 ms
   and repeat. Expect 2–3 rounds. The last run is the spelling reference
   for step 7.
5. Still over? `atempo=1.03` is inaudible and buys 3 %. Re-run loudnorm
   after it.
6. Re-cleaning after the beats are built (a different chain): re-apply
   the same time map, so every beat, caption and word time keeps its
   timing: `tools/tighten_vo.py vo_clean.wav --out vo_final.wav --map-in
   timemap.json --level -14`.

Then the timing transcript and word times, once, for every beat agent and
for the captions:

```
$MW transcribe --model whisperkit:openai_whisper-large-v2 --language en --no-speakers \
   --format json --overwrite -o transcript_final.json vo_final.wav
tools/word_times.py transcript_final.json vo_final.wav -o words.json
```

`words.json` is `[{"t", "end", "word", "seg"}]`, master seconds. Fix its
spellings against `transcript_final_text.txt` (Parakeet) now: the captions
are built from it in step 7, so one fix serves both. `tools/fix_words.py`
does it in one line per fix: `--join "agent's MD," "AGENTS.md,"` (merged
words), `--sub harnesses "harness is"`, and `--break-after WORD` where the
recognizer ran two segments together; `WORD@SECONDS` picks one occurrence.

Then the final beat table: `tools/beat_cuts.py words.json vo_final.wav
01_hook 02_context=Context 03_tools=Tools ...` puts each cut mid-pause
before the beat's first word (at least 80 ms before it), writes
`beats.json` and prints the table (start, length, folder, VO) for
`storyboard.md`. Beat lengths are the contract for step 6.

Under it, a **seam-states table**: every cut, and what is on screen there
(each shared part's state, which labels are on, where things sit). The
agents on either side of a cut both build to that row, so the cut matches
without either seeing the other's render (012 ep01: five of six cuts
pixel-identical on the first render).

## 6. Generate the beats (Claude, parallel agents, ~10 min)

- Manim beat: one scene file per beat, `BocShortScene`, ending in
  `self.hold_until(DURATION)` so the render is exactly the VO window.
  HyperFrames beat: one folder per beat, `NN_beat/index.html`, whose
  composition lasts exactly `BEAT_SECONDS`.
- Give each agent the brief for its engine, `agents/beat-brief.md`
  (Manim) or `agents/beat-brief-hyperframes.md` (HyperFrames), plus its
  beat's lines: file and class (or folder), `BEAT_SECONDS`, VO with
  master times, the visual brief, the hero. Group beats that share a
  visual onto one agent, and give one agent both sides of a cut that a
  beat-only prop crosses (012 ep01's tool icons, beats 3 → 4: exact). Write
  any local part (`_parts.py`, or a HyperFrames kit like `_kit/`) before
  spawning so every agent draws the same one. Check `agents/parts.md` first.
- **Show Chris the canonical frame before spawning agents** when the look
  is new to the repo: render `00_layout/` (the shared parts at rest) and
  send it. ep01 and ep02 each built and assembled a whole Short in a look
  Chris then rejected (the isometric floor; a 3D lattice); one frame
  settles it in one exchange. Send two or three different takes on the
  hero image side by side in one PNG, not one: 012 ep01's single rig was
  rejected and cost a round; three stills settled it in the next message.
  Render it while the cut list waits, and send the cut list and the frame
  together, so one reply approves both.
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
tools/captions_from_transcript.py words.json captions.json   # ≤3 words and ≤15 characters (one line), timed by their words
# beats.json (tools/beat_cuts.py, step 5): {"beats": [{clip, end}, ...]} in order; ends sum to the VO length
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

A caption never crosses a sentence end (. ? !), even where the recognizer
put two sentences in one segment. Read the generated `captions.json` once: Whisper writes "NX" for N× and
"NN module" for nn.Module. Spellings are fixed in `words.json` (step 5),
so a wrong word here means a fix missed there: fix it there and rebuild. A scene
element in the band too (a code card): `agents/style.md`, "Share the band
with a scene element".

## 8. Review (Claude, then Chris)

- `tools/review_frames.sh media/short.mp4` for contact sheets (the last
  tile is always the final frame; `--at 1.48,2.54` adds tiles at cue
  times); or three
  20 s sheets at 300 px wide, one frame every 2 s, which shows the whole
  Short on one screen each.
- Check at that size: text legible, nothing in the dead zones, one magenta
  hero at a time, first frame moving, last frame still and clean, captions
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
- A line cut after assembly ("too long before X"): cut the finished VO,
  not the take, so every beat after the cut keeps its audio to the sample:
  `tools/cut_vo.py vo_final.wav --out vo_final.wav --words words.json
  --cut A-B[:silence] ...`. Cut whole beats where you can (a beat that
  starts in silence can simply be dropped, and `--cut 0-T` drops an
  opening), give the shortened beats new cues, rebuild captions and
  beats.json, re-transcribe to check the joins. 013 ep01: two late cuts,
  beats 4–7 untouched.
- Re-cleaning the voice after assembly: `tighten_vo.py --map-in` (step 5).

## 9. Publish (Chris, 2 min)

The channel's own evidence: 62 % of Shorts views come from search, and
the Shorts that get found are titled with a phrase people type (step 0's
search phrase). The "Made Simple" suffix is not what does it: on concept
nouns it got 25–44 % of views from search (004, 005, 006), and "AI
Architecture Diagrams" drew searches for buildings. General guidance agrees: keyword in the first 30–40 characters, title
under ~50 so the feed doesn't truncate it, first 100 characters of the
description carry the takeaway, 3–5 hashtags at the end, tags barely matter.

**The rule:** *The title starts with the search phrase from step 0, in
those words, then promises it's simple.* One idea, no clever hook in the
title; the visual is the hook.

- Title: `<search phrase> Made Simple (Beginner Friendly)`, or
  `What is <X>? <the answer in ≤ 5 words>` for a new term. ≤ 50
  characters.
- Description: line 1 answers THE QUESTION in one sentence and contains
  the search phrase (≤ 100 chars). Then
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

## 12. Day-10 and day-30 read (Claude)

Search takes time: the 86K Short got under 1K views a month for its first
six months. A Short is judged at day 10 and again at day 30, never in its
first week.

```
cd ~/repos/yt-stats && python3 -m yt_stats sync && python3 -m yt_stats report
```

If it says to log in, Chris runs `python3 -m yt_stats login` and clicks
Allow. Copy this Short's numbers into `videos/NNN-slug/publish.md` under
`## Day-10 read` (later `## Day-30 read`): search %, top search terms,
stayed %, relative retention, at end, subs and shares per 1K. Then:

- Compare the search terms with THE SEARCH PHRASE. If people typed
  something else, the phrase rule in step 0 or the title rule in step 9
  gets the fix.
- Relative retention under 0.55, or at end under 0.25: look at VO line 1
  and frame 0 first (step 0, and step 1 "Line 1 is a reframe").
- A rule change gets a changelog line, as in step 11.

## Tools (all under `tools/`, tests under `tests/`)

Commands in this runbook name tools from the repo root and run from the
video folder. In a series episode the folder is a level deeper
(`videos/NNN-series/epNN-slug/`), so call them as
`"$(git rev-parse --show-toplevel)"/tools/NAME` rather than counting `../`.
The Python tools are executable; `uv run --no-sync python tools/NAME.py`
also works.

| Tool | Does | Tested |
|---|---|---|
| `enhance_vo.sh` | high-pass + loudnorm to −14 LUFS; `--denoise` adds a floor-matched denoise and de-ess | manual |
| `vo_floor.py` | a take's noise floor in dB (10th-percentile 50 ms RMS) | yes |
| `tighten_vo.py` | range cuts, pause capping, time map; `--noise auto`, `--level`, `--map-in` | yes |
| `cut_vo.py` | cut phrases out of a finished `vo_final.wav`, shift `words.json` (late cuts, step 8) | yes |
| `captions_from_transcript.py` | `words.json` (or a MacWhisper .json / .txt) → captions.json | yes |
| `fix_words.py` | `words.json` spellings and caption breaks: `--join`, `--sub`, `--break-after` | yes |
| `beat_cuts.py` | cuts mid-pause before each beat's first word → `beats.json` + the final beat table | yes |
| `assemble.py` | concat beats, mux VO, burn captions | yes |
| `review_frames.sh` | contact sheets at phone size, ending on the final frame; `--at` adds cue times | manual |
| `seam_check.py` | HyperFrames cuts: snapshot both sides, pixel-diff, side-by-side PNGs; `--beat` for one beat's cuts | yes |
| `hf_state_check.js` | a seam-state HyperFrames beat's first and last states against the kit's `SEAM`, in Node, before rendering | yes |
| `word_times.py` | each word's start: the recognizer's (WhisperKit JSON) out of the silence, or estimated from the envelope → `words.json` | yes |
| `videos/_shared/to_gif.sh` | mp4 → email-safe looping GIF (blog embeds) | manual |

Run everything: `uv run --no-sync python -m unittest discover -s tests`.
