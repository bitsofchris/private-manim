// seam.js — ep 1's seam states: SC.SEAM[n] is the state at cut n (the end of
// beat n and the start of beat n+1); SEAM[0] is frame 0. Loaded after
// ep/loop.js. tools/hf_state_check.js compares a beat's S(0) and S(end)
// with these (merged over SC.REST). The storyboard's seam-states table is
// the prose version of this file.
//
// Three images, each a state shape:
//   machine(hero)        the series machine at rest (SC.REST), hero named
//   loop(u, lit)         the training-loop image alone (machine off), glyph at u
//   card(lines, lit)     the code card over everything (flip 1), fully typed
(function () {
  const SC = window.SC, LOOP = window.LOOP, LO = SC.LOOP_ONLY, R = "ring";
  const loop = (u, lit) => Object.assign({}, LO, { loop: { o: 1, take: R, u, batch: 1, slot: 0, lit } });
  const machine = (hero) => ({ hero, flip: 0, loop: { o: 0 } });
  const next = (s) => { s.loop = Object.assign({}, s.loop, { n: 1 }); return s; };
  const card = (lines, lit) => ({ flip: 1, hero: null, loop: { o: 0 }, code: { o: 1, lines, typed: Infinity, lit, cursor: 0 } });
  SC.SEAM = {
    0: machine("batch"),                                   // frame 0: the series image, samples hopping, the batch hero
    1: machine("batch"),                                   // "packed into one tensor": still the machine
    2: loop(0, "batch"),                                   // the loop is up, the batch in the slot
    3: loop(LOOP.at(R, "forward"), "forward"),             // beside forward, forward lit
    4: card(LOOP.BODY, "loss"),                            // the four lines, loss lit
    5: loop(LOOP.at(R, "update"), "update"),               // beside update, update lit
    6: card(LOOP.BODY, LOOP.STEP),                         // the four lines lit together: one training step
    7: next(loop(0, "batch")),                             // the next batch in the slot: a different one (n 1), the used one gone
    8: card(LOOP.CODE, "outer"),                           // six lines, the outer loop lit
    9: machine("batch"),                                   // the machine, the batch hero
    10: machine("batch"),                                  // same, after the pulse
    11: card(LOOP.CODE, LOOP.STEP),                        // the end: six lines, the four lit
  };
})();
