// seam.js — ep 4's seam states: SC.SEAM[n] is the state at cut n (the end of
// beat n and the start of beat n+1); SEAM[0] is frame 0. Loaded after
// ep/ep.js. tools/hf_state_check.js compares a beat's S(0) and S(end) with
// these (merged over SC.REST, which ep.js extends). The storyboard's
// seam-states table is the prose version of this file.
(function () {
  const SC = window.SC, run = SC.D.run;
  const card = { o: 1, lines: SC.D.code.autocast, typed: Infinity, lit: "bf16", cursor: 0, cy: 1190 + window.EP.LIFT };
  SC.SEAM = {
    // frame 0: already working; chip view, fp32 / fp16 / bf16 / fp8 small in the top slot, the grid shimmering, bf16 the hero
    0: { lit: run.mfu, shimmer: 1, hero: "row:bf16" },
    // "half the bits of fp32": unchanged, bf16 still the hero
    1: { lit: run.mfu, shimmer: 1, hero: "row:bf16" },
    // "multiply-adds per tensor core cycle": every cell holds 2 numbers, tensor cores emphasised and the hero
    2: { lit: run.mfu, shimmer: 1, split: 1, tc: 1, hero: "tc", title: "tensor cores" },
    // "fp8 doubles that": 4 numbers a cell, the ladder full, the fp8 rung (and fp8's row label) the hero
    3: { lit: run.mfu, shimmer: 1, split: 2, ladder: 1, rungs: 3, hero: "rung:fp8" },
    // "will overflow": bits view (chip faded), the 1/3 column, 70,000 in fp32 and "inf" in fp16; "inf" the hero
    4: { lit: run.mfu, shimmer: 1, split: 1, view: 1, colA: 1, big: 1, inf: 1, hero: "inf" },
    // "training stays stable": bf16's 70,144 in, both exponent fields outlined, bf16's exponent (+ its 70,144) the hero
    5: { lit: run.mfu, shimmer: 1, split: 1, view: 1, colA: 1, big: 1, inf: 1, bigb: 1, same: 1, hero: "exp:bf16" },
    // "Transformer Engine": outlines off, fp8's "max 448" and the scale tag in; the tag the hero
    6: { lit: run.mfu, shimmer: 1, split: 1, view: 1, colA: 1, big: 1, inf: 1, bigb: 1, big8: 1, scale: 1, hero: "scale" },
    // the end: chip view lifted, bf16 alone in the top slot, 2 numbers a cell, the autocast card, dtype line lit
    7: { lit: run.mfu, shimmer: 1, split: 1, close: 1, o32: 0, o16: 0, o8: 0, hero: "code", code: card },
  };
})();
