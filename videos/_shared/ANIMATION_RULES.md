# Animation Rules

**What:** 15 checkable rules for making explainer animations clear and useful, drawn from 3Blue1Brown, animation research, and classic animation principles.
**When to use:** Before scripting a video, and as a checklist in code review of any scene file.
**How it works:** Each rule is one imperative sentence, followed by a one-line *why* with its source. `STYLE.md` covers *which* constants and mobjects to use. This file covers *when and how* to move them.

## Rules

### Story (what to animate)

1. **Animate a change only when the narration is naming that change right now. If the idea isn't changing, nothing moves.**
   *Why:* Grant: "Every movement on the screen should be deliberate, with an identifiable purpose" (3b1b About). Tversky's congruence principle says the display's structure should match the concept's structure.
2. **Open on a concrete example, such as one neuron or one data point. Do not open on a definition or a general formula. The general form arrives last.**
   *Why:* 3b1b About: "Concrete before abstract" and "Never start with definitions."
3. **Use motion for what really varies (a parameter sweep, a transform, a gradient step). Show static facts as still frames.**
   *Why:* Tversky et al. (2002) found that animation helps only when change over time is the concept. Otherwise a static graphic does as well.
4. **Cut every mobject and motion that isn't the point: no decorative flourishes, and no equations or text sliding around for show.**
   *Why:* Mayer's coherence principle is that people learn more when extraneous material is left out. Grant warns against Manim "overuse and abuse" (3b1b About).

### Motion (how it moves)

5. **Each `self.play` makes one kind of change. If a transition mixes kinds (axis rescale + value change), split it into two plays, and never use more than about 3 stages.**
   *Why:* Heer & Robertson (2007) found that simple staging helped, while heavy "one thing at a time" staging raised error.
6. **Use the default `smooth` rate function (ease in/out) for moves. Use `linear` only for continuous `ValueTracker` sweeps where a constant rate means something.**
   *Why:* Heer & Robertson's "maximize predictability" calls for slow-in slow-out timing. This is also Disney's "slow in and slow out" principle.
7. **Prefer translate, grow, and fade over rotate and complex morphs, and keep motion paths direct so the endpoint is predictable mid-flight.**
   *Why:* Heer & Robertson's "use simple transitions" says translation and expand/contract are easier to follow than rotation.
8. **A mobject that stands for a thing stays that mobject through the transition. Use `Transform` only when the object keeps its identity, and `FadeOut`+`FadeIn` when it doesn't.**
   *Why:* Heer & Robertson's "respect semantic correspondence" says marks for one data point must not be reused for a different one.
9. **Give any move the viewer must track at least `S.BEAT`. Use `S.HOLD`-scale run times (about 1 s) for staged steps. Never use `S.QUICK` for a change that carries meaning.**
   *Why:* Heer & Robertson recommend about 1 s per stage, because half-second stages hurt tracking. Tversky's apprehension principle says animations fail when too fast to perceive.
10. **After each key reveal, `self.beat("HOLD")` before the next change starts.**
    *Why:* Heer & Robertson say the dwells between stages must be long enough for accurate change tracking.
11. **Before a change, signal where to look: a quick `S.HIGHLIGHT` pulse or an `Indicate` on the thing that is about to move.**
    *Why:* Mayer's signaling principle is to add cues that highlight organization. Heer cites Disney's anticipation and staging as ways to direct attention.

### Frame (layout / color / text)

12. **Color is meaning. Use one magenta hero per beat, keep the same color for the same concept across every scene, and let everything else recede (`FG_DIM`, `MUTED`, `OP_GHOST`).**
    *Why:* Disney staging is "the presentation of any idea so that it is completely and unmistakably clear" (Johnston & Thomas). Heer asks for consistent mappings.
13. **Put a label next to the thing it names and move it with that thing (`always_redraw` / `next_to`). Never use a legend or a far corner.**
    *Why:* Mayer's spatial contiguity principle (median effect size 1.10) is that corresponding words and pictures should be near each other.

### Sound / VO sync

14. **Make the visual change land on the word that names it, at the same moment and not a sentence before or after.**
    *Why:* Mayer's temporal contiguity principle is that animation and narration together beat animation and narration in sequence. Grant says each visual "should communicate the same point that the narration is" (3b1b About).
15. **Never put the narration on screen. Captions are a few key words, never a transcript.**
    *Why:* Mayer's redundancy principle is that graphics + narration beat graphics + narration + text. A boundary condition is that short on-screen text is OK.

## Process

**Documented (Grant / 3Blue1Brown):**
- He lays out the animations in a timeline first, *then* records voiceover. After that, editing takes "like a day" (Dwarkesh interview).
- Manim is "just a tool for making individual clips to be edited together later." He worries when people ask how to sync narration inside Manim, and says to use a traditional video editor as much as you can (3b1b About).
- He thinks visually in code: he "can't even put into words what I want to put on the screen, except to do so in code" (Dwarkesh).
- His scene workflow is interactive: `manimgl file.py Scene -se <line>` plus `checkpoint_paste()` to iterate on one animation at a time (3b1b/videos README).

**Documented (Kurzgesagt):** research → script (about a dozen drafts) → sketching visual metaphors → illustration → voiceover, which "provides the timing for the animation team" → soundtrack. This is audio-first.

**Inference, not sourced:** Grant clearly has a written script or outline before the timeline (he narrates to the animations). We found no source saying he records final VO before animating. His order is roughly script → animate → VO → retime in the editor, which is visual-first. Kurzgesagt locks the VO first and animates to it.

**Implication for us (recommendation):**
- For **shorts (under 60 s)**, go audio-first like Kurzgesagt. Lock the script, record VO (scratch or final), mark the timestamp of each noun or verb that triggers a change, then build one scene or clip per sentence whose `beat()`s fit those gaps. At short length, pacing *is* the VO.
- For **longer explainers**, a Grant-style visual-first order is fine: script → animate clips → record VO → retime in the editor.
- Either way, don't sync audio inside Manim. Render clips and sync in the editor.
- Note: `S.BEAT` = 0.6 s is shorter than Heer's roughly 1 s recommendation for tracked moves. Rule 9 therefore steers meaningful moves toward `HOLD`-scale run times.

## Sources

- 3Blue1Brown About / advice: https://www.3blue1brown.com/about/
- Grant on Dwarkesh Podcast: https://www.dwarkesh.com/p/grant-sanderson
- 3b1b/videos README (workflow): https://github.com/3b1b/videos
- "How I animate 3Blue1Brown": https://3blue1brown.substack.com/p/how-i-animate-3blue1brown
- Kurzgesagt, what we do: https://kurzgesagt.org/what-we-do?visit=videos
- Tversky, Morrison & Betrancourt (2002), *Animation: can it facilitate?*: https://hci.stanford.edu/courses/cs448b/papers/Tversky_AnimationFacilitate_IJHCS02.pdf
- Heer & Robertson (2007), *Animated Transitions in Statistical Data Graphics*: https://idl.cs.washington.edu/files/2007-AnimatedTransitions-InfoVis.pdf
- Mayer & Fiorella, *Principles for Reducing Extraneous Processing* (Cambridge Handbook ch. 12): https://edtechuvic.ca/wp-content/uploads/sites/11/2022/09/principles-for-reducing-extraneous-processing-in-multimedia-learning-coherence-signaling-redundancy-spatial-contiguity-and-temporal-contiguity-principles.pdf
- Twelve basic principles of animation: https://en.wikipedia.org/wiki/Twelve_basic_principles_of_animation
- Manim rate functions: https://docs.manim.community/en/stable/reference/manim.utils.rate_functions.html
