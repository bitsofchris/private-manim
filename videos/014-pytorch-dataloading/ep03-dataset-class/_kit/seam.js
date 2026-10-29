// seam.js — ep 3's seam states: SC.SEAM[n] is the state at cut n (the end of
// beat n and the start of beat n+1); SEAM[0] is frame 0. Loaded after
// ep/ep.js. tools/hf_state_check.js compares a beat's S(0) and S(end) with
// these (merged over SC.REST). The storyboard's seam-states table is the
// prose version of this file.
//
// Two images, never both on screen:
//   machine(hero)          the series machine (SC.REST: map-style, workers 0), hero named
//   card(lines, lit, ...)  the code card over everything (flip 1), fully typed unless `typed` given
(function () {
  const SC = window.SC, EP = window.EP;
  const machine = (hero) => ({ hero, flip: 0, code: { o: 0 } });
  const card = (lines, lit, typed = Infinity, cursor = 0) =>
    ({ flip: 1, hero: null, code: { o: 1, lines, typed, lit, cursor, blink: 0 } });
  // frame 0: the Dataset card already being typed, the last line landing, __getitem__ the hero
  const typed0 = EP.chars(EP.MAP.slice(0, 4)) + 6;
  SC.SEAM = {
    0: card(EP.MAP, "getitem", typed0, 1),   // frame 0: typing the last line
    1: card(EP.MAP, "getitem"),              // "how do I get sample i?": __getitem__ lit
    2: machine(null),                        // "the data loader's job": the stations swept, none left lit
    3: machine("getitem"),                   // "returns sample at index i": __getitem__ on the Dataset card
    4: card(EP.MAP, "getitem"),              // "you can index into the dataset": __getitem__ lit
    5: machine("getitem"),                   // "calls getitem on each one"
    6: machine("sampler"),                   // "a list of indices": the sampler's indices
    7: card(EP.HAND, null),                  // the hand-rolled loop typed, nothing lit
    8: machine("collate"),                   // "plus collate"
    9: card(EP.MAP, "slice"),                // "random access is cheap": the slice
    10: card(EP.MAP, EP.TWO),                // the end: the two functions lit
  };
})();
