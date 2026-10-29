// data.js — the ledger of the Understanding the GPU series (SERIES.md), as the
// kit draws it. Every string and number a beat shows comes from here; a beat
// never types a new one. Loaded before chip.js.
window.GPU_DATA = {
  // The chip: a picture, not a count (SERIES.md: the SM count is never stated).
  chip: { n: 12, title: "GPU" },
  // MFU and GPU-Util on the same run (ledger: 720 TFLOPS of 2,250 → 32 %; nvidia-smi 100 %).
  run: { mfu: 0.32, mfuText: "32%", util: "GPU-Util 100%" },
  // HBM (high-bandwidth memory) is the GPU's own memory; the take never says "HBM", so the slab says "GPU memory".
  hbm: { name: ["GPU", "memory"], size: "180 GB", bw: "8 TB/s" },
  // Kernel tiles in the queue, everywhere (SERIES.md "Kernel-tile labels").
  queue: ["matmul", "add", "relu", "∇", "adam"],
  // Code cards: real lines that run. ≤ 36 characters a line fits the card at
  // 40 px; longer lines shrink the whole card's type (kit/code.js), so keep
  // to 36. `lit` names the part the line lights when it is the hero.
  code: {
    matmul: [                                   // ep 1
      { t: 'x, W = x.to("cuda"), W.to("cuda")', lit: "chip" },
      { t: "y = x @ W", lit: "at" },
    ],
    flops: [                                    // ep 2
      { t: "flops = 6 * 8e9 * 15_000  # 7.2e14", lit: "count" },
      { t: "seconds = flops / 2250e12  # 0.32", lit: "rate" },
    ],
    sixN: [                                     // ep 3
      { t: "flops = 6 * n_params * n_tokens", lit: "sixN" },
      { t: "6 * 8e9 * 15_000  # 7.2e14 /s", lit: "run" },
    ],
    autocast: [                                 // ep 4
      { t: 'with torch.autocast("cuda",', lit: null },
      { t: "    dtype=torch.bfloat16):", lit: "bf16" },
      { t: "  loss = model(x)", lit: null },
      { t: "loss.backward()", lit: null },
    ],
    bound: [                                    // ep 5
      { t: "y = x @ W   # ~1,640 FLOPs/byte", lit: "matmul" },
      { t: "y = torch.relu(x)  # 0.25", lit: "relu" },
    ],
    step: [                                     // eps 6–8: the series training step
      { t: "loss = loss_fn(model(x), y)", lit: "forward" },
      { t: "loss.backward()", lit: "backward" },
      { t: "opt.step()", lit: "update" },
      { t: "print(loss.item())", lit: "sync" },
    ],
    mfu: [                                      // ep 7
      { t: "flops = 6 * 8e9 * 15_000  # 7.2e14", lit: null },
      { t: "mfu = flops / 2250e12", lit: "mfu" },
      { t: "# 0.32", lit: "mfu" },
    ],
    // ep 8's profiler block is 80+ characters a line in its storyboard;
    // the ep 8 session cuts it to phone width and adds it here via its own _kit/.
  },
};
