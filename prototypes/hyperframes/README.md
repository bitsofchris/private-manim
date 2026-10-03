# HyperFrames prototypes

**Name:** hyperframes-prototypes
**Description:** Two silent 9:16 shorts built 2026-10-03 to test a web
engine (HTML/CSS/SVG rendered to MP4 by headless Chrome) for cartoon and
abstract explainers, next to Manim for technical diagrams. Each was
concepted and built by one subagent from a Substack-queue card.
**When to use:** deciding whether a beat or a whole short should be built
in HyperFrames instead of Manim, and as the worked examples if it is.
**How it works:** one `index.html` per video. The root div carries the
composition id, size and duration; timed elements are `class="clip"` with
`data-start` / `data-duration`; one paused GSAP timeline registered on
`window.__timelines[id]` is seeked per frame by the renderer, so every
motion must be a tween or a pure function of time (no clocks, no random).

| Folder | Idea | Concept | Length |
|---|---|---|---|
| `quiz/` | "I scored 7 out of 20 on my own quiz" | a stick figure fills a bucket from a lecture; it leaks overnight; the cold quiz is the dipstick; day 1 / day 4 / week 2 reviews patch the holes | 34 s |
| `ironies/` | Bainbridge's "Ironies of Automation" | one operator, one desk: AUTO takes the levers, the hard knot lands in their lap, the 1983 panel becomes a 2026 chat, a SKILL bar drains until "YOUR TURN" | 31 s |

```
cd prototypes/hyperframes/quiz
npm run check     # lint + layout + contrast
npm run render    # -> out/*.mp4   (uses npx hyperframes@0.8.115, pinned in package.json)
```

## Field notes

- **Speed.** Renders take 10–20 s per 30 s video; each short passed review
  in two or three renders. Manim takes minutes for the same length.
- **Good at:** characters and props in SVG, posing a stick figure, UI
  mock-ups (chat windows, panels), hand-drawn "boil" via an SVG turbulence
  filter stepped a few times a second, CSS caption pills, color tweens.
- **Bad at:** math, axes, anything Manim has primitives for. Nothing
  enforces the house style; the palette and safe areas were followed
  because the brief said so.
- **Its own `check`** lints layout and contrast, which is the kind of
  geometry check our Manim side is missing.
- **Dependencies.** `hyperframes@0.8.115` (Apache-2.0, heygen-com) via npx,
  no local `node_modules`, no lock file. The scaffold loads GSAP 3.14.2
  from jsDelivr and fetches Inter from Google Fonts into
  `~/.cache/hyperframes`. Skill install was skipped
  (`HYPERFRAMES_SKIP_SKILLS=1`) and the scaffold's own `CLAUDE.md` /
  `AGENTS.md` were deleted so the repo keeps one entry point.
- **A house template would need:** palette CSS variables, a caption clip
  component, the `?guides` safe-area overlay (both prototypes have one),
  the sketch filter, a stick-figure rig with pose helpers, a hold-freeze
  helper, and a way to take beat lengths from `beats.json` so a
  HyperFrames beat can sit in a Manim short.
