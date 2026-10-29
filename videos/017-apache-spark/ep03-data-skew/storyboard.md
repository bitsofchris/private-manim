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

**Sources of the VO:** `Spark - salting guide how to fix slow task`
(2025-03-05), `Spark Optimizing Writing` (window functions), `Spark -
random tips` (2025-10-25), and the shuffle post (AQE) where marked. Most
of these notes are fragments, so most lines are † (fragments joined):
this script needs your words more than the other two.

## VO (draft: 114 words without the if-time beat, 128 with)

| beat | VO | visual |
|---|---|---|
| 01_hook | Spark runs one task per partition. So when one partition is huge, one task does all the work, and the cluster waits. † | Frame 0 already working: the cluster, seven cores dim and done (check marks), one core running a 10×-wide tile (magenta hero). Counter `199/200`. |
| 02_skew | That's data skew. In the Spark UI it's one lagging task while the rest are done. † | Stages-tab sketch: 199 short teal bars, one bar running off the right edge. On-screen fact (research, not VO): `stage time = slowest task`. |
| 03_window | I hit it with a global window: all the data was forced into one partition, so only one executor was doing work. † | Code card: `Window.orderBy("partition_id", "temp_idx")`; all 16 tiles slide into one slot of executor 1; executor 2 goes dark. |
| 04_sort | Same with a global sort: one task to sequence everything. † | `orderBy(...)` on the card; the same single-slot pile. |
| 05_salt | The fix is salting. Add a salt to the key, and the partitions get more uniform, so the cluster is more utilized. † | The fat tile cuts into 8 slices (salt 0–7), magenta passes to the slices; they spread across all 8 cores; every slot lights. |
| 06_code | Group by the key and the salt, then group again by the key. | Code card (Dark+): `salted = df.withColumn("salt", (F.rand() * 8).cast("int"))` / `.groupBy("org_id", "salt").count()` / `.groupBy("org_id").sum("count")`. Two short stages; bars in the Stages sketch now even. |
| 07_aqe *(if time)* | Adaptive query execution adjusts shuffle partitions at runtime, which helps especially with data skew. (post) † | `spark.conf.set("spark.sql.adaptive.enabled", "true")`; a fat shuffle partition splits by itself. |
| 08_close | Break the problem down yourself to keep things parallelized. | The cluster, 8 slots lit, `200/200`. |

## Notes for Chris

- Your salting note says "My advanced one two time frames with severe
  sore" (skew, I think) and "screen shots of lagging task vs more uniform". If you have
  the work screenshots (redacted), 02 and 06 could use them instead of
  the sketch.
- 04 may be one line too many after 03: cut it first if the take runs
  long.
- Research says try AQE and the partition count before salting, since
  salting multiplies shuffle bytes and needs the second groupBy. 07 is
  the if-time beat; if you want that order in the VO, swap 07 above 05.
- Cut, for the written companion: bucketing (in your 2025-03 content
  list), speculation, the max/median task-duration ratio.
