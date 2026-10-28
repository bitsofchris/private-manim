# PyTorch Data Loading and Training Essentials Series

[00:00:00] Episode one, [00:00:01] PyTorch [00:00:02] training loop [00:00:03] explained one batch [00:00:04] at a time. [00:00:05] [00:00:06] A batch is just a [00:00:07] bunch of samples [00:00:08] packed into one tensor so [00:00:09] the GPU can [00:00:10] parallelize, [00:00:11] and a PyTorch [00:00:12] training loop is what [00:00:13] happens to that one batch. [00:00:14] [00:00:15] The data loader yields [00:00:16] it, [00:00:17] the batch goes into the [00:00:18] forward pass, and the [00:00:19] model makes a prediction [00:00:20] [00:00:21] [00:00:22] We [00:00:23] compare that prediction to [00:00:24] the target, and that's the [00:00:25] loss.[00:00:26]

[00:00:26] The loss [00:00:27] is then propagated [00:00:28] backwards, and the weights [00:00:29] are updated as part of [00:00:30] gradient descent. [00:00:31] That is [00:00:32] one training step. [00:00:33] [00:00:34] Then we go back to the data [00:00:35] loader for the next batch. [00:00:36] [00:00:37] An epoch [00:00:38] is one pass through the [00:00:39] whole data set. [00:00:40] So this inner [00:00:41] loop runs once per [00:00:42] epoch, and the [00:00:43] outer loop runs [00:00:44] for as many epochs as [00:00:45] you set.[00:00:46]

[00:00:46] The model never [00:00:47] sees your data set. [00:00:48] It only ever [00:00:49] sees one batch at a time. [00:00:50] So if [00:00:51] your loss isn't moving, [00:00:52] check the batch first. [00:00:53] Everything [00:00:54] downstream of it is the [00:00:55] same four lines every [00:00:56] time[00:00:57] [00:00:58] [00:00:59]

[00:00:59] [00:01:00] Episode two, [00:01:01] PyTorch Data Loader [00:01:02] explained. [00:01:03] [00:01:04] In PyTorch, the [00:01:05] dataset's job is to [00:01:06] hand back one [00:01:07] sample, and the data [00:01:08] loader's job is to [00:01:09] call it [00:01:10] N number of times and [00:01:11] hand back a batch. [00:01:12] The [00:01:13] data loader is a [00:01:14] machine with four different [00:01:15] stations, and every argument you [00:01:16] pass is one of those [00:01:17] stations. [00:01:18] [00:01:19] Your dataset sits at the [00:01:20] front.

[00:01:20] All it [00:01:21] knows is how to go get [00:01:22] one sample, [00:01:23] wherever that data lives [00:01:24] [00:01:25] [00:01:26] The [00:01:27] first station is the [00:01:28] sampler. It decides [00:01:29] the order. [00:01:30] Shuffle equals true [00:01:31] is a random [00:01:32] sampler, a random [00:01:33] sequences of indies. [00:01:34] A [00:01:35] random sequence of [00:01:36] [00:01:37] indices. Second up is [00:01:38] fetch. Workers [00:01:39] will call your dataset with [00:01:40] those indices [00:01:41] in parallel if you ask [00:01:42] for them.[00:01:43]

[00:01:43] Third is [00:01:44] batching. It [00:01:45] collects [00:01:46] batch-sized samples. [00:01:47] [00:01:48] And fourth is collate. This is [00:01:49] what packs them [00:01:50] into one tensor [00:01:51] shaped for the GPU. [00:01:52] [00:01:53] Out comes the batch [00:01:54] and what goes into the forward [00:01:55] [00:01:56] pass.

[00:01:56] so [00:01:57] episode three, [00:01:58] [00:01:59] PyTorch Dataset [00:02:00] Class: Two Functions and [00:02:01] You're Done. [00:02:02] [00:02:03] A PyTorch [00:02:04] dataset class is two [00:02:05] functions. How [00:02:06] many samples [00:02:07] and how do I get [00:02:08] sample i? [00:02:09] Everything else is the [00:02:10] data loader's job. [00:02:11] [00:02:12] Len [00:02:13] returns the number of [00:02:14] samples.

[00:02:14] [00:02:15] Getitem returns [00:02:16] sample at [00:02:17] index i. [00:02:18] [00:02:19] In this[00:02:20] [00:02:21] [00:02:22] [00:02:23] [00:02:24]

[00:02:24] Here, the [00:02:25] series are precomputed [00:02:26] into one tensor, [00:02:27] so get item [00:02:28] is just a [00:02:29] slice. Because you [00:02:30] can index into the [00:02:31] dataset, the sampler [00:02:32] owns the order. [00:02:33] It uses the [00:02:34] length to make a random [00:02:35] sequence of indices [00:02:36] and calls get [00:02:37] item on each one. [00:02:38] So shuffling is [00:02:39] free, and a [00:02:40] validation split is just a [00:02:41] list of indices.[00:02:42]

[00:02:42] If you've [00:02:43] ever shuffled with [00:02:44] torch.randperm [00:02:45] and sliced batches [00:02:46] by hand, you already wrote [00:02:47] this. [00:02:48] Randperm is the sampler. [00:02:49] The range step [00:02:50] is the batcher, and the [00:02:51] slice is get [00:02:52] item plus [00:02:53] collate.

[00:02:53] This is [00:02:54] called a map style [00:02:55] dataset. You use it [00:02:56] when random access is [00:02:57] cheap[00:02:58] [00:02:59] [00:03:00] [00:03:01] [00:03:02]

[00:03:02] If you write these two [00:03:03] functions first, the [00:03:04] loader, the shuffle, and the split will [00:03:05] come for free

[00:03:08] [00:03:09] Episode four, [00:03:10] PyTorch iterable [00:03:11] dataset [00:03:12] [00:03:13] explained. If [00:03:14] looking up one sample isn't [00:03:15] cheap, you use an [00:03:16] iterable dataset.[00:03:17]

[00:03:17] Here we use [00:03:18] one function iter [00:03:19] that just yields [00:03:20] samples [00:03:21] [00:03:22] I [00:03:23] most frequently use this when [00:03:24] training bigger models. [00:03:25] You pack the data into [00:03:26] shards and just [00:03:27] stream them through. [00:03:28] There's no length, no [00:03:29] get item. Sample [00:03:30] i doesn't exist [00:03:31] until the iterator [00:03:32] produces it. [00:03:33] [00:03:34] This means there's no [00:03:35] sampler. The loader just [00:03:36] calls your dataset over and [00:03:37] over, and it yields the next [00:03:38] sample.

[00:03:38] So [00:03:39] shuffling is now your [00:03:40] problem. You [00:03:41] pre-shuffle the data into [00:03:42] shards, load one shard [00:03:43] into memory, and yield from [00:03:44] it. [00:03:45] Splits are also your problem [00:03:46] too. If you run multiple [00:03:47] workers, splitting the stream [00:03:48] between them is up to you [00:03:49] to determine. [00:03:50] The [00:03:51] data loader on top is [00:03:52] the same though.

[00:03:52] [00:03:53] Same batch size, same [00:03:54] collate, same batch [00:03:55] out. The only thing that [00:03:56] changes the data loader is [00:03:57] asking for the next [00:03:58] sample, not for the [00:03:59] sample at index [00:04:00] i.

[00:04:00] So use [00:04:01] map until you can't, and [00:04:02] the day sample i stops [00:04:03] being cheap, swap [00:04:04] to an interval dataset[00:04:05] [00:04:06] [00:04:07] [00:04:08]

[00:04:08] Episode five: [00:04:09] PyTorch [00:04:10] [00:04:11] NumWorkers, [00:04:12] why you get duplicate [00:04:13] batches. [00:04:14] [00:04:15] In [00:04:16] PyTorch, NumWorkers [00:04:17] doesn't split your data [00:04:18] across the workers. [00:04:19] [00:04:20] Each worker is a full [00:04:21] copy of your dataset [00:04:22] fetching and collating on [00:04:23] its own. [00:04:24] So when you run an [00:04:25] iterable dataset with multiple [00:04:26] workers, [00:04:27] every worker gets [00:04:28] the same dataset [00:04:29] object, and unless you [00:04:30] split the stream yourself, they [00:04:31] all deliver the same [00:04:32] data.

[00:04:32] [00:04:33] With a map-style [00:04:34] dataset, you're fine. [00:04:35] The sampler stays [00:04:36] in the main [00:04:37] process and hands [00:04:38] each worker a different set [00:04:39] of indices. [00:04:40] Every sample here [00:04:41] gets fetched once. [00:04:42] But with an [00:04:43] iterable dataset, there [00:04:44] are no indices. [00:04:45] Each worker [00:04:46] starts the stream from the [00:04:47] beginning. So if [00:04:48] you have the same seed, you're [00:04:49] getting the same data.[00:04:50]

[00:04:50] [00:04:51] Two workers, batch [00:04:52] size four, the first [00:04:53] two batches will be [00:04:54] identical. [00:04:55] The fix lives [00:04:56] inside your iter [00:04:57] function. Ask [00:04:58] for the worker [00:04:59] info and have [00:05:00] worker K take [00:05:01] every Nth [00:05:02] sample starting at [00:05:03] K, [00:05:04] or [00:05:05] spread the shards out among [00:05:06] workers based on the [00:05:07] worker's identity. [00:05:08] [00:05:09] Now the two [00:05:10] copies can walk the stream [00:05:11] in step and nothing is [00:05:12] delivered [00:05:13] twice.

[00:05:13] So before [00:05:14] you increase num [00:05:15] workers on an iterable [00:05:16] dataset, be sure you're [00:05:17] passing that worker [00:05:18] info to each iter [00:05:19] function so you can [00:05:20] split the stream [00:05:21] [00:05:22] [00:05:23] accordingly

