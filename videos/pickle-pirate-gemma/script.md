VO script — your arc, your words
CLIP 00 opening
You can do more than just prompt an LLM. I took an open-weights model, looked inside to find specific concepts, and manipulated the model from the inside.


--

CLIP 2 - alpha sweep
By doing this I can find a specific ocncept like pickle, and crank it up on the same prompt. Doing this you can see the effect. Model starts liking pizza and as we crank up the concept of picklness by amplifying 


Let me explain how this is even possible

--

06c - residual stream

The way a language model works is it takes some input this gets split into tokens where each becomes a vecot known as an embedding.

this vector is what flows through the layers of the model, each layer updates the vector a little bit with what it has learned (this is the transformer stack through attention)

this final vector is them unembedded into logits which is a raw score that gets softmaxed into a probability to select the last word

(double check and time)

---

transiont
Now the reason this works is because thes nubmers in a very high dimensionl space capture meaning

through trainign the model learns to put these thigns next to each others

CLIP 4 — ConceptSpace (~20s) | direction encodes meaning
(over words clustering) That vector is a direction — a point in high-dimensional space. The space means different things at each layer, but the principle is the same: the direction encodes meaning. Pickle sits near cucumber. 

--

A classic example takes the points for man, king, woman, queen

CLIP 5 — KingQueen (~25s) | king-queen example
Since this space encodes meaning, we can do vector math.

If we take the vector pointing to man subtract oman gives us vecto for this genderness - now if we apply this vector starting at king we should move the notino if king on the genderness direction toward queen.


if take this vector - move it up king you get notion of queen
now this is a famous example proving how you can do vector math and meaning is encoded in these embedding spaces


--

So in our example from earlier, we used a concept called mean-differencing to find pickles.

CLIP 6 — MeanDiff (~15s) | mean differencing
Now I need to identify a concept as a direction. The technique is called mean differencing. Here's how I did it. (over the cloud subtraction) Thirty sentences about pickles. Thirty sentences about other foods. Average each cloud. Subtract. (over the arrow drawing) What's left is the pickle direction.


Clip back to alpha morph to show thats how we found pickles


(optional) in sert layer sweep landscape

But now one specific detail to manetion is each layer has it's own space. So to find a concept we need to explore every layer with mean differencing to identify the concepts vector and test if we can find it there.
layers store different levels of abstraction as the model builds up its under standing.

so the process itook required me to check for a concept at each lyaer


---



Santa cruz clip
now my first attemp didnt quite work out, I was looking for the golden gat birdge to recreate a paper from Anthropic.

using our same technique of mean differencing I found what I thought was the golden gate bridgeness direction

but as i magnified this vector with this prompt something strange started to happen

falls off a cliff 

we got closter to bridge, but then the model get weird and degraded to gibberish.

now the reason it does this is interestion..

---

CLIP 9 — Superposition (~30s) | why it failed

Now the reason this failed is because in training a LLM a small model like I used sees enough examples of pickle to get a clear direction ofi


The reason is called superposition. The model has millions of concepts to store, but only a few thousand dimensions to put them in. Common things — pickle, rain, kindness — get their own clean spot. (over left side) Aim at pickle, hit pickle. (over right side) But rare specific things — like one particular bridge — don't get their own spot. They live as the overlap of California, San Francisco, famous bridge, fog. When I pulled on the Golden Gate direction, I pulled on the whole overlap.


this is called super position


whcih got me thinking, what if we combined multipel concepts at once?


---


CLIP 10 — Composition (~25s) | three together

because meaninng is captured as a vector we can add them to gether to create a new vector that pushes
in multiple directions at once

pirate direction plus pickle and golden gate from ealrier 

now we can see the model start get more creative 

the key difference between this an prmopting it to role play is and actually fuse goether these concepts at a token level - so you get words like golden dreadken






--

CLIP 11 — Closing (~50s) | outro
So why does this matter.

(takeaway 1) Steering is a real, separate lever. It's how safety researchers hunt for deceptive behavior in models without asking nicely. It's how someday you might get a "be more concise" toggle that actually works. A whole second control surface.

(takeaway 2) AI doesn't actually know specific things the way you think. Common concepts are points. Rare ones are weather. The way the model thinks about your name, your company, your niche — that's probably not a clean concept. It's a smear.

(takeaway 3) I used the 2022 method. Subtraction. Anthropic uses sparse autoencoders — tens of thousands of cleaner concept directions. The map is getting more readable every year.

-- much more effective but more expensive to train

(over "The box opens") Full writeup is in the description.
- idea to take away is we are jsut discoveriung now whats inside these models


