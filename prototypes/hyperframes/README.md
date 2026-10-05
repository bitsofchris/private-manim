# HyperFrames prototypes

**Name:** hyperframes-prototypes
**Description:** Two silent 9:16 shorts built 2026-10-03 to test a web
engine (HTML/CSS/SVG rendered to MP4 by headless Chrome) for cartoon and
abstract explainers, next to Manim for technical diagrams. Each was
concepted and built by one subagent from a Substack-queue card.
**When to use:** as the worked examples for a HyperFrames beat
(`agents/beat-brief-hyperframes.md`; which engine a Short uses is decided
in `AGENTS.md`, "Which engine"). `agents/parts.md` lists the pieces worth
copying.
**How it works:** one `index.html` per video. The root div carries the
composition id, size and duration; timed elements are `class="clip"` with
`data-start` / `data-duration`; one paused GSAP timeline registered on
`window.__timelines[id]` is seeked per frame by the renderer, so every
motion must be a tween or a pure function of time (no clocks, no random).

| Folder | Idea | Concept | Length |
|---|---|---|---|
| `quiz/` | "I scored 7 out of 20 on my own quiz" | a stick figure fills a bucket from a lecture; it leaks overnight; the cold quiz is the dipstick; day 1 / day 4 / week 2 reviews patch the holes | 34 s |
| `ironies/` | Bainbridge's "Ironies of Automation" | one operator, one desk: AUTO takes the levers, the hard knot lands in their lap, the 1983 panel becomes a 2026 chat, a SKILL bar drains until "YOUR TURN" | 31 s |
| `stack-styles/` | which visual styles are possible | one beat (the transformer stack) in ten styles plus the house-style control; its own README | 5 s each |

```
cd prototypes/hyperframes/quiz
npm run check     # lint + layout + contrast
npm run render    # -> out/quiz.mp4   (npx hyperframes@0.8.115, pinned in package.json)
```

Both render offline. GSAP and Inter come from `videos/_shared/web/vendor/`
through the `vendor` symlink in each folder (HyperFrames lints `../` paths
above the project root as errors, so a relative path out of the folder
does not work), and each `index.html` declares Inter with a local
`@font-face`, so the compiler embeds the file instead of fetching Google
Fonts. The npm scripts pass `--prefer-offline` and set
`HYPERFRAMES_NO_TELEMETRY=1 HYPERFRAMES_NO_UPDATE_CHECK=1`. Checked
2026-10-03 by rendering both under `sandbox-exec` with outbound network
denied (loopback allowed): same duration, size and picture as the CDN
renders (PSNR ~51 dB); under the same sandbox the pre-change HTML fails
with `net::ERR_ACCESS_DENIED` on the GSAP script.

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
  no local `node_modules`, no lock file. Its scaffold loads GSAP from
  jsDelivr and HyperFrames fetches any font without a local face from
  Google Fonts; both prototypes now use the vendored copies instead (see
  above). Skill install was skipped (`HYPERFRAMES_SKIP_SKILLS=1`) and the
  scaffold's own `CLAUDE.md` / `AGENTS.md` were deleted so the repo keeps
  one entry point. `hyperframes.json` still names the HeyGen registry, which
  `add` / `catalog` use; beats do not run those, and the offline renders
  ran with the file in place.
- **No house template yet** (Chris, 2026-10-03). If one is ever built it
  would hold: palette CSS variables, the caption clip, the `?guides`
  overlay, the sketch filter, a stick-figure rig with pose helpers, a
  hold-freeze helper. Until a real video needs a piece twice, agents copy
  from these two files.
