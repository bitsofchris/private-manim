// seam.js — ep 5's seam states: SC.SEAM[n] is the state at cut n (the end of
// beat n and the start of beat n+1); SEAM[0] is frame 0. Loaded after
// ep/ep5.js. tools/hf_state_check.js compares a beat's S(0) and S(end) with
// these (merged over SC.REST). The storyboard's seam-states table is the prose
// version of this file.
//
// Every state carries the whole machine, also under the code card (flip 1), so
// a flip back lands on exactly the machine the table names.
//   trap(hero)        iterable, sampler struck, two workers, twin [4, 512] batches (the trap)
//   map(hero)         map-style, sampler back, two workers, one batch (beat 4: "you're fine")
//   fixed(hero)       the trap's machine after the fix: one batch on the card, no twin (beats 8–10)
//   card(m, lines, lit, typed)   machine m under the code card (flip 1)
(function () {
  const SC = window.SC, L = window.EP5.LINES, small = SC.D.series.smallShape;
  const base = { workers: 2, shape: small, flip: 0, code: { o: 0 } };
  const trap = (hero) => Object.assign({}, base, { mode: "iterable", strike: 1, twins: 1, hero });
  const map = (hero) => Object.assign({}, base, { mode: "map", strike: 0, twins: 0, hero });
  const fixed = (hero) => Object.assign({}, base, { mode: "iterable", strike: 1, twins: 0, hero });
  const card = (m, lines, lit, typed = Infinity) => Object.assign({}, m, { flip: 1, code: { o: 1, lines, typed, lit, cursor: 0 } });
  SC.SEAM = {
    0: trap("twins"),                                       // frame 0: the twin batches, samples hopping
    1: trap("fetch"),                                       // "num_workers": the fetch station, two photocopies
    2: trap("collate"),                                     // "fetching and collating on its own"
    3: trap("twins"),                                       // "they all deliver the same data" (back from the iterable card)
    4: map("batch"),                                        // "every sample here gets fetched once": one batch
    5: trap("twins"),                                       // "you're getting the same data": the twin slides back in
    6: card(trap("twins"), L.workers, "twins"),             // "identical": torch.equal(b1, b2)  # True
    7: trap("iter"),                                        // "inside your iter function"
    8: card(fixed("fetch"), L.shard, ["k", "step"], window.EP5.SHARD3),  // "every nth sample, starting at k"
    9: card(fixed("fetch"), L.shard, "twins"),              // "nothing is delivered twice": # False
    10: card(fixed("fetch"), L.shard, "fetch"),             // the end: info = get_worker_info() lit
  };
})();
