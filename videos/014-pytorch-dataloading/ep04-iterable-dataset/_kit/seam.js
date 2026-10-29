// seam.js — ep 4's seam states: SC.SEAM[n] is the state at cut n (the end of
// beat n and the start of beat n+1); SEAM[0] is frame 0. Loaded after
// ep/ep4.js. tools/hf_state_check.js compares a beat's S(0) and S(end) with
// these (merged over SC.REST). The storyboard's seam-states table is the
// prose version of this file.
//
// Two images, never both:
//   machine(hero, extra)   the iterable machine: sampler struck, `__iter__` on the card
//   card(lines, lit)       the code card (flip 1), fully typed, cursor off
(function () {
  const SC = window.SC, EP4 = window.EP4;
  const ON = { o: 1, order: [0, 1, 2], load: 0, hero: 0 };
  const SHUF = { o: 1, order: [2, 0, 1], load: 1, loadCard: 2, hero: 0 };   // after the pre-shuffle, card 2 (now first) loaded
  const machine = (hero, extra) => Object.assign({ mode: "iterable", strike: 1, workers: 0, hero, flip: 0, shards: { o: 0 } }, extra || {});
  const card = (lines, lit) => ({ mode: "iterable", strike: 1, workers: 0, hero: null, flip: 1, shards: { o: 0 },
                                  code: { o: 1, lines, typed: Infinity, lit, cursor: 0 } });
  SC.SEAM = {
    0: machine("iter"),                                            // frame 0: iterable, sampler struck, __iter__ the hero
    1: machine("iter"),                                            // "…you use an iterable dataset."
    2: card(EP4.ITER, "yield"),                                    // the class typed, the yield line lit
    3: machine(null, { shards: Object.assign({}, ON, { hero: 1 }) }),   // the shards up, the hero
    4: card(EP4.LEN, "yield"),                                     // len(stream) # TypeError typed; "until the iterator produces it"
    5: machine("iter", { shards: ON }),                            // "…it yields the next sample"
    6: machine("iter", { shards: SHUF }),                          // shuffled, one shard loaded; "yield from it"
    7: machine("fetch", { shards: SHUF, workers: 2 }),             // two workers
    8: machine("batch", { shards: SHUF, workers: 2 }),             // "same batch out"
    9: card(EP4.CMP, "getitem"),                                   // not "the sample at index i"
    10: machine("iter"),                                           // swapped: back to frame 0
  };
})();
