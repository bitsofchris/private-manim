// data.js — the ledger of the PyTorch Dataloading series (SERIES.md), as the
// kit draws it. Every string and number a beat shows comes from here; a beat
// never types a new one. Loaded before machine.js.
window.DL_DATA = {
  series: { points: 512, nSeries: 512, batch: 32, workers: 2, smallBatch: 4, shape: "[32, 512]", smallShape: "[4, 512]",
            // The first values of the first three series (the ledger's readout; one decimal, true minus signs), so a
            // batch on screen is rows of numbers in brackets (agents/style.md "Vectors and matrices as numbers"), not a picture.
            // four rows: the card and the batching station show the first three; a glyph shows two (batch n = rows 2n, 2n+1)
            readout: [["0.3", "\u22121.2"], ["0.7", "0.1"], ["\u22120.8", "0.5"], ["1.4", "\u22120.2"]] },
  // The sampler's glyph: a shuffled run of indices (the ledger's RandomSampler, seed 77, first six).
  indices: [7, 2, 5, 0, 3, 1],
  // Method names shown on the Dataset card.
  methods: { map: ["__len__", "__getitem__"], iterable: ["__iter__"] },
  // Code cards (≤ 28 characters a line at 52 px monospace; two-space indents). `lit` names the station
  // or part the line lights when typed (the magenta hero passes to it).
  code: {
    loader: [
      { t: "loader = DataLoader(dataset,", lit: "dataset" },
      { t: "  batch_size=32,", lit: "batching" },
      { t: "  shuffle=True,", lit: "sampler" },
      { t: "  num_workers=2)", lit: "fetch" },
    ],
    loop: [
      { t: "for batch in loader:", lit: "batch" },
      { t: "  out = model(batch)", lit: "model" },
      { t: "  loss = loss_fn(out, y)", lit: null },
      { t: "  loss.backward()", lit: null },
      { t: "  optimizer.step()", lit: null },
    ],
    mapStyle: [
      { t: "class Series(Dataset):", lit: "dataset" },
      { t: "  def __len__(self):", lit: "len" },
      { t: "    return len(self.series)", lit: null },
      { t: "  def __getitem__(self, i):", lit: "getitem" },
      { t: "    return self.series[i]", lit: "slice" },   // ep 3: "getitem is just a slice"
    ],
    handRolled: [
      { t: "perm = torch.randperm(n)", lit: "sampler" },
      { t: "for i in range(0, n, 32):", lit: "batching" },
      { t: "  idx = perm[i : i + 32]", lit: null },
      { t: "  batch = data[idx]", lit: "collate" },
    ],
    iterable: [
      { t: "class Stream(IterableDataset):", lit: "dataset" },
      { t: "  def __iter__(self):", lit: "iter" },
      { t: "    while True:", lit: null },
      { t: "      yield next_series()", lit: null },
    ],
    workers: [
      { t: "loader = DataLoader(stream,", lit: "dataset" },
      { t: "  batch_size=4,", lit: "batching" },
      { t: "  num_workers=2)", lit: "fetch" },
      { t: "torch.equal(b1, b2)  # True", lit: "twins" },
    ],
    shard: [
      { t: "info = get_worker_info()", lit: "fetch" },
      { t: "start = info.id        # k", lit: null },
      { t: "step = info.num_workers", lit: null },
      { t: "torch.equal(b1, b2)  # False", lit: "twins" },
    ],
  },
};
