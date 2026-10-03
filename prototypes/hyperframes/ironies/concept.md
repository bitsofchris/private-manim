# Ironies of Automation — concept (HyperFrames prototype)

## Concept

**"The Watcher."** One stick-figure operator sits at one desk for the whole
short. In 1983 they work two levers by hand; a piston marked AUTO takes the
levers, the machine spits a tangled knot (the part nobody could automate) into
their lap, and all that is left to do is hold the knot and stare at the panel.
The panel then flips from dials to an AI chat window (1983 -> 2026) and nothing
else about the picture changes — that is the joke. A SKILL bar that has hung
over the figure's head since frame 0 drains while they watch, so when the
machine finally says YOUR TURN, the bar is empty.

One metaphor carries it: **same chair, same stare, different screen; the skill
bar empties while the hands do nothing.**

Colour roles (house look): teal = the human's own work (levers, knot once it is
theirs, skill bar). Magenta = the one thing each beat points at. Muted = old
heroes and construction lines.

## Storyboard (31 s, 1080x1920, 30 fps, silent)

| # | Seconds | On screen | Magenta hero | Caption |
|---|---------|-----------|--------------|---------|
| 1 | 0.0 - 4.5 | Operator pumps two teal levers from frame 0; dials twitch, lamps blink; "1983" over the panel. At ~1.5 s a piston shoots out of the panel, grabs the levers, pumps them faster; hands drop to the lap. | AUTO lamp + piston | 1983. Automate the easy part. |
| 2 | 4.5 - 9.0 | Panel ejects a tangled knot; it bounces into the operator's lap; they look down and start picking at it. | the knot | You keep the hard part. |
| 3 | 9.0 - 13.0 | Knot turns teal (it is theirs now). Eyes lift to the panel; a dotted sight-line runs from eye to machine while hands fumble blind. | the sight-line | And you watch the machine. |
| 4 | 13.0 - 17.0 | "1983" flips to "2026"; dials fold away, a chat window grows in the same panel; levers sink into the desk. Figure does not move. | "2026" | Swap "operator" for "AI user." |
| 5 | 17.0 - 21.5 | Output lines stream down the chat faster than anyone could read. Hands go still. A teal tick stamps on, then a big "?" lands over the output. | the "?" | Looks fine. Is it right? |
| 6 | 21.5 - 26.0 | Output keeps streaming. SKILL bar drains from full to a sliver; figure slumps back, eyelids drop. | SKILL label | Only watching, skills fade. |
| 7 | 26.0 - 31.0 | Stream stops. Panel says YOUR TURN. Figure jolts forward, eyes wide on the knot, hands hover and shake over it; bar is empty. Motion settles by 29.8 s, hold. | YOUR TURN | Your turn. Use it or lose it. |

## Layout

- Safe area: x 65..950, y 230..1536. Scene stage y 260..1060, captions centred
  on y ~1290 in a dark pill, 76 px bold.
- Labels (1983/2026, AUTO, SKILL, YOUR TURN, ?) are all >= 60 px.
- Floor lines bleed to the frame edges below the caption (background only).
