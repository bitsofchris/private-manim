ENGINE: hyperframes

# Data skew in Spark (series ep 3 of 3): storyboard (v1, VO draft for Chris)

THE QUESTION: "Why is my Spark job stuck at 199 of 200 tasks?"
WHO IS ASKING: the same engineer; the stage shows 199 tasks done in
seconds and one still running, and adding executors didn't help.
THE ANSWER IN ONE SENTENCE: Spark runs one task per partition, so when
one partition holds most of the data, one task does most of the work
while the rest of the cluster waits; salt the key to make partitions
uniform.
THE SEARCH PHRASE: data skewness in spark (autocomplete, checked 10/28
via the suggest endpoint; "data skew salting" also offered; results page
not opened).

**One idea:** a stage is as slow as its biggest partition.

**Engine:** HyperFrames. Ledger and the cluster image: `../SERIES.md`.

**Sources:** facts and the story from Chris's vault notes (`MOC - Spark`, salting, optimizing notes) and his post [Shuffling in Spark: how to balance](https://bitsofchris.com/p/shuffling-in-spark-how-to-balance). The VO is written fresh to be spoken (Chris, 10/29: no VO recorded yet, write the scripts from scratch); v1 cut the post's sentences and read like writing.

## VO (draft v2, written to be spoken: 140 words without the if-time beat, 161 with)

| beat | VO | visual |
|---|---|---|
| 01_hook | Data skew is why your Spark job sits at 199 of 200 tasks. One partition got most of the data, so one task is doing most of the work. | Frame 0 already working: the cluster, seven cores dim and done (check marks), one core running a 10×-wide tile (magenta hero). Counter `199/200`. |
| 02_skew | Spark runs one task per partition, and a stage isn't done until its slowest task is. The rest of your cluster just waits. | Stages-tab sketch: 199 short teal bars, one bar running off the right edge. On-screen fact (research, not VO): `stage time = slowest task`. |
| 03_window | I've done this myself. A window over the whole dataset forced everything into one partition. One executor working, the rest idle. | Code card: `Window.orderBy("partition_id", "temp_idx")`; all 16 tiles slide into one slot of executor 1; executor 2 goes dark. |
| 04_more | Adding executors won't help. Only one of them has the work. | Two more executor boxes slide in, empty and dim; the one fat tile keeps running in its single slot. |
| 05_salt | The fix is salting. Add a random number to the hot key, and its rows spread across many partitions. Now every core has work. | The fat tile cuts into 8 slices (salt 0–7), magenta passes to the slices; they spread across all 8 cores; every slot lights. |
| 06_code | Group by the key and the salt, then group again by the key to combine the pieces. | Code card (Dark+): `salted = df.withColumn("salt", (F.rand() * 8).cast("int"))` / `.groupBy("org_id", "salt").count()` / `.groupBy("org_id").sum("count")`. Two short stages; bars in the Stages sketch now even. |
| 07_aqe *(if time)* | On Spark 3 and up, turn on adaptive query execution first. In joins, it can split a skewed partition for you. | `spark.conf.set("spark.sql.adaptive.enabled", "true")`; a fat shuffle partition splits by itself. |
| 08_close | Find the task that won't finish, find the key behind it, and spread it out. | The cluster, 8 slots lit, `200/200`. |

## Notes for Chris

- Your salting note says "My advanced one two time frames with severe
  sore" (skew, I think) and "screen shots of lagging task vs more uniform". If you have
  the work screenshots (redacted), 02 and 06 could use them instead of
  the sketch.
- The global-sort line is gone: a global sort range-partitions, it does
  not pile everything into one partition, so the global window is the
  only one-partition example (your note had it with a "?").
- Research says try AQE and the partition count before salting, since
  salting multiplies shuffle bytes and needs the second groupBy. 07 is
  the if-time beat; if you want that order in the VO, swap 07 above 05.
- Cut, for the written companion: bucketing (in your 2025-03 content
  list), speculation, the max/median task-duration ratio.
