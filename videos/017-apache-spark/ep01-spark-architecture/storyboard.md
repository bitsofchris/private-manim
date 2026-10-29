ENGINE: hyperframes

# Spark architecture explained (series ep 1 of 3): storyboard (v1, VO draft for Chris)

THE QUESTION: "What are the driver, executors, tasks and partitions in Spark, and how do they fit together?"
WHO IS ASKING: an engineer whose first PySpark job runs at work, who has
seen "executors", "stages" and "tasks" in the Spark UI with no picture of
what they are.
THE ANSWER IN ONE SENTENCE: one driver turns your code into tasks, and
many executors run them, one task per core, each task on one partition,
a slice of your dataframe.
THE SEARCH PHRASE: spark architecture explained (autocomplete, checked
10/28 via the suggest endpoint; results page not opened).

**One idea:** one task per core, one task per partition.

**Engine:** HyperFrames: boxes, slots and tiles; nothing needs Manim.
Ledger and the cluster image: `../SERIES.md`.

**Sources:** facts and the story from Chris's vault notes (`MOC - Spark`, salting, optimizing notes) and his post [Shuffling in Spark: how to balance](https://bitsofchris.com/p/shuffling-in-spark-how-to-balance). The VO is written fresh to be spoken (Chris, 10/29: no VO recorded yet, write the scripts from scratch); v1 cut the post's sentences and read like writing.

## VO (draft v2, written to be spoken: 127 words without the if-time beat, 148 with)

| beat | VO | visual |
|---|---|---|
| 01_hook | Spark's architecture is simple: one driver hands out the work, and a bunch of executors do it. | Frame 0 already working: the whole cluster. Driver box top, two executors middle (4 core slots each), 8 teal tiles sitting in the 8 slots, glowing. The magenta hero: one tile in executor 1, core 1. ~6 rows. |
| 02_driver | The driver is your program. It reads your code and turns it into a plan. | Executors dim; driver lights. A line of code (`df.groupBy("org_id").count()`) drops into the driver, becomes a stack of task chips; chips fly down to the slots on "distributes"; small arrows back up on "collects". |
| 03_stages | The plan is a job, split into stages, and each stage is split into tasks. | Inside the driver: `job` → `stage 1`, `stage 2` → 8 task chips under stage 1. Tree, top-down, one level per clause. |
| 04_partitions | Your dataframe gets cut into slices called partitions. One task works on one partition. | `training_data` strip (16 teal tiles) below the executors; it splits into 16 slices on "slices". One slice lifts into core 1 and becomes the hero task. |
| 05_executors | Executors run those tasks. Each core runs one task at a time. Two executors with four cores each? Eight tasks at once. | Back to the cluster: 8 slices fill the 8 slots and glow together; the other 8 wait below as wave 2. Label `4 cores = 4 tasks at once` under executor 1. |
| 06_lazy *(if time)* | And nothing runs until you ask for a result. Spark plans first, and only works when you call something like count. | Slots empty, tiles frozen; `.count()` appears, then everything runs. |
| 07_code | So if your job is slow and half your cores sit idle, you probably don't have enough partitions. Repartition, and every core gets work. | Code card (Dark+): `df = df.repartition(100)`. The strip re-cuts into thinner slices; more of them queue for the slots. |
| 08_close | Then open the Stages tab in the Spark UI. You want to see lots of tasks running side by side. | A Stages-tab sketch: one stage row, a timeline of 8 bars overlapping (teal), label `tasks: 100`. Ends on the cluster with every slot lit. |

## Notes for Chris

- Cut, for the written companion: YARN / the cluster manager, the
  catalog and SparkSession, Paul's scaling advice ("vertically to ~8
  cores, then horizontally"), default parallelism = executors × cores ×
  2–8. Ep 2 owns the shuffle; ep 3 owns the slow task.
