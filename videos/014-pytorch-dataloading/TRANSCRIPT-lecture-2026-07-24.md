# The 2026-07-24 lecture take (the long video), transcribed

Source: `~/Creating/pytorch dataloading/edit/studio-sound-Chris Lettieri.m4a`
(Descript Studio Sound, 1430.6 s). Parakeet v3, 2026-10-25. The published
8.7-minute video (youtube.com/watch?v=Jo8lCFLMpCQ) is Descript's cut of
298–1424 s. Reference only: the series was re-recorded on 2026-10-28
(`TRANSCRIPT.md`).

00:58.260-00:59.220
Okay.

01:03.540-01:09.380
Today we're going to implement the data loading for a small time series transformer model in PyTorch.

01:12.840-01:17.160
Today we're building the data loading for a small time series transformer model in PyTort.

01:22.159-01:28.320
By the end of this video, by the end of this video, you'll understand how we do

01:37.640-01:42.680
Today we're going to implement the data loading for a small time series transformer model in PyTorch.

01:42.640-01:48.880
By the end of this video, you'll understand the map where data loading fits.

01:48.880-01:51.920
By the end of this video, you'll understand the overview of where

01:54.920-01:59.960
By the end of this video, you understand the big picture where data loading fits into the training step.

01:59.960-02:05.320
We'll talk about the two different types of data sets that you can have and how that impacts your data loading decisions.

02:10.160-02:14.720
And then we'll actually see this train a tiny time series transformer model on your CPU.

02:19.040-02:29.760
The key idea I want you to remember is that a dataset, the dataset object, its job is to produce one sample from your dataset that lives somewhere else in a source system.

02:29.540-02:34.180
The data loader is what takes that data set to produce your batches.

02:34.180-02:37.460
Those batches are what are fed to the training loop.

02:38.260-02:40.900
And those batches are what are fed to the training loop.

03:00.060-03:02.700
Today we're talking about data loading in PyTorch.

03:04.160-03:08.400
By the end of this video, you'll understand how data loading fits into the basic training loop.

03:09.599-03:12.480
The difference between a map and an iterable style data set.

03:14.120-03:19.640
And then we'll even run it on a tiny time series transformer model using.

03:19.640-03:23.640
And then we'll even run it on a tiny time series transformer model.

03:23.640-03:26.760
And then we'll train a tiny time series transformer model using our

03:26.920-03:27.319
Vier

03:36.120-03:46.600
Before we proceed, the key idea I want you to understand is that a dataset is an object that wraps your source data living somewhere else, and its job is to produce a single sample.

03:46.720-03:47.760
From your data set.

03:47.760-03:49.360
That's all a dataset object does.

03:49.360-03:58.400
The data loader then takes that data set and does a bunch of other steps to produce these ready-made tensors in the form of a batch that'll be used in your training set.

04:58.160-05:03.040
All right, so before we dive into data loading, let's just take a look at our basic training loop.

05:08.680-05:17.080
Again, at a high level, the data loader is actually going to be yielding us a batch, which is a bunch of samples ready to be sent to the GPU for our training step.

05:17.420-05:21.900
That batch is then sent into the forward pass or at least the input part of that batch.

05:21.900-05:28.220
The forward pass takes its results to compute our loss of what the model actually currently predicts against some target.

05:28.139-05:30.460
That loss isn't propagated backwards.

05:30.460-05:33.660
The weights are updated as part of gradient descent.

05:33.660-05:37.180
And that is basically one training loop here.

05:37.039-05:41.440
Now, the way this looks in pseudocode is we're iterating through a batch in our data letter.

05:41.440-05:50.800
So our data letter is yielding this endless stream of batches of data, and we continually training for some number of epochs, an epoch being when you pass through the whole data set at least once

05:50.560-05:52.560
So when this inner loop completes.

05:52.800-05:57.919
And again, if you just do this forward pass, you get the loss, and then you do your backward pass, and that updates the weights.

06:31.220-06:34.419
Alright, so now if we drill into this data loader part.

06:41.320-06:45.480
It looks like this and this looks a maybe a lot going on here.

06:45.860-06:47.060
It looks like this.

06:47.060-06:54.180
Now I'm showing you two separate styles of datasets, but they all flow into this data loader object that does roughly the same thing.

06:54.220-06:59.580
The map style dataset includes this additional piece called a sampler.

06:59.580-07:02.940
The sampler uses the length of your dataset

07:03.580-07:09.740
to generate a random sequence of indices to say this is the sample order we're going to pull from.

07:09.740-07:13.340
And then the dataset calls getItem on that index.

07:13.060-07:20.259
So the sampler creates the ordering of your data, the dataset, you have to implement this getItem function, and that's how you fetch one sample from your data.

07:20.259-07:24.259
Now, map style datasets should be used until you can't use them anymore.

07:23.900-07:30.220
Basically, if your data is small enough that doing random access like one sample at a time is efficient or good enough, they're fine to do.

07:30.220-07:32.460
They're pretty simple, they're straightforward.

07:32.860-07:35.180
This feeds your samples here.

07:35.180-07:44.460
If that is not the case for your dataset, the other approach is this iterable style data set where you implement this iter function, and that iter function yields samples.

07:45.400-07:53.960
Either way, the dataset again is just showing the data loader how to go get one sample from your dataset.

07:55.900-07:58.780
Then the data loader has several pieces here.

07:58.780-08:01.660
So it has these workers that you can span out in parallel.

08:01.660-08:05.420
So you'll have multiple data loaders perhaps calling this dataset object.

08:05.360-08:08.800
It'll collect some number of samples to build your batch.

08:08.800-08:16.960
Then it collates them, which is basically just packing them in a nice shape so that it's optimized in the tensor for our GPUs.

08:17.780-08:24.180
And then collation is basically just packing those batches into a nice shape or into our tensor that we'll actually send to the GPUs.

08:24.180-08:25.940
And then we output this batch.

08:31.680-08:36.959
And then if you come back to training, that batch right here is what we feed into our forward pass.

08:37.760-08:42.640
And then we come back to the training loop, that batch is what we feed into the forward pass for one training step

09:07.040-09:10.880
Alright, so now what does this look like in code?

09:11.280-09:17.840
So here I have a notebook using a tiny time series transform model I've implemented called Nano TST

09:17.800-09:19.399
It is a basic transformer model.

09:19.399-09:23.160
The tokens are roughly patches of 32 time steps of time series data.

09:23.160-09:25.800
It uses synthetically generated time series data.

09:27.240-09:30.839
And so the way I have this working today is this is our training loop.

09:32.860-09:36.380
We iterate through some number of epochs that we set.

09:36.380-09:38.380
We get a random sequence of our data.

09:38.380-09:41.420
So this is kind of like a random sampler here that's implemented.

09:41.420-09:44.220
Takes the length of our data set, gives us a random sequence.

09:43.959-09:48.360
And then we iterate through one batch at a time of that random sequence doing our training loop.

09:48.360-09:50.120
So this is today how nanoTST works.

09:50.120-09:53.160
There's no data loading classes used.

09:53.160-09:54.839
But we're going to change that.

10:23.780-10:29.940
Okay, and so this here is the map style dataset for our synthetic time series.

10:29.839-10:33.839
You can see we implemented both the length and the getItem dunder functions.

10:34.160-10:36.720
Length just returns the self of the series.

10:37.199-10:39.920
Length just returns the length of our series.

10:39.920-10:42.800
And then this get item just knows how to slice into that series.

10:42.800-10:44.480
Again, it's just returning the index.

10:44.440-10:48.440
Because our series here is synthetically generated from this make series function.

10:48.440-10:53.400
So when this object is created, make series will generate a bunch of time series data.

10:53.400-10:56.840
And now these are just different um methods for generating

10:57.080-11:00.040
or randomizing a sequence of time series data.

11:00.360-11:07.400
But we generate some number of series here stored in this object and then we can slice into it using this map style data set.

11:07.400-11:11.960
So you see here the only two functions you need are this length and getItem.

11:18.540-11:21.500
And so we it's we instantiate that data set just like this.

11:21.740-11:24.300
Say we'll generate 500 series.

11:23.959-11:27.240
You take a look, it generates something looking like this, a bunch of different shapes.

11:27.240-11:29.959
This is our time series data then for our transformer.

11:33.000-11:35.160
And then we wrap this in the data loader.

11:35.160-11:37.880
So if you remember from this diagram.

11:43.840-11:48.880
So if you remember from this diagram, the data set is just one part of this data loader.

11:48.880-11:55.120
So we actually feed this data set to the data loader and the data loader handles all these different steps for us to build the batches.

11:54.839-11:56.680
And so that's what that looks like here.

11:56.680-12:01.560
We have our data loader, we pass in the data set, we set the batch size, that's the batcher.

12:01.560-12:06.920
This optional argument here to shuffle that acts as like our default random sampler.

12:11.200-12:15.200
And we can just keep calling next on the loader to get a batch.

12:47.280-12:52.080
And then we can just instantiate our model, call train, and we're good to go.

13:01.400-13:05.640
Now if you can't use a map style dataset because there's not an easy way to

13:05.839-13:13.759
randomly select a single index first or rather because there's not an easy way now if you can't use a map style data set because there's just not a fix

13:14.600-13:21.079
Now if you can't use a map style data set because it's not effective enough to look up a single sample, you will use an iterable dial dataset.

13:21.079-13:23.560
And this is what I tend to use more in my day

13:24.620-13:28.620
And iterable style data sets are more commonly used, especially as you're training larger models.

13:28.620-13:33.019
You do these techniques like packing shards of data that you then stream through into the model.

13:33.040-13:35.519
And so here we just have to implement this iter function.

13:35.519-13:39.200
There is no length, you just continually yield samples from this dataset.

13:50.160-13:56.000
And so here what we do is we inherit from this iterable dataset class, and we implement this iter function.

13:58.400-14:02.960
And what this iter function will do is it's going to continually yield a sample.

14:10.140-14:16.780
The rest of this in here is just some boilerplate so that we are generating unique samples per dayloader worker since we don't have a fixed

14:17.320-14:19.160
uh sequence of samples anymore.

14:19.160-14:20.280
There's no sampler here.

14:20.280-14:22.600
We need to do some shuffling or randomization on our own.

14:22.600-14:26.520
So we handle that deterministically based on a seed and based on the worker.

14:26.520-14:29.880
So when this is called, we're generating data on the fly.

14:29.560-14:37.960
Now, if you were using this on some data that's already been pre-processed on something like S3, you would pre-shuffle the data into maybe shards.

14:38.120-14:41.160
You can load the shard into memory and then yield samples from that shard.

14:41.160-14:43.960
So keeping a small slice of data in memory.

14:43.180-14:44.139
to reduce network I.

14:44.220-14:44.380
O.

14:44.699-14:49.660
There's many different techniques there, but the idea is there's no more sampler telling you what index to call data.

14:49.660-14:53.500
It just calls this data set object over and over again to yield the sample.

14:53.500-14:56.459
So you have to handle the randomization on your own.

15:05.000-15:08.440
And then similarly we implement the dataset.

15:08.759-15:14.360
And then similarly we instantiate the dataset here into the stream variable.

15:14.259-15:16.740
And then we pass that to our data loader.

15:16.980-15:22.980
And then that is what we use with our model after we'd sent you your model and we're able to train.

15:31.660-15:38.780
And then one of the key things I was alluding to earlier is when you run an iterable data set with some fixed number or sorry.

15:38.660-15:48.500
And then one thing I was alluding to earlier is when you run an integral dataset with multiple workers, you need to handle how you split the data among workers because every worker is going to get that same dataset object.

15:48.400-15:56.800
So if you're starting from the same random seed or you're not letting them know the or you're not passing in the worker info along, they could be generating the same data or pulling the same exact data.

15:56.800-15:59.760
So you again, something to be aware of, you have to handle that.

15:59.400-16:05.560
Whereas when you're using the sampler, it's assigning indices and sh and spreading that out among the different workers.

17:29.660-17:35.660
Okay, so this is a little web UI I made for our nano time series transformer model.

17:39.880-17:43.320
Very quickly, this is the architecture of the model.

17:43.320-17:47.000
It's just a basic transformer stack with an embedding layer.

17:47.000-17:50.680
We take the time series, we slice it into these patches, embed those.

17:50.460-17:57.820
Those patches or chunk of sequential time steps are our tokens that flow through a couple of attention layers.

17:57.820-18:01.260
Then we output the next patch or the next token prediction.

18:04.640-18:09.680
And now the data is all synthetic generated, so we you know generate a couple SIME series that look like this.

18:09.680-18:12.720
Again, this is CPU only, so it's meant to only learn a few patterns.

18:12.720-18:16.160
Um, but we can go ahead and watch this train.

18:37.640-18:43.720
And so now what we're watching is the model learning each epoch.

18:43.720-18:44.760
So we're going to be

19:37.680-19:41.600
And so now this model is actually just using our CPU to train.

19:41.400-19:50.760
It is running very short epochs on again our synthetically generated time series data that on our synthetically generated time series data that we're now using our data loaders to load.

19:51.160-19:54.440
We can see this is the model loss over time.

19:56.880-20:01.040
And then over here we can see how the model is learning some basic shapes.

20:01.040-20:03.760
So we have some like a sine wave trend, a flat line.

20:03.760-20:07.040
The model's already learned a flat line, how to predict that.

20:07.060-20:12.340
And in this short amount of time we can solely watch it get a little bit better at these other types of shapes.

20:12.740-20:16.740
One thing we could always come play with is the different types of data we're generating.

20:21.300-20:27.780
Alright, so I'm just gonna take the the hook again from the top.

20:27.780-20:31.380
Today we're gonna be talking about data loading in PyTorch.

20:32.799-20:41.120
I'll walk you through where it fits into the basic training loop, the two different types of datasets that you can use, a map versus an interval, and when you should use each.

20:41.919-20:45.280
And then we'll run it on a tiny time series transformer mod.

20:50.340-20:55.539
The key idea I want you to know the key idea I want you to walk away with is that a dataset

20:58.080-21:04.080
The key idea I want you to walk away with is that in PyTorch there are two big classes, the dataset and the data loader.

21:04.080-21:09.280
The dataset's job is to yield one sample from your dataset wherever that lives.

21:08.860-21:20.059
The data loader's job is to take that data set, call it however many times it needs to, batch all that data, group it into a ready-made tensor, and produce a batch that we can hand to the training.

21:25.919-21:32.480
A batch is just a bunch of samples packed into a ready-made tensor for the GPU to be able to paralyze its calculations.

21:43.120-21:47.520
All right, so we finished 25 epochs through our synthetic data.

21:47.920-21:51.520
We can see our model was learning stuff, training losses going down.

21:51.520-21:57.280
And one of the cool features I added on this web UI is this ability to look at the eval set at different points in training.

21:57.240-22:03.480
So here uh at epoch zero before we even started training, so this is with weights randomly initialized.

22:03.480-22:06.840
This is what, or sorry, this is after epoch one.

22:06.840-22:07.720
No, this is with rand

22:08.160-22:11.120
This is with random initialization, this is the model.

22:11.120-22:11.440
Um

22:15.960-22:17.960
Yeah, so we can s let me just take that back.

22:17.960-22:25.000
Uh and so one of the cool features I added to this UI is the ability to replay the uh eval results at the end of each epoch.

22:24.800-22:30.960
And so this is just like a tiny eval set here, trying to predict a sine wave, a you know, a little jump in the data.

22:30.960-22:35.760
The black lines are what the actual data looks like, and the blue is the prediction.

22:35.760-22:38.000
So we can see here after one epoch the model

22:38.060-22:39.500
Can't really predict a trend.

22:39.500-22:41.580
It's not so good at predicting the sine wave.

22:41.580-22:47.580
It does have a flat line, and then you can see epoch over epoch, how our model actually learns over time.

22:47.460-22:52.660
And even though it's not perfect, we do see improvement just using this CPU only training.

22:52.660-22:55.140
After twenty five epochs, we kinda get the trending down.

22:55.140-22:58.260
It's very noisy, but the sine wave, the jump is a little bit better.

22:58.260-23:01.060
Uh and I think this is kind of neat because this is just on the CPU.

23:01.060-23:01.860
This takes

23:01.740-23:02.780
10 minutes to train.

23:02.780-23:08.380
It's a very tiny transformer model using synthetic data that you just generated on your computer as well.

23:08.380-23:11.180
And we're able to predict some of this.

23:11.180-23:13.580
And we're able to predict some of these shapes.

23:14.260-23:15.620
That's all I have for you today.

23:15.620-23:16.580
Thank you so much for watching.

23:16.740-23:22.019
In the next video, I'll dive a little bit deeper into how we can use torch data nodes instead of the

23:24.180-23:24.900
Pause.

23:24.900-23:26.100
Thank you so much for watching.

23:26.100-23:27.380
I'll see you in the next one.

23:28.500-23:29.780
Thank you so much for watching.

23:29.780-23:35.380
In the next one, I'll talk about how we can use torch data nodes instead of these dataset and data loader objects.

23:35.000-23:48.280
Torch data nodes is a composable way to build pipelines and kind of replaces some of the inner workings of the data loader with individual steps that you can call instead and get allows for more flexibility as well for stateful training.


