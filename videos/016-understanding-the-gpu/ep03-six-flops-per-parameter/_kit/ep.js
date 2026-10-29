// ep.js — every string and number ep 3 shows beyond the series kit (storyboard.md "Ledger").
// A beat never types a new one. Loaded after ../_kit/data.js.
window.EP = {
  inName: "x", outName: "y",                 // the tiny layer: x1 x2 x3 → y1 y2, six weights
  errIn: "dx", errOut: "dy",                 // the backward pass's error at each end
  hook: "6 × params",                        // the readout at frame 0
  count: (n) => `${n} FLOPs`,                // the readout while counting: 12, 24, 36 (a count: FLOPs)
  total: "36 = 6 × 6",                       // beat 06
  eq: { fwd: "y = W x", back: "dx = Wᵀ dy", grad: "dW = dy xᵀ" },
  bar: { fwd: "→ 2", back4: "← 4", back2: "← 2" },
  times: "×", plus: "+",
  run: "720 TFLOPS",                         // 6 × 8e9 × 15,000 = 7.2e14 FLOP/s (a rate: FLOPS)
};
