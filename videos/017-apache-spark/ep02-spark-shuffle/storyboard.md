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

**Sources:** facts and the story from Chris's vault notes (`MOC - Spark`, salting, optimizing notes) and his post [Shuffling in Spark: how to balance](https://bitsofchris.com/p/shuffling-in-spark-how-to-balance). The VO is written fresh to be spoken (Chris, 10/29: no VO recorded yet, write the scripts from scratch); v1 cut the post's sentences and read like writing.

## VO (draft v2, written to be spoken: 146 words without the if-time beat, 168 with)

| beat | VO | visual |
|---|---|---|
| 01_hook | A Spark shuffle is your data moving across the network, between executors. It's usually the slowest part of your job. | Frame 0 already working: the cluster, tiles in executor 1 sliding across the gap into executor 2 along arrows (magenta hero: the crossing). Gap label `network`. |
| 02_narrow | Some steps never move data. A filter or a map works on each partition right where it sits. | Every tile stays in its own slot and changes colour in place (`filter` drops rows: tiles shrink). No arrows. Label `narrow`. |
| 03_wide | Others need every row with the same key in one place: a join, a groupBy, a distinct. To get there, Spark has to shuffle. | `groupBy("org_id")`: tiles split by key colour stripe; every same-stripe piece crosses to one slot. Arrows criss-cross the gap. Label `wide`. |
| 04_cost | Shuffles cost you: the network is slow, they eat executor memory, and when memory runs out, data spills to disk. | Three items land one per clause: the arrows slow and queue at the gap (`network`); an executor's memory bar fills; overflow tiles drop into a disk glyph (`spill`). |
| 05_story | I hit this prepping a big time-series dataset for model training. A global sort shuffled everything, and the job crawled. | `training_data` strip; `orderBy(...)` on screen; every tile crosses the gap at once, the arrows become a jam. |
| 06_fix | The fix: hash the key into a partition number, repartition once, then sort inside each partition. One small shuffle instead of a giant one. | Code card: `.repartition("partition_id")` / `.sortWithinPartitions(...)`. One crossing, then tiles sort inside their own slots; no more arrows. |
| 07_broadcast *(if time)* | If one side of a join is small, broadcast it. Every executor gets its own copy, and the big table never moves. | A small table copied into both executors; the big tiles never move. `broadcast(df_small)`. |
| 08_close | Before you run anything, call explain. Read the plan from the bottom up. Every Exchange you see is a shuffle. | Code card: `df.join(df_other, "key").groupBy("column").count().explain()` then the plan: `HashAggregate` / `+- Exchange hashpartitioning(column, 200)`; the Exchange line goes magenta. |

## Notes for Chris

- 05–06 is the proof from your post; the hash formula from `Spark
  Optimizing Writing` is too long for the card, so the card shows the
  two calls only.
- Cut, for the written companion: Spark UI shuffle read/write and spill
  checks, coalesce vs repartition, caching and storage levels, executor
  memory, `spark.sql.shuffle.partitions`, AQE. Ep 3 owns AQE and
  shuffle partitions only if it needs them.
- 08 is the closer and the code beat: the viewer's next move.
