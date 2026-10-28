// seam.js — ep 1's seam states: SC.SEAM[n] is the state at cut n (the end of
// beat n and the start of beat n+1); SEAM[0] is frame 0. Loaded after
// ep/loop.js. tools/hf_state_check.js compares a beat's S(0) and S(end)
// with these (merged over SC.REST). The storyboard's seam-states table is
// the prose version of this file.
(function () {
  const SC = window.SC, LOOP = window.LOOP, LO = SC.LOOP_ONLY, R = "ring";
  const loop = (u, lit, extra) => Object.assign({}, LO, { loop: Object.assign({ o: 1, take: R, u, batch: 1, slot: 0, lit }, extra || {}) });
  const machine = (hero) => ({ hero, flip: 0, loop: { o: 0 } });
  SC.SEAM = {
    0: loop(0, "batch"),                                   // frame 0: the batch in the DataLoader's slot, about to ride
    1: loop(0, "batch"),                                   // hook done: one lap ridden, parked in the slot
    2: loop(LOOP.at(R, "forward"), "forward"),             // beside forward, forward lit ("makes a prediction")
    3: loop(LOOP.at(R, "loss"), "loss"),                   // beside loss, loss lit
    4: loop(LOOP.at(R, "update"), "step"),                 // beside update, the four boxes lit ("one training step")
    5: loop(0, "batch"),                                   // back in the slot: the next batch, hero
    6: { flip: 1, hero: null, loop: { o: 0 },              // the code card, fully typed, outer loop lit; the machine waits under it
         code: { o: 1, lines: LOOP.CODE, typed: Infinity, lit: "outer", cursor: 0 } },
    7: machine("batch"),                                   // the machine at rest (ep 2's frame 0), the batch hero
    8: machine("batch"),                                   // the end: still
  };
})();
