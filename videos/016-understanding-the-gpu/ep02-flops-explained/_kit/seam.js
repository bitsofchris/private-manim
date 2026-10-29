// seam.js — ep 2's seam states: SC.SEAM[n] is the state at cut n (the end of
// beat n and the start of beat n+1); SEAM[0] is frame 0. Loaded after
// ep/flops.js. tools/hf_state_check.js compares a beat's S(0) and S(end) with
// these (merged over SC.REST). storyboard.md's seam-states table is the prose
// version of this file.
//
// Every state: the chip with the CPU, its queue and the time strip off (ep 2
// never names them), GPU memory at rest, the lit cells shimmering, and ep 2's
// top card in their place.
(function () {
  const SC = window.SC, FLOPS = SC.D.code.flops;
  const base = { cpu: 0, queueO: 0, strip: 0, shimmer: 1 };
  const st = (o) => Object.assign({}, base, o);
  const card = (A) => ({ o: 1, A, B: null, mix: 0 });
  const NAME = { kind: "name" };
  const floatAt = (o) => Object.assign({ o: 1, grow: 1, row1: 1, row2: 0, glide1: 0, glide2: 0, anat: 1, anatO: 1, lab: [1, 1, 1] }, o);
  const code = (lit) => ({ o: 1, lines: FLOPS, typed: FLOPS[0].t.length, lit, cursor: 0, cy: 1245 });
  SC.SEAM = {
    0: st({ hero: "count", card: card({ kind: "op", n: 0, lit: null }) }),                  // frame 0: the counter at 0
    1: st({ hero: "count", card: card({ kind: "op", n: 2, lit: null }) }),                  // "one add": 2 FLOPs
    2: st({ hero: "acronym", card: card(NAME) }),                                            // "floating-point operation"
    3: st({ hero: "exp", card: card(NAME), float: floatAt({}) }),                            // "an exponent"
    4: st({ hero: "exp", card: card(NAME), float: floatAt({ row2: 1, glide1: 1, glide2: 1, anat: 2 }) }),  // "three million"
    5: st({ hero: "hbm", card: card({ kind: "word", word: "gradients" }) }),                 // "gradient is one of these numbers"
    6: st({ hero: null, card: card({ kind: "count", o2: 1 }), code: code("count") }),        // "720 trillion FLOPs"
    7: st({ hero: "tera", title: "B200", card: card({ kind: "rate", step: 2 }), code: code(null) }),   // "Tera is a trillion"
    8: st({ hero: "chip", title: "B200", lit: 1, card: card({ kind: "matmul", step: 1 }) }), // "thousands at once"
    9: st({ hero: "bill", title: "B200", lit: 1, card: card({ kind: "frac", dollar: 1 }) }), // "This is the bill": the end
  };
})();
