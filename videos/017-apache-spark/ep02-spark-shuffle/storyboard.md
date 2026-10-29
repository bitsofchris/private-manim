ENGINE: hyperframes

# Spark shuffle explained (series ep 2 of 3): storyboard (v1, VO draft for Chris)

THE QUESTION: "What is a shuffle in Spark, and why does it make my job so slow?"
WHO IS ASKING: the same engineer, now with a working job that crawls; the
Spark UI shows huge "shuffle read / write" numbers and spill.
THE ANSWER IN ONE SENTENCE: a shuffle is data moving between executors,
caused by wide transformations like join, groupBy and distinct; it is
slow because network I/O is slow, it needs more memory, and it spills to
disk, and `df.explain()` shows it as `Exchange` before you run.
THE SEARCH PHRASE: spark shuffle explained (autocomplete, checked 10/28
via the suggest endpoint; results page not opened).

**One idea:** a shuffle is data crossing the network between executors.

**Engine:** HyperFrames. Ledger and the cluster image: `../SERIES.md`.

**Sources of the VO:** Chris's post
[Shuffling in Spark: how to balance](https://bitsofchris.com/p/shuffling-in-spark-how-to-balance),
sentences cut and reordered. Lines marked † are trimmed mid-sentence.

## VO (draft: 137 words without the if-time beat, 161 with)

| beat | VO | visual |
|---|---|---|
| 01_hook | To improve Spark performance, do your best to avoid shuffling. A shuffle is when data needs to move between executors. | Frame 0 already working: the cluster, tiles in executor 1 sliding across the gap into executor 2 along arrows (magenta hero: the crossing). Gap label `network`. |
| 02_narrow | Narrow transformations, like map and filter: each partition can be completed independently. This is Spark at its best. † | Every tile stays in its own slot and changes colour in place (`filter` drops rows: tiles shrink). No arrows. Label `narrow`. |
| 03_wide | Wide transformations, like join, groupBy and distinct, need data from different partitions co-located. That triggers a shuffle. † | `groupBy("org_id")`: tiles split by key colour stripe; every same-stripe piece crosses to one slot. Arrows criss-cross the gap. Label `wide`. |
| 04_cost | Shuffles are bad for performance: network I/O is slow, executors need more memory to hold the intermediate data, and data can spill to disk. † | Three items land one per clause: the arrows slow and queue at the gap (`network`); an executor's memory bar fills; overflow tiles drop into a disk glyph (`spill`). |
| 05_story | I was preparing a large dataset for deep learning. The job was painfully inefficient because of a global sort. This was causing a massive data shuffle. † | `training_data` strip; `orderBy(...)` on screen; every tile crosses the gap at once, the arrows become a jam. |
| 06_fix | I hashed the composite key, assigned a partition number to each row, and randomized with sortWithinPartitions. † | Code card: `.repartition("partition_id")` / `.sortWithinPartitions(...)`. One crossing, then tiles sort inside their own slots; no more arrows. |
| 07_broadcast *(if time)* | When one side of a join is small, broadcast it: a copy of the smaller dataset goes to each executor, to avoid a shuffle. † | A small table copied into both executors; the big tiles never move. `broadcast(df_small)`. |
| 08_close | Before you run a job, use df.explain(). Read the plan bottom-up. The Exchange is the shuffle. | Code card: `df.join(df_other, "key").groupBy("column").count().explain()` then the plan: `HashAggregate` / `+- Exchange hashpartitioning(column, 200)`; the Exchange line goes magenta. |

## Notes for Chris

- 05–06 is the proof from your post; the hash formula from `Spark
  Optimizing Writing` is too long for the card, so the card shows the
  two calls only.
- Cut, for the written companion: Spark UI shuffle read/write and spill
  checks, coalesce vs repartition, caching and storage levels, executor
  memory, `spark.sql.shuffle.partitions`, AQE. Ep 3 owns AQE and
  shuffle partitions only if it needs them.
- 08 is the closer and the code beat: the viewer's next move.
