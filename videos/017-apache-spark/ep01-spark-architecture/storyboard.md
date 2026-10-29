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

**Sources of the VO:** `MOC - Spark` (Basics, 2024-08-01) unless marked.
Lines marked † join note fragments into a sentence; say them your way.

## VO (draft: 113 words without the if-time beat, 126 with)

| beat | VO | visual |
|---|---|---|
| 01_hook | Spark is one driver and many executors. One task per core, one task per partition. † | Frame 0 already working: the whole cluster. Driver box top, two executors middle (4 core slots each), 8 teal tiles sitting in the 8 slots, glowing. The magenta hero: one tile in executor 1, core 1. ~6 rows. |
| 02_driver | The driver is the main method of your application. It translates your code into tasks, distributes them to the executors, and collects the results. † | Executors dim; driver lights. A line of code (`df.groupBy("org_id").count()`) drops into the driver, becomes a stack of task chips; chips fly down to the slots on "distributes"; small arrows back up on "collects". |
| 03_stages | A Spark job breaks into stages, and stages break into tasks. | Inside the driver: `job` → `stage 1`, `stage 2` → 8 task chips under stage 1. Tree, top-down, one level per clause. |
| 04_partitions | Partitions are slices of a dataframe. Each task does work for a single partition of data. | `training_data` strip (16 teal tiles) below the executors; it splits into 16 slices on "slices". One slice lifts into core 1 and becomes the hero task. |
| 05_executors | Executors are the agents that execute tasks. Each one runs tasks concurrently, based on its number of cores. | Back to the cluster: 8 slices fill the 8 slots and glow together; the other 8 wait below as wave 2. Label `4 cores = 4 tasks at once` under executor 1. |
| 06_lazy *(if time)* | Spark uses lazy evaluation: no data actually moves until an action is called. (post) | Slots empty, tiles frozen; `.count()` appears, then everything runs. |
| 07_code | To force more concurrency, raise the number of partitions on your dataset. † | Code card (Dark+): `df = df.repartition(100)`. The strip re-cuts into thinner slices; more of them queue for the slots. |
| 08_close | Then open the Spark UI, go to the Stages tab, and look for tasks running in parallel. | A Stages-tab sketch: one stage row, a timeline of 8 bars overlapping (teal), label `tasks: 100`. Ends on the cluster with every slot lit. |

## Notes for Chris

- 01 joins "Driver - 1 driver / Executor - many, with cores / 1 task per
  core / 1 task operates on 1 partition". If you want the search phrase
  spoken, "Spark's architecture is one driver and many executors."
- 02 is your "main() method of your application, translates code into
  tasks, distributes tasks to workers, collects and aggregates results";
  "workers" became "executors" so the picture has one name per box.
- Cut, for the written companion: YARN / the cluster manager, the
  catalog and SparkSession, Paul's scaling advice ("vertically to ~8
  cores, then horizontally"), default parallelism = executors × cores ×
  2–8. Ep 2 owns the shuffle; ep 3 owns the slow task.
