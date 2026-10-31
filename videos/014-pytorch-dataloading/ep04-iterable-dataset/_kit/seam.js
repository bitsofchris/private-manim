// seam.js — ep 4's seam states: SC.SEAM[n] is the state at cut n (the end of
// beat n and the start of beat n+1); SEAM[0] is frame 0. Loaded after
// ep/ep4.js. tools/hf_state_check.js compares a beat's S(0) and S(end) with
// these (merged over SC.REST). The storyboard's seam-states table is the
// prose version of this file.
//
// Two images, never both:
//   machine(hero, extra)   the iterable machine: sampler struck, `__iter__` on the card
//   card(lines, lit)       the code card (flip 1), fully typed, cursor off
//   stream(extra)          the stream (ep/stream.js), the machine faded under it (hero null)
(function () {
  const SC = window.SC, EP4 = window.EP4;
  const machine = (hero, extra) => Object.assign({ mode: "iterable", strike: 1, workers: 0, hero, flip: 0, shards: { o: 0 } }, extra || {});
  const card = (lines, lit) => ({ mode: "iterable", strike: 1, workers: 0, hero: null, flip: 1, shards: { o: 0 },
                                  code: { o: 1, lines, typed: Infinity, lit, cursor: 0 } });
  // the machine's opacities are 0 under the stream (ep4.js also fades them by stream.o, for crossfades)
  const stream = (extra, m) => machine(null, Object.assign({ dataset: 0, loader: 0, batch: 0, model: 0,
                                                             stream: Object.assign({ o: 1 }, extra) }, m || {}));
  SC.SEAM = {
    0: machine("iter"),                                            // frame 0: iterable, sampler struck, __iter__ the hero
    1: machine("iter"),                                            // "…you use an iterable dataset."
    2: card(EP4.ITER, "yield"),                                    // the class typed, the yield line lit
    3: stream({ hero: "shards" }),                                 // "…pack the data into shards and just stream them through"
    4: card(EP4.LEN, "yield"),                                     // len(stream) # TypeError typed; "until the iterator produces it"
    5: stream({ hero: "iter", ask: 1 }),                           // the loader calls next(); "…it yields the next sample"
    6: stream({ hero: "iter", order: [2, 0, 1], load: 1 }),        // pre-shuffled, shard 2 in memory; "yield from it"
    7: stream({ hero: "split", order: [2, 0, 1], lanes: 1 }, { workers: 2 }),   // forked to two workers' __iter__; who reads what? (machine, hidden: workers 2)
    8: machine("batch", { workers: 2 }),                           // back on the machine: "same batch out"
    9: card(EP4.CMP, "getitem"),                                   // not "the sample at index i"
    10: machine("iter"),                                           // swapped: back to frame 0
  };
})();
