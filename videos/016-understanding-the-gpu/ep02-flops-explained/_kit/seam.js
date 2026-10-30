// seam.js — ep 2's seam states: SC.SEAM[n] is the state at cut n (the end of
// beat n and the start of beat n+1); SEAM[0] is frame 0. Loaded after
// ep/flops.js. tools/hf_state_check.js compares a beat's S(0) and S(end) with
// these (merged over SC.REST). storyboard.md's seam-states table is the prose
// version of this file.
//
// Every state: the chip with the CPU, its queue and the time strip off (ep 2
// never names them), GPU memory at rest, the lit cells shimmering, and ep 2's
// top card in their place. The Short alternates between the whole chip and the
// inside of one core (core: the arithmetic; float: one number).
(function () {
  const SC = window.SC, FLOPS = SC.D.code.flops;
  const base = { cpu: 0, queueO: 0, strip: 0, shimmer: 1 };
  const st = (o) => Object.assign({}, base, o);
  const card = (A) => ({ o: 1, A, B: null, mix: 0 });
  const CARD_OFF = card(null);
  const acro = (u) => ({ o: 1, u });
  const coreOp = (o) => Object.assign({ o: 1, grow: 1, mode: "op", mul: 0, carry: 0, add: 0, n: 0, lit: null }, o);
  const floatAt = (o) => Object.assign({ o: 1, grow: 1, row1: 1, row2: 0, glide1: 0, glide2: 0, anat: 1, anatO: 1, lab: [1, 1, 1] }, o);
  const code = (lit) => ({ o: 1, lines: FLOPS, typed: FLOPS[0].t.length, lit, cursor: 0, cy: 1245 });
  SC.SEAM = {
    0: st({ hero: "count", card: CARD_OFF, acro: acro(0), core: coreOp({}) }),          // frame 0: inside one core, `1.5 × 2.0`, 0 FLOPs
    1: st({ hero: "chip", card: CARD_OFF, acro: acro(0) }),                              // "all AI compute": back out to the chip
    2: st({ hero: "acronym", card: CARD_OFF, acro: acro(1) }),                           // "floating-point operation"
    3: st({ hero: "exp", card: CARD_OFF, acro: acro(1), float: floatAt({}) }),           // "an exponent"
    4: st({ hero: "exp", card: CARD_OFF, acro: acro(1), float: floatAt({}) }),           // = SEAM[3]: beat 04 ("the point floats ... three million") was cut, 03 runs straight into 05
    5: st({ hero: "hbm", card: card({ kind: "word", word: "gradients" }) }),             // "gradient is one of these numbers"
    6: st({ hero: null, card: card({ kind: "count", o2: 1 }), code: code("count") }),    // "720 trillion FLOPs"
    7: st({ hero: "clock", card: card({ kind: "rate", clock: 1, clockO: 1 }), code: code(null) }),  // "This is a rate."
    8: st({ hero: "chip", lit: 1, card: card({ kind: "matmul" }) }),                     // "thousands at once"
    9: st({ hero: "bill", lit: 1, card: card({ kind: "frac", dollar: 1 }) }),            // "This is the bill": the end
  };
})();
