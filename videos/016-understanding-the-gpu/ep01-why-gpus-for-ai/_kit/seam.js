// seam.js — ep 1's seam states: SC.SEAM[n] is the state at cut n (the end of
// beat n and the start of beat n+1); SEAM[0] is frame 0. Loaded after
// ep/ep.js. tools/hf_state_check.js compares a beat's S(0) and S(end) with
// these (merged over SC.REST, which ep.js extends). The storyboard's
// seam-states table is the prose version of this file.
(function () {
  const SC = window.SC;
  const ALL = "1".repeat(16), NONE = "0".repeat(16);
  const card = { o: 1, lines: SC.D.code.matmul, typed: Infinity, lit: "at", cursor: 0, cy: 1246 };
  SC.SEAM = {
    // frame 0: already working; the grid shimmering at rest, the CPU's 4 cores lit, y = x @ W empty; the grid the hero
    0: { lit: SC.D.run.mfu, shimmer: 1, hero: "chip", fill: NONE },
    // "all happen at the same time": every cell lit, every y cell done
    1: { lit: 1, hero: "chip", fill: ALL },
    // "none of them waits on the other": every y cell done at once, the y cells the hero
    2: { lit: 1, hero: "y", fill: ALL },
    // "a few at a time": the CPU big in the chip's place (chip and memory hidden), 3 of 4 rows done
    3: { lit: 0, chip: 0, hbm: 0, big: 1, cache: 1, branch: 1, hero: "cpu", fill: "1".repeat(12) + "0000" },
    // "all working at once": the CPU back in the top slot, every cell lit, every y cell done
    4: { lit: 1, cache: 1, branch: 1, hero: "chip", fill: ALL },
    // "in one step": tensor cores emphasised and the hero
    5: { lit: 1, cache: 1, branch: 1, tc: 1, hero: "tc", title: "tensor cores", fill: ALL },
    // the end, "runs the whole grid": the code card in the bottom slot, `y = x @ W` lit
    6: { lit: 1, cache: 1, branch: 1, hero: null, mat: 0, fill: ALL, code: card },
  };
})();
