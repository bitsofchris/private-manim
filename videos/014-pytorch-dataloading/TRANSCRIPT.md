# The series take, transcribed

Source: `~/Creating/014-pytorch-dataloading.m4a` (323.5 s, recorded
2026-10-28, five episodes in script order with "Episode N: title" before
each). Parakeet v3 (runbook step 4), 2026-10-28. Chris's own 1-second
transcript is `recorded-transcript.md`; the two disagree on "batch size"
(ep 4, Parakeet "batch I") and agree on "interval dataset" (ep 4's last
words, ear check pending).

Episode cuts (seconds into the file, announcement removed):

| Ep | Folder | Cut | Raw |
|---|---|---|---|
| 1 | `ep01-training-loop` | 5.70–57.00 | 51.3 s |
| 2 | `ep02-dataloader-explained` | 63.90–116.00 | 52.1 s |
| 3 | `ep03-dataset-class` | 122.80–186.40 | 63.6 s |
| 4 | `ep04-iterable-dataset` | 193.30–246.00 | 52.7 s |
| 5 | `ep05-num-workers` | 255.00–322.50 | 67.5 s |

The earlier lecture take (2026-07-24, the long video) is
`TRANSCRIPT-lecture-2026-07-24.md`.

00:00.001-00:05.760
Episode one PyTorch Training Loop Explained One Batch at a time.

00:05.760-00:10.720
A batch is just a bunch of samples packed into one tensor so the GPU can parallelize.

00:10.880-00:14.560
And a PyTorch training loop is what happens to that one batch.

00:14.519-00:20.200
The data loader yields it, the batch goes into the forward pass, and the model makes a prediction.

00:22.599-00:25.960
We compare that prediction to the target and that's the loss.

00:26.119-00:31.240
The loss is then propagated backwards and the weights are updated as part of gradient descent.

00:31.240-00:33.480
That is one training step.

00:33.480-00:36.440
Then we go back to the data loader for the next batch.

00:36.960-00:40.240
An epoch is one pass through the whole dataset.

00:40.240-00:45.920
So this inner loop runs once per epoch and the outer loop runs for as many epochs as you set.

00:45.920-00:51.280
The model never sees your dataset, it only ever sees one batch at a time.

00:50.460-00:53.100
So if your loss isn't moving, check the batch first.

00:53.100-00:56.700
Everything downstream of it is the same four lines every time.

00:59.520-01:12.560
Episode 2, PyTorch Data Loader Explained In PyTorch, the dataset's job is to hand back one sample, and the data loader's job is to call it n number of times and hand back a batch.

01:12.439-01:17.719
The data loader is a machine with four different stations, and every argument you pass is one of those stations.

01:18.600-01:20.360
Your dataset sits at the front.

01:20.360-01:24.280
All it knows is how to go get one sample, wherever that data lives.

01:26.560-01:28.399
The first station is the sampler.

01:28.399-01:29.759
It decides the order.

01:29.759-01:36.799
Shuffle equals true is a random sampler, a random sequence of indices, a random sequence of indices.

01:37.080-01:38.520
Second up is fetch.

01:38.520-01:43.080
Workers will call your dataset with those indices in parallel if you ask for them.

01:43.080-01:44.360
Third is batching.

01:44.360-01:47.320
It collects batch-sized samples.

01:47.420-01:48.860
And fourth is collate.

01:48.860-01:52.780
This is what packs them into one tensor shaped for the GPU.

01:52.780-01:55.900
Out comes the batch and what goes into the forward pass.

01:56.259-02:01.860
So episode three, PyTorch dataset class, two functions, and you're done.

02:02.899-02:05.939
A PyTorch dataset class is two functions.

02:05.640-02:06.840
How many samples?

02:06.840-02:08.840
And how do I get sample i?

02:08.840-02:11.320
Everything else is the data loader's job.

02:12.280-02:14.600
Len returns the number of samples.

02:14.600-02:18.040
Get item returns sample at index i.

02:18.660-02:29.620
In this here the series are pre-computed into one tensor, so get item is just a slice.

02:29.340-02:33.100
Because you can index into the dataset, the sampler owns the order.

02:33.100-02:37.900
It uses the length to make a random sequence of indices and calls getItem on each one.

02:37.900-02:42.060
So shuffling is free, and a validation split is just a list of indices

02:42.240-02:44.000
If you've ever shuffled with torch.

02:44.080-02:47.280
randperm and sliced batches by hand, you already wrote this.

02:47.280-02:49.040
Randperm is the sampler.

02:49.040-02:53.520
The range step is the batcher, and the slice is get item plus collate.

02:53.340-02:55.420
This is called a map style dataset.

02:55.420-02:57.740
You use it when random access is cheap.

03:01.820-03:06.140
If you write these two functions first, the loader, the shuffle, and the split will come for free.

03:08.400-03:13.360
Episode 4, PyTorch Iterable Dataset Explained.

03:13.360-03:17.040
If looking up one sample isn't cheap, you use an iterable dataset.

03:17.040-03:21.680
Here we use one function iter that just yields samples.

03:22.500-03:24.980
I most frequently use this when training bigger models.

03:24.980-03:27.860
You pack the data into shards and just stream them through.

03:27.860-03:29.620
There's no length no get item.

03:29.620-03:33.060
Sample i doesn't exist until the iterator produces it.

03:33.740-03:35.260
This means there's no sampler.

03:35.260-03:38.620
The loader just calls your dataset over and over and it yields the next sample.

03:38.620-03:40.300
So shuffling is now your problem.

03:40.300-03:44.540
You pre-shuffle the data into shards, load one shard into memory and yields from it.

03:44.460-03:46.140
Splits are also your problem too.

03:46.140-03:50.380
If you run multiple workers, splitting the stream between them is up to you to determine.

03:50.380-03:52.940
The data loader on top is the same though.

03:52.600-03:55.080
Same batch I, same collate, same batch out.

03:55.080-04:00.200
The only thing that changes the data loader is asking for the next sample, not for the sample at index i.

04:00.200-04:05.800
So use map until you can't, and the day sample i stops being cheap, swap to an interval dataset.

04:07.800-04:11.959
Episode five PyTorch Numb Workers.

04:11.959-04:13.720
Why you get duplicate batches

04:15.060-04:19.459
In PyTorch, numorkers doesn't split your data across the workers.

04:19.459-04:23.860
Each worker is a full copy of your dataset, fetching and collating on its own.

04:23.500-04:29.340
So when you run an iterable data set with multiple workers, every worker gets the same dataset object.

04:29.340-04:32.700
And unless you split the stream yourself, they all deliver the same data.

04:32.660-04:34.900
With a map style dataset, you're fine.

04:34.900-04:39.940
The sampler stays in the main process and hands each worker a different set of indices.

04:39.940-04:42.340
Every sample here gets fetched once.

04:42.240-04:45.120
But with an iterable dataset, there are no indices.

04:45.120-04:47.520
Each worker starts the stream from the beginning.

04:47.520-04:50.400
So if you have the same seed, you're getting the same data.

04:50.620-04:55.020
Two workers, batch size four, the first two batches will be identical.

04:55.020-04:57.500
The fix lives inside your iter function.

04:57.500-05:03.020
Ask for the worker info and have worker k take every nth sample starting at k

05:03.780-05:08.900
or spread the shards out among workers based on the worker's identity.

05:08.900-05:13.139
Now the two copies can walk the stream in step and nothing is delivered twice.

05:13.039-05:21.840
So before you increase num workers on an iterable dataset, be sure you're passing that worker info to each iter function so you can split the stream accordingly.


