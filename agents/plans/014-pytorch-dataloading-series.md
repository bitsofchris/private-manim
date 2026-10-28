# Plan: the PyTorch Dataloading series (014), cut from the 2026-07-24 take

**Name:** pytorch-dataloading-series-plan
**Description:** How to turn the published long video "PyTorch Dataloading:
Map vs Iterable Datasets Explained" (8.7 min, 88 views, cut from a 24-min
take) into a series of self-contained Shorts, each found by its own search
phrase, reusing Chris's recorded lines where they stand alone and the two
diagrams as the recurring image. Status: **draft for Chris, 2026-10-25.**
Nothing is agreed yet; the decisions he owns are listed at the end.
**When to use:** at the start of the 014 series. Once the decisions are
made, this becomes `videos/014-pytorch-dataloading/SERIES.md` (the
`agents/series.md` shape) and this plan moves to `agents/archive/`.
**How it works:** `agents/series.md` runs the series; `agents/runbook.md`
runs each episode. The only new thing here is step 3–4 of the series
process: the "one recording" already exists, so the split is a mine of a
lecture take, not of a scripted read.

## What exists

| Thing | Where | Use |
|---|---|---|
| The take, Studio Sound, 1430.6 s | `~/Creating/pytorch dataloading/edit/studio-sound-Chris Lettieri.m4a` | VO source. Runbook step 3 is loudnorm only (Studio Sound, never denoise) |
| Transcript, Parakeet v3, timestamped | `videos/014-pytorch-dataloading/TRANSCRIPT-lecture-2026-07-24.md` | the line mine below; times are seconds into the m4a |
| Camera + screen recordings, same clock | `…/edit/Chris Lettieri.mp4`, `…/edit/Chris Lettieri's screen.mp4` | the web-UI training footage (17:29–23:13 of the take) if a Short wants real footage on top, kb-graph style |
| Descript edit | `…/edit/edit.xml` | what the long video kept: 298.5–1424.0 s, 520 s after cuts |
| Diagram 1: the training loop | `…/ChatGPT Image … 08_26_44 AM.png` | six boxes (DataLoader → forward → loss → backward → update → log) over the pseudo-code; ep 1's image |
| Diagram 2: how a batch is produced | `…/ChatGPT Image … 08_26_59 AM.png` | sampler → map-style Dataset → DataLoader (fetch/workers, batching, collation, output) → batch; iterable Dataset feeds in with no sampler; the series image |
| Diagram notes, states A and B | `~/repos/deep-learning/code/18_time-series-transformer-from-scratch/dataloading_diagram.md` | process boundaries: worker boxes as photocopies of the Dataset; "that line IS this box" (each DataLoader argument is one box) |
| Notebook 1, map vs iterable | `…/dataloading_1_map_vs_iterable.ipynb` + `tst_data.py` | every code card and every number below comes from here (the ledger) |
| Notebook 2, torchdata.nodes | `…/dataloading_2_torchdata_nodes.ipynb` | a second series, not this one (see "Out of scope") |
| Video intros note | `…/dataloading_video_intros.md` | Chris's tightened structure; "NanoTST stays out of titles" |

## Who it is for, the promise

Someone writing their first real PyTorch training script who has typed
`DataLoader(dataset, batch_size=32, shuffle=True)` from a tutorial and
cannot say what it does, which of the two Dataset classes to subclass, or
why `num_workers=4` sometimes hands the model the same batch four times.

**Promise:** the Dataset hands back one sample; the DataLoader is the
machinery that turns "one sample" into a batch tensor. Every argument you
pass it is one box in that machine, and knowing the boxes tells you which
Dataset to write and what `num_workers` really does.

## The ledger (identical in every episode)

Taken from notebook 1 and `tst_data.py`; no beat invents a number.

- **The data:** synthetic time series, **512 points** each (16 patches of
  32); a `SeriesDataset` of **512 series**, seed 77.
- **The loader:** `DataLoader(dataset, batch_size=32, shuffle=True,
  drop_last=True)`. **One batch is `[32, 512]`.**
- **The hand-rolled loop** (`nano_tst.train_model`): `perm =
  torch.randperm(len(data))`, `for i in range(0, len(data) - batch_size,
  batch_size)`, `data[perm[i : i + batch_size]]`. Names: randperm = the
  RandomSampler; the range step = the batch sampler with `drop_last=True`;
  the slice = `__getitem__` + collate fused.
- **Map-style:** `__len__` + `__getitem__`, 13 lines (`SeriesDataset`).
- **Iterable:** `__iter__` only, `SyntheticSeriesStream`; `len(stream)`
  raises `TypeError`.
- **The worker trap:** `DataLoader(SyntheticSeriesStream(seed=77),
  batch_size=4, num_workers=2)`: `torch.equal(b1, b2)` is **True**. With
  `shard_per_worker=True` (worker k takes k, k+N, k+2N via
  `get_worker_info()`): **False**.
- **Splits:** `Subset(dataset, indices)`; train 460, val 52.
- **The model:** "a tiny time-series transformer" in VO; never "NanoTST" in
  a title (zero search volume). 807,872 params; losses 1.68 → 1.30 over
  three epochs of 14 steps.
- **Key sentence (Chris, 21:04):** "The dataset's job is to yield one
  sample from your dataset wherever that lives. The data loader's job is to
  take that dataset, call it however many times it needs to, batch all
  that data, group it into a ready-made tensor, and produce a batch."

## The two recurring images

1. **The machine** (diagram 2, redrawn in the house style): a left-to-right
   pipe. Left, yours: the Dataset card (map-style, with a sampler feeding
   it indices; or iterable, with no sampler). Middle, the DataLoader's
   dashed box with four stations: fetch/workers, batching (a stack of N
   samples), collate (samples stacked into one `[32, 512]` tensor),
   output. Right: the batch tensor, then the model. Frame 0 of eps 2–5,
   already running: samples flowing one at a time into the box, a batch
   leaving it. The **magenta hero** is whatever the VO names: the batch,
   the sampler, `__getitem__`, the twin batches.
2. **The code card in the band**, the "hyperframes with code" angle
   (`prototypes/hyperframes/kb-code/`): the editor types the real lines from
   notebook 1, and as each argument lands its box in the machine lights.
   `batch_size=32` → batching; `shuffle=True` → the sampler; `drop_last` →
   the batcher's stop; `num_workers=2` → two photocopies of the Dataset
   card. That is `dataloading_diagram.md`'s "that line IS this box", and it
   is why the channel's code Shorts hold people (runbook, "Why this
   shape").

Both are built **once**, at the series root, before any episode session:
`_kit/machine.js` (the pipe, its stations, seam states: sampler on/off,
N worker clones, the batch tensor) and `_kit/code.js` (the typed card),
plus `00_layout/` approved by Chris. `agents/series.md` step 5 says why
(013 built five copies of one image).

Engine: `ENGINE: hyperframes` for every episode. Nothing here needs axes.
The one-series-plot (ep 1's loss curve, if used) is drawn on the canvas
from the notebook's three numbers, not in Manim (AGENTS.md, one engine per
Short).

## The episodes

Search phrases checked in YouTube autocomplete, 2026-10-25.

| # | Folder | Search phrase (title starts with it) | Their question | VO line 1 (the answer) | Hero | Code beat |
|---|---|---|---|---|---|---|
| 1 | `ep01-training-loop` | **pytorch training loop explained** (autocompletes; "pytorch training loop" too) | What happens in one training step? | A batch is just a bunch of samples packed into one tensor so the GPU can parallelize, and one training step is what happens to it. | the batch, riding the loop | `for batch in loader:` + forward / loss / backward / step (diagram 1's pseudo-code, 8 lines) |
| 2 | `ep02-dataloader-explained` | **pytorch dataloader explained** (autocompletes; also "pytorch dataset dataloader") | What does the DataLoader actually do? | The dataset's job is to yield one sample; the data loader's job is to call it as many times as it needs and hand back a batch. | the batch tensor leaving the box | `DataLoader(dataset, batch_size=32, shuffle=True, drop_last=True)`, each argument lighting its station |
| 3 | `ep03-dataset-class` | **pytorch dataset class** (autocompletes; "pytorch custom dataset" too) | How do I write a custom Dataset? | Two functions: `__len__` and `__getitem__`, and the sampler owns the order. | `__getitem__(idx)` | `SeriesDataset`, 13 lines; then the hand-rolled loop with its three parts named (randperm = sampler) |
| 4 | `ep04-iterable-dataset` | **pytorch iterable dataset** (does **not** autocomplete; see risk) | When do I need an IterableDataset? | When looking up sample *i* isn't cheap, you implement `__iter__` and just yield samples: no length, no sampler, the order is yours. | `__iter__`, with the sampler crossed out | `SyntheticSeriesStream.__iter__`; `len(stream)` → `TypeError` |
| 5 | `ep05-num-workers` | **pytorch dataloader num_workers** (autocompletes) | Why does num_workers give me duplicate data? | Every worker gets its own copy of your dataset; with a sampler the indices are split, with an iterable each copy runs the whole stream. | the two identical batches | `num_workers=2` → `torch.equal(b1, b2)` **True**; `get_worker_info()` shard → **False** |
| 6 (optional) | `ep06-collate-fn` | **pytorch collate_fn** (autocompletes) | What is collate_fn? | Collate packs the samples into one tensor of the shape the GPU wants. | the stack becoming `[32, 512]` | `default_collate` on 32 `[512]` tensors; one custom `collate_fn` |

**Order and dependence.** Each is found alone (62 % of Shorts views come
from search), so none says "last episode". Ep 2 is the series image at
full width; eps 3–5 each zoom one station. Ep 1 is the on-ramp from the
channel's best search term ("pytorch") and ends on the batch arriving, which
is ep 2's frame 0. Ep 4's closer is the decision rule, "map until you
can't", said once in the series (series rule: one home per sentence).

**Risks, by episode**

- Ep 4: nobody types "pytorch iterable dataset" into YouTube. Options:
  (a) ship it anyway, titled `PyTorch IterableDataset Explained (When Map
  Style Won't Work)` and judge it at day 10; (b) merge 4 into 5 under the
  "num_workers" phrase, which is where the iterable story bites. I'd ship
  (a): the concept needs a home, and 5 stays one idea.
- Ep 6: only 16 s of the take covers collate (8:05–8:24) and both readings
  are deictic. It needs a re-record or stays optional.
- Ep 1 is not "dataloading", but it is the phrase people type and it is
  diagram 1 verbatim. Cut it if the series should stay strictly on topic.

## The VO: reuse the take, or re-record from it

Chris asked to reuse the audio. It works where a Short can be built from
6–10 of his sentences that stand alone; it fails where a line points at
the screen ("you see here", "this diagram", "right here"). The take is a
lecture, so about half the lines do. Runbook rule: cut and reorder, never
reword; what was said is the VO. Spliced lines from different minutes of
a take sound fine when tone and level match (013's context splice did
not: it was recorded as an aside). Everything below is one sitting, same
mic, Studio Sound, so the splices should hold; the cut list will tell.

Candidate lines per episode (seconds into the m4a; `~` = contains a
deictic word that a cut may remove; **bold** = line 1):

**Ep 1, training loop** (≈ 50 s available)
- **21:25.9–21:32.5** "A batch is just a bunch of samples packed into a ready-made tensor for the GPU to be able to parallelize its calculations."
- 05:08.7–05:17.1 "the data loader is actually going to be yielding us a batch, which is a bunch of samples ready to be sent to the GPU for our training step."
- 05:17.4–05:33.7 "That batch is then sent into the forward pass … compute our loss … propagated backwards. The weights are updated as part of gradient descent."
- 05:37.0–05:50.8 "in pseudocode is we're iterating through a batch in our data loader … an endless stream of batches … an epoch being when you pass through the whole data set at least once."
- 05:52.8–05:57.9 "if you just do this forward pass, you get the loss, and then you do your backward pass, and that updates the weights." (~ "this")
- 08:37.8–08:42.6 "that batch is what we feed into the forward pass for one training step." (closer)

**Ep 2, DataLoader explained** (≈ 55 s available)
- **21:04.1–21:20.1** "in PyTorch there are two big classes, the dataset and the data loader. The dataset's job is to yield one sample … The data loader's job is to take that data set, call it however many times it needs to, batch all that data, group it into a ready-made tensor, and produce a batch."
- 03:36.1–03:49.4 (alt. of the same idea) "a dataset is an object that wraps your source data living somewhere else, and its job is to produce a single sample. That's all a dataset object does."
- 07:45.4–07:54.0 "Either way, the dataset again is just showing the data loader how to go get one sample."
- 07:55.9–08:25.9 "the data loader has several pieces. It has these workers that you can span out in parallel … It'll collect some number of samples to build your batch. Then it collates them, which is basically just packing them in a nice shape … And then we output this batch." (~; the four stations in order)
- 11:56.7–12:06.9 "We have our data loader, we pass in the data set, we set the batch size, that's the batcher. This optional argument here to shuffle, that acts as our default random sampler." (~ "here"; the code beat's line)
- 12:11.2–12:15.2 "we can just keep calling next on the loader to get a batch." (closer)

**Ep 3, Dataset class** (≈ 55 s available)
- **11:07.4–11:12.0** "the only two functions you need are this length and getItem." (~ "this")
- 10:29.8–10:33.8 "we implemented both the length and the getItem dunder functions."
- 10:37.2–10:44.5 "Length just returns the length of our series. And then this get item just knows how to slice into that series."
- 06:59.6–07:20.3 "The sampler uses the length of your dataset to generate a random sequence of indices … the dataset calls getItem on that index. So the sampler creates the ordering of your data; the dataset, you have to implement this getItem function, and that's how you fetch one sample."
- 09:36.4–09:48.4 "We get a random sequence of our data. So this is kind of like a random sampler … Takes the length of our data set, gives us a random sequence. And then we iterate through one batch at a time." (the hand-rolled loop; ~ "this")
- 07:23.9–07:32.5 "if your data is small enough that doing random access, like one sample at a time, is efficient or good enough, they're fine. They're pretty simple, they're straightforward." (closer)

**Ep 4, IterableDataset** (≈ 55 s available; the cleanest reuse)
- **13:14.6–13:21.1** "if you can't use a map style dataset because it's not effective enough to look up a single sample, you will use an iterable style dataset."
- 13:24.6–13:39.2 "iterable style datasets are more commonly used, especially as you're training larger models. You do these techniques like packing shards of data that you then stream through into the model. And so here we just have to implement this iter function. There is no length, you just continually yield samples."
- 13:50.2–14:03.0 "we inherit from this iterable dataset class, and we implement this iter function … it's going to continually yield a sample."
- 14:19.2–14:26.5 "There's no sampler here. We need to do some shuffling or randomization on our own. So we handle that deterministically based on a seed and based on the worker."
- 14:29.6–14:43.9 "if you were using this on some data that's already been pre-processed on something like S3, you would pre-shuffle the data into shards. You can load the shard into memory and then yield samples from that shard."
- 14:44.7–14:56.5 "the idea is there's no more sampler telling you what index to call. It just calls this dataset object over and over again to yield the sample. So you have to handle the randomization on your own."
- 07:20.3–07:24.3 "map style datasets should be used until you can't use them anymore." (closer; the decision rule, said once in the series)

**Ep 5, num_workers** (≈ 45 s available; the demo output is on screen, not spoken)
- **15:38.7–15:48.5** "when you run an iterable dataset with multiple workers, you need to handle how you split the data among workers, because every worker is going to get that same dataset object."
- 07:58.8–08:05.4 "it has these workers that you can span out in parallel. So you'll have multiple data loaders perhaps calling this dataset object."
- 15:48.4–15:59.8 "if you're starting from the same random seed, or you're not passing the worker info along, they could be generating the same data or pulling the same exact data. So, something to be aware of, you have to handle that."
- 15:59.4–16:05.6 "Whereas when you're using the sampler, it's assigning indices and spreading that out among the different workers." (flub "sh and" at 16:03, cut it)
- 14:10.1–14:19.2 "boilerplate so that we are generating unique samples per dataloader worker, since we don't have a fixed sequence of samples anymore."
- Missing from the take: the fix in words (`get_worker_info`, worker k takes every Nth sample). It goes on the code card; or Chris records one sentence.

**Ep 6, collate**: 08:05.4–08:25.9 only. Re-record.

**Recommendation:** try the reuse first on eps 4 and 2 (the cleanest), with
the runbook's cut list and the sub-clip checks; if Chris hears the splices,
re-record the whole series in one sitting from `SCRIPTS.md` built from
these very lines (series step 2–3). Either way the scripts are his words.

## Footage (optional)

`Chris Lettieri's screen.mp4` 17:29–23:13 shows the web UI training the
model on CPU, the loss falling and the eval shapes improving epoch by
epoch. kb-graph's clock → video-time map (`prototypes/hyperframes/kb-graph/`)
can put it on top of the machine for ep 1's or ep 2's closer (the batch
arrives, the model learns). Not needed for any episode to work.

## Out of scope (written down so it isn't lost)

- **torchdata.nodes** (notebook 2, the take's 23:29–23:48, the diagram's
  state B): a second series, "the DataLoader with the lid off", one node
  per DataLoader argument, mid-epoch `state_dict()`. Its first episode's
  hook is this series' ep 5 ("the fix is: stop cloning the reader"). Plan
  it after the day-10 read of 014.
- The NanoTST architecture (17:39–18:01) belongs to the transformer series.
- A "watch a tiny transformer learn on CPU" Short from the footage alone.

## Steps (the series process, adapted)

1. Chris decides the list below. I write `SERIES.md` from this plan.
2. **Kit first:** `_kit/machine.js`, `_kit/code.js`, `00_layout/` with two
   or three takes on the machine side by side; Chris approves one frame.
3. **Mine, don't split:** for each episode, cut the candidate lines from
   the m4a in VO order into `epNN/vo_raw.m4a` (`ffmpeg -ss … -to …`,
   concat), write `epNN/script.md` with the source times, and send Chris
   the stitched audio and its transcript before any beat is built. This
   replaces series step 4's "Episode N" split. Tighten per episode as usual
   (runbook step 5).
4. `EPISODE_PROMPT.md`, one session per episode, in the order 2, 3, 5, 4,
   1 (the series image first, the on-ramp last), then the update pass.

## Decisions for Chris

1. Five episodes (1–5) with 6 optional, or four (drop ep 1 as off-topic)?
2. Ep 4: ship under a phrase nobody types, or fold it into ep 5?
3. VO: splice the take (start with eps 4 and 2), or re-record all from the
   lines above?
4. The look: the machine redrawn flat in the house style, or the isometric
   kit (`videos/_shared/web/iso/`) as in 009? The code-in-the-band angle
   from kb-code either way.
5. NanoTST / the footage: in or out of ep 1's closer?
