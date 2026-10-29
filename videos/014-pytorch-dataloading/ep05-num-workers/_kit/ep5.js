// ep5.js — ep 5's own helpers on the shared kit (loaded after kit/code.js, before ep/seam.js).
// Nothing here draws a new part; it tags and relabels what the shared kit already has.
//
//   EP5.LINES.iterable   DL_DATA.code.iterable, as is (beats 3, 5)
//   EP5.LINES.workers    DL_DATA.code.workers, as is (beat 6: "# True")
//   EP5.LINES.shard      DL_DATA.code.shard, same text, with `lit` tags on the two lines the
//                        VO names: "worker k" -> "k" (start = info.id), "every nth" -> "step"
//   EP5.SHARD3           characters in the first three shard lines (beat 8 ends with them typed,
//                        the "# False" line not yet started)
//   EP5.mount(root)      SC.mount(root), then the batching station's "×32" reads "×4": this
//                        episode's loader is batch_size=4 (the ledger), and the batch card says [4, 512]
//   EP5.draw(kit, S)     kit.draw(null, S), then two fixes the shared kit lacks (both for the update pass):
//                        hero "twins" lights both batch cards (the twin pair is the one hero, not the
//                        second card alone), and a card with a line over 28 characters (the iterable
//                        card's `class Stream(IterableDataset):`, 30) is set at 44 px so it fits
(function () {
  const C = window.SC.D.code, D = window.SC.D;
  const tag = { "start = info.id        # k": "k", "step = info.num_workers": "step" };
  const shard = C.shard.map((ln) => Object.assign({}, ln, tag[ln.t] ? { lit: tag[ln.t] } : {}));
  const SHARD3 = shard.slice(0, 3).reduce((a, l) => a + l.t.length, 0);
  function mount(root) {
    const kit = window.SC.mount(root);
    kit.parts.batching.dom.forEach((el) => { if (el.textContent === "×" + D.series.batch) el.textContent = "×" + D.series.smallBatch; });
    return kit;
  }
  const HERO = window.SC.PAL.hero;
  function draw(kit, S) {
    kit.draw(null, S);
    if (S.hero === "twins") {
      kit.parts.batch.svg.forEach((el) => { if (el.getAttribute("stroke") && el.getAttribute("stroke") !== "none") el.setAttribute("stroke", HERO); });
      kit.parts.batch.dom.forEach((el) => { el.style.color = HERO; });
    }
    const lines = (S.code && S.code.lines) || [];
    const size = lines.some((l) => l.t.length > 28) ? 44 : 48;
    if (kit.code) kit.code.rows.forEach((el) => { el.style.fontSize = `${size}px`; });
  }
  window.EP5 = { LINES: { iterable: C.iterable, workers: C.workers, shard }, SHARD3, mount, draw };
})();
