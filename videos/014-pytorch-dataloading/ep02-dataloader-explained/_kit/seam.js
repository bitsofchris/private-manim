// seam.js — ep 2's seam states: SC.SEAM[n] is the state at cut n (the end of
// beat n and the start of beat n+1); SEAM[0] is frame 0. Loaded after
// kit/code.js. tools/hf_state_check.js compares a beat's S(0) and S(end)
// with these (merged over SC.REST). The storyboard's seam-states table is
// the prose version of this file.
//
// Two images, each a state shape:
//   machine(hero, workers)   the series machine (SC.REST), hero named, N worker photocopies
//   card(lit)                the loader call on the code card (flip 1), fully typed, `lit` the hero line
(function () {
  const SC = window.SC, LOADER = SC.D.code.loader;
  const machine = (hero, workers = 0) => ({ hero, workers, flip: 0 });
  // hero "dataset" under the card, so the flip back to the machine lands on the Dataset card lit
  const card = (lit) => ({ hero: "dataset", workers: 0, flip: 1, code: { o: 1, lines: LOADER, typed: Infinity, lit, cursor: 0 } });
  SC.SEAM = {
    0: machine("batch"),            // frame 0: the machine running, samples hopping, the batch hero
    1: machine("batch"),            // "hand back a batch"
    2: machine(null),               // "four different stations": the ripple has run, no station lit
    3: card("dataset"),             // the loader call typed; "your dataset sits at the front": its line lit
    4: machine("dataset"),          // "go get one sample": the Dataset card
    5: machine("sampler"),          // "a random sequence of indices"
    6: machine("fetch", 2),         // "in parallel if you ask for them": two workers
    7: machine("batching", 2),      // "batch-sized samples"
    8: machine("batch", 2),         // "one tensor shaped for the GPU": the batch card
    9: machine("model", 2),         // the end: "the forward pass", the model chip
  };
})();
