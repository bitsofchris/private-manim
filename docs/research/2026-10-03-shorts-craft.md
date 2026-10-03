# Research digest: explainer Shorts craft, hooks, and design systems

**Name:** shorts-craft-research
**Description:** What practitioners and research say about (1) Manim explainer
craft, (2) opening and holding an educational Short, (3) how studios codify
motion style and how a design system stays alive. Three agent reports from
2026-10-03, condensed; every claim keeps its source. Marked **M** (measured)
or **O** (opinion / practice).
**When to use:** when changing `STYLE.md`, `ANIMATION_RULES.md`, the Shorts
constants, the storyboard step, or the hook of a Short. The plan that acts on
this is `docs/plans/design-system.md`.

## 1. What holds up (measured)

- **Visual change lands on the spoken word.** Mayer's temporal contiguity,
  9/9 experiments, median d ≈ 1.2–1.3; signaling d ≈ 0.4–0.5; segmenting
  d ≈ 0.3. Our `hold_until` beat system and one-magenta-hero rule are the
  right mechanism. **M**
  https://www.researchgate.net/publication/262915119 ·
  https://www.researchgate.net/publication/339545308 ·
  https://maria-wirzberger.de/wp-content/uploads/2019/01/Rey2019_Article_AMeta-analysisOfTheSegmentingE.pdf
- **Staged transitions beat simultaneous ones.** Heer & Robertson: move,
  then morph; keep the picture valid mid-transition; "as long as needed,
  no longer". Tversky: animation fails when too fast or too much changes.
  **M** https://idl.cs.washington.edu/files/2007-AnimatedTransitions-InfoVis.pdf ·
  https://www.tc.columbia.edu/faculty/bt2158/faculty-profile/files/_Morrison_Betrancourt_AnimationCanitfacilitate.pdf
- **Swipe-or-stay is decided in 1–3 s.** Galloway, 5,400 Shorts: under 60%
  viewed-vs-swiped rarely performs; 70–90% is the good band. **M**
  https://threadreaderapp.com/thread/1646898356419981315.html
- **Captions keep muted viewers.** 69% watch muted in public; 80% more
  likely to finish with captions (Verizon/Publicis, n=5,616); +12% view
  time in a Facebook test. **M**
  https://www.forbes.com/sites/tjmccue/2019/07/31/verizon-media-says-69-percent-of-consumers-watching-video-with-sound-off/
- **Reading speed.** Comprehension drops from 12 → 20 → 28 characters per
  second (Kruger et al. 2022 eye-tracking); Netflix caps at 17 cps. A
  3-word caption needs ≥ 1 s on screen. **M**
  https://researchers.mq.edu.au/en/publications/why-subtitle-speed-matters-evidence-from-word-skipping-and-reread/
- **Brisk narration helps.** Guo, Kim & Rubin (6.9M MOOC sessions):
  engagement rises with speaking rate; informal, drawn visuals beat
  polished slides. **M** https://up.csail.mit.edu/other-pubs/las2014-pguo-engagement.pdf
- **What 3b1b motion actually does** (Jacob et al. 2024, 15 videos, κ=.89):
  seven roles: connect representations, co-vary objects, dynamic concept,
  dynamic process, symbol sense, connect to reality, generalize by
  continuous variation. A checklist: every move serves one. **M**
  https://academic.oup.com/teamat/article/44/1/47/7681993

## 2. Practitioner consensus

- **Frame 0 is the hook.** The finished visual, already moving, filling the
  stage, with the question as 5–8 words of on-screen text because feed
  autoplay is often muted (Hoyos; YouTube creator guide). Matches our own
  84K vs 2K data. **O**
  https://blog.youtube/creator-and-artist-stories/youtube-shorts-deep-dive/ ·
  https://www.opus.pro/blog/youtube-shorts-hook-formulas
- **Speak the question in the first second.** No preamble. **O**
- **Visual first, then articulate** (Sanderson). Open on a concrete
  example; motion = logical connection, so morph A into B rather than
  fade A out and B in. **O**
  https://www.antoinebuteau.com/lessons-from-grant-sanderson/ ·
  https://medium.com/@d.danielides/understanding-linear-algebra-through-movement-a-visual-journey-83c0436ac52c
- **Endings:** no outro, no CTA; one-line takeaway over the final visual,
  cut within ~0.5 s. One creator measured 83 → 88% retention trimming a 1 s
  tail. **O** https://www.opus.pro/blog/ideal-youtube-shorts-length-format-retention
- **Opacity hierarchy:** hero 1.0, context ~0.4, scaffold ~0.15. **O**
  https://hermes-agent.nousresearch.com/docs/user-guide/skills/bundled/creative/creative-manim-video
- **Motion tokens need easings per role**, not just durations: entrance,
  exit, standard; exits shorter than entrances; longer distance → longer
  duration (IBM Carbon, Material 3). **O**
  https://carbondesignsystem.com/elements/motion/overview/ ·
  https://m3.material.io/styles/motion/easing-and-duration/tokens-specs
- **3b1b's repo pattern:** a small `custom/` of branded parts plus an
  explicit `once_useful_constructs/` graveyard. Welch Labs copies it. **O**
  https://github.com/3b1b/videos/tree/master/custom
- **Component pairs own their transitions** (ManimML: each valid pair of
  layers defines the animation between them). **O**
  https://arxiv.org/abs/2306.17108
- **Promote on the third use, not the first.** Deprecate by mark → migrate
  → remove. **O**
  https://www.designsystemscollective.com/dont-build-reusable-components-too-early-f5377c75f0d9
- **Agent-consumable design systems:** tokens as data are normative, prose
  explains why, required do/don't pairs, a linter validates. **O**
  https://github.com/google-labs-code/design.md/blob/main/docs/spec.md
- **Review:** mute test, squint/thumbnail test, contact sheet at 2 fps, 12
  consecutive frames around fast action. **O**
  https://sunstrikestudios.com/en/blog/timing_in_animation/

## 3. Manim CE 0.18.1 traps worth encoding

- Negative or zero `z_index` on an animated mobject breaks `LaggedStart`.
  https://github.com/ManimCommunity/manim/issues/3914
- `Text` cache ignores non-string kwargs → stale renders; `--disable_caching`.
  https://github.com/ManimCommunity/manim/issues/4096
- `Text` strips whitespace, so glyph indices skip spaces; ligatures break
  per-glyph work (`disable_ligatures=True`).
  https://docs.manim.community/en/stable/reference/manim.mobject.text.text_mobject.Text.html
- Add copies of template mobjects to scenes; keep originals pristine.
  https://flyingframes.readthedocs.io/en/latest/ch3.html
- `manim-voiceover` gives per-word bookmarks from recorded audio; a
  candidate to replace hand-timed cues. https://voiceover.manim.community/en/stable/

## 4. Things we were already doing right

One hero per beat, change on the word, captions in the lower third, no
decorative motion, concrete example first, VO sets the clock. Keep them.

## 5. Things to change (feeds the plan)

1. Frame 0 carries the question as on-screen text, in the band, before the
   first caption.
2. Caption minimum hold from length (≤ 15 cps), checked at assembly.
3. Easing roles and an opacity hierarchy as tokens.
4. Morph over cut: fade-swap only when the thing changes meaning.
5. A layout check that fails a render for text under the floor, outside
   safe, overlapping, or in the band.
6. Promote parts on repeat use; a graveyard folder for retired ones.
7. Tag each beat's moves with the role they serve; untagged motion is cut.
