ENGINE: hyperframes

# What is Jev and why is everyone excited?, isometric — storyboard

**What this is:** `videos/008-jev-decision-models` rebuilt beat for beat in
the isometric HyperFrames house style (the look of 009 and 010), over the
same voice-over, cut and captions. The question, answer, ledger of example
values, sources and VO are 008's and live in
`../008-jev-decision-models/storyboard.md`; nothing was re-recorded.

**Audio and captions (not copied):** `../008-jev-decision-models/vo_final.wav`
and `../008-jev-decision-models/captions.json`.

## The look

A model is a slab with its name on the front face; a probability is the
height of a pillar; data falls down through a machine. The three choices keep
their colours everywhere (bug teal, query blue, spam gold). Parts shared by
the beats are in `_jev/jev.js`; the kit is 009's `_iso/iso.js`; beat 5 uses
010's transformer figure; `BRIEF.md` is the contract the beat agents built
to, including the accuracy rules.

## Final beats

| # | Beat | Master start | Length | Folder |
|---|------|-------------:|-------:|--------|
| 1+2 | Hook and what it is | 0.00 | 10.14 | `01_hook` |
| 3 | One pass | 10.14 | 13.11 | `03_onepass` |
| 4 | Agents | 23.25 | 10.53 | `04_agents` |
| 5 | Decision head | 33.78 | 13.69 | `05_head` |
| 6 | Your own labels | 47.47 | 7.682 | `06_labels` |

Total 55.15 s. VO per beat is in `BRIEF.md`.

## Render and assemble

```
cd videos/011-jev-decision-models-iso
export HYPERFRAMES_NO_TELEMETRY=1 HYPERFRAMES_NO_UPDATE_CHECK=1
for b in 01_hook 03_onepass 04_agents 05_head 06_labels; do
  (cd $b && npx --yes --prefer-offline hyperframes@0.8.115 render -o ../media/hf/$b.mp4)
done
uv run --no-sync python ../../tools/assemble.py beats.json \
    --vo ../008-jev-decision-models/vo_final.wav \
    --captions ../008-jev-decision-models/captions.json \
    -o media/jev_hyperframe.mp4
```
