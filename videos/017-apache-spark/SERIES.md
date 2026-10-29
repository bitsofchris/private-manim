# Apache Spark: the series (three Shorts)

**Name:** apache-spark-series
**Description:** Three Shorts for an engineer who just started writing
Spark jobs: what the driver, executors, tasks and partitions are (one
picture of the cluster), then the two things that make a job slow, the
shuffle and the one task that holds everyone up. Dispatched from Chris's
2026-10-28 task (`short: makes this spark series`), storyboarded
2026-10-28. **Status: VO is a draft cut from Chris's Spark notes and his
shuffle post, for him to edit before recording.** The notes are mostly
fragments ("Driver - 1 driver"), so some lines join fragments into
sentences; each storyboard marks which.
**When to use:** record the three in one take (`agents/series.md` step 3),
then one session per episode, `agents/runbook.md` from step 2. Steps 0–1
are done here.
**How it works:** one recurring image, the cluster (one driver, two
executors with four cores each, a dataframe cut into partition tiles),
carries all three. Ep 1 builds it; ep 2 moves tiles between executors
(the shuffle); ep 3 makes one tile fat and the other cores go idle
(skew). One engine, HyperFrames, every beat.

## Who it is for, the promise

A data or ML engineer whose first PySpark job is running at work and is
slow. Has opened the Spark UI and seen "executors", "stages" and "200
tasks" without a model of what they are. **Promise:** one picture of the
cluster, then the two places time goes: data moving between executors,
and one task doing everyone's work.

## The episodes

| # | Working name | Their question | The answer | What they do after |
|---|---|---|---|---|
| 1 | spark architecture | What are the driver, executors, tasks and partitions? | One driver turns your code into tasks; many executors run them, one task per core, each task on one partition (a slice of your dataframe). | Raise the partitions; check the Stages tab for tasks running in parallel. |
| 2 | spark shuffle | What is a shuffle, and why is my job slow? | A shuffle is data moving between executors: network I/O, more memory, spills to disk. Joins, groupBy and distinct cause it; `explain()` shows it as `Exchange`. | Run `df.explain()` and look for Exchange before you run the job. |
| 3 | data skew | Why is my job stuck on the last task? | One task per partition, so one big partition means one task does the work while the cluster waits. Salt the key to even the partitions out. | Salt the hot key; avoid global windows and sorts. |

## Search phrases (checked 2026-10-28, YouTube autocomplete via the suggest endpoint, not the browser box)

- ep 1: **spark architecture explained** (offered; also "apache spark
  architecture explained", "spark architecture interview questions").
  Never title it "spark driver": autocomplete is all Walmart delivery
  drivers.
- ep 2: **spark shuffle explained** (offered; "spark shuffle join" and
  "spark shuffle partitions" too).
- ep 3: **data skewness in spark** (offered; also "data skew salting",
  "data skewness in pyspark").
- The results pages were not opened: a person should glance at them
  before the titles are set (runbook step 0, second check).

## Ledger (identical in every episode)

- **The cluster:** 1 driver (top), 2 executors (`executor 1`,
  `executor 2`), 4 cores each = 8 task slots.
- **The dataframe:** `training_data`, Chris's real job: a time-series
  dataset being prepared for deep learning, keyed by `org_id`. 16
  partitions in ep 1 (two waves of 8 tasks).
- **Shuffle partitions:** 200 (`spark.sql.shuffle.partitions`' default).
  Ep 3's stuck stage reads `199/200`.
- **Code:** PySpark, VS Code Dark+ code card (`agents/style.md`).
  ep 1 `df = df.repartition(100)` (Chris's note); ep 2 his `explain()`
  plan from the post; ep 3 a two-step salted `groupBy`.

## The image (`_kit/cluster.js`, to build before the episode sessions: `agents/series.md` step 5)

- **Driver:** one rounded box, top of the stage, label `driver`. Holds the
  plan (job → stages → tasks) as a short stack.
- **Executors:** two boxes side by side, middle of the stage, each with
  four core slots in a row. Label `executor` and `core` once.
- **Partitions:** teal tiles (data, `S.DATA`), a dataframe drawn as a strip
  of 16 tiles that splits into slices. A task = a tile sitting in a core
  slot, glowing while it runs.
- **Shuffle (ep 2):** tiles leave one executor and cross the gap to the
  other along arrows; the gap is labelled `network`.
- **Skew (ep 3):** one tile is 10× wide; its core runs, seven cores sit
  dim.
- **Magenta hero:** ep 1 the task (one tile in one core); ep 2 the
  `Exchange` (the crossing, then the plan line); ep 3 the fat partition,
  then the salted slices.

## Research (evidence, one beat at most; the spine is Chris's notes)

- Vault: `MOC - Spark` (basics, 2024-08-01, the driver/executor/partition
  lines), `Spark Driver - StackOverflow`, `Monitoring Spark`, `Spark
  Optimizing Writing` (the global window line), `Spark - salting guide
  how to fix slow task`, `Spark - random tips` (2025-10-25), `2025-03-21 -
  spark content before Toto open publish` (Chris wanted "a quick spark
  YouTube series": memory, salting, avoiding global sorts, bucketing).
- Chris's post: [Shuffling in Spark: how to balance](https://bitsofchris.com/p/shuffling-in-spark-how-to-balance),
  the source of ep 2.
- 101: Apache Spark, [Cluster Mode Overview](https://spark.apache.org/docs/latest/cluster-overview)
  (driver runs main and creates the SparkContext; executors run tasks and
  keep data in memory or disk; a job is a parallel computation of many
  tasks spawned by an action). Matches Chris's notes; nothing to correct.
- Optimisation, current practice: the "5 S" framing of slow jobs (spill,
  skew, shuffle, storage, serialization;
  [dev.to](https://dev.to/anhcodes/debug-long-running-spark-job-5go4)),
  "stage time = slowest task time" and the max/median task-duration ratio
  as the skew tell
  ([Databricks community, reading the Spark UI](https://community.databricks.com/t5/community-articles/reading-spark-ui-a-repeatable-guide-to-finding-performance/td-p/160574),
  [Towards AI on skew](https://pub.towardsai.net/part-vii-data-skew-in-spark-why-199-tasks-finish-in-40-seconds-and-one-runs-for-3-hours-7daef3b1de44)),
  and "try AQE and partition counts before salting, which multiplies
  shuffle bytes" ([OneUptime on AQE and skewed joins](https://oneuptime.com/blog/post/2026-08-13-spark-aqe-not-fixing-skewed-join/view)).
  Used: "stage time = slowest task" as ep 3's on-screen fact. The 5 S list
  is the spine of a possible ep 4+ (spill, storage, serialization are not
  covered here).

## Checklist

| ep | working name | folder | Script | VO | Storyboard | Beats | Assembled | Shipped |
|---|---|---|---|---|---|---|---|---|
| 1 | spark architecture | `ep01-spark-architecture/` | [x] draft | [ ] | [x] | [ ] | [ ] | [ ] |
| 2 | spark shuffle | `ep02-spark-shuffle/` | [x] draft | [ ] | [x] | [ ] | [ ] | [ ] |
| 3 | data skew | `ep03-data-skew/` | [x] draft | [ ] | [x] | [ ] | [ ] | [ ] |
