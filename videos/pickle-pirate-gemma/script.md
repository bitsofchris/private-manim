VO script — your arc, your words
CLIP 00 opening
You can do more than just prompt an LLM. I took an open-weights model, looked inside to find specific concepts, and manipulated the model from the inside.


--

CLIP 2 - alpha sweep
By doing this I can find a specific ocncept like pickle, and crank it up on the same prompt. Doing this you can see the effect. Model starts liking pizza and as we crank up the concept of picklness by amplifying 

(Maybe instead of cold open - we do alphasweep morph - Here i found the concept of pickle inside the model, with this same prompt as we crank it up watch what happens.)

Clip 2 - alpha sweep
For example, i found the concept of pickles inside Gemma 2B. with tis prompt not changing we can see it's responses change as we increasae the pickle weight in the models, until it hits full obsesson mode

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


CLIP 4 — ConceptSpace (~20s) | direction encodes meaning
(over words clustering) That vector is a direction — a point in high-dimensional space. The space means different things at each layer, but the principle is the same: the direction encodes meaning. Pickle sits near cucumber. 

--

A classic example takes the points for man, king, woman, queen

CLIP 5 — KingQueen (~25s) | king-queen example
Since this space encodes meaning, we can do vector math.

If we take the vector pointing to man subtract oman gives us vecto for this genderness - now if we apply this vector starting at king we should move the notino if king on the genderness direction toward queen.


--

So in our example from earlier, we used a concept called mean-differencing to find pickles.

CLIP 6 — MeanDiff (~15s) | mean differencing
Now I need to identify a concept as a direction. The technique is called mean differencing. Here's how I did it. (over the cloud subtraction) Thirty sentences about pickles. Thirty sentences about other foods. Average each cloud. Subtract. (over the arrow drawing) What's left is the pickle direction.

now my first attemp didnt quite work out

CLIP 8 — SantaCruz (~30s) | golden gate fails
Then I tried the same trick with the Golden Gate Bridge. Anthropic did this in 2024 — they made their model obsessed with the bridge. I tried to copy them. Same method. Thirty bridge sentences, thirty other-bridge sentences, subtract. Prompt: "My favorite place in the whole world is…" (small) Santa Cruz, California. (bigger) The place where I was born. (bigger) Physics equations. The model started spitting out cubic meters. (maximum) Just broken tokens. (beat) It never mentioned the Golden Gate Bridge. Not once.

CLIP 9 — Superposition (~30s) | why it failed
The reason is called superposition. The model has millions of concepts to store, but only a few thousand dimensions to put them in. Common things — pickle, rain, kindness — get their own clean spot. (over left side) Aim at pickle, hit pickle. (over right side) But rare specific things — like one particular bridge — don't get their own spot. They live as the overlap of California, San Francisco, famous bridge, fog. When I pulled on the Golden Gate direction, I pulled on the whole overlap.

Steering vector? clip?

CLIP 10 — Composition (~25s) | three together
Directions can be added. So I built three: pirate, pickle, and the Golden-Gate-ish vector. I turned all three on at once. (over Golden Dreadken materializing) And the model gave me — Golden Dreadken. The pirate ship from the cold open. "Golden" from one direction, "Kraken" from another, fused into a single word because no real word satisfied all three pulls at once. That's the signature. A made-up word is what proves steering happened. No prompt could have produced it.

CLIP 11 — Closing (~50s) | outro
So why does this matter.

(takeaway 1) Steering is a real, separate lever. It's how safety researchers hunt for deceptive behavior in models without asking nicely. It's how someday you might get a "be more concise" toggle that actually works. A whole second control surface.

(takeaway 2) AI doesn't actually know specific things the way you think. Common concepts are points. Rare ones are weather. The way the model thinks about your name, your company, your niche — that's probably not a clean concept. It's a smear.

(takeaway 3) I used the 2022 method. Subtraction. Anthropic uses sparse autoencoders — tens of thousands of cleaner concept directions. The map is getting more readable every year.

(over "The box opens") Full writeup is in the description.



---



(Artifact here - without prompting I got the LLm to say this)

This is a way to give LLMs new capabilities without having to train them. The Inside of LLMs have meaning we can explore, it’s an under explored frontier.

Here’s how I did it and why this technique matters. (Now the value prop for viewer)?

Model is set of parameters learned from training. When input it’s turned into embedding vector that flows through model. Models have different layers and params. Each layer adding context to the input. This input is the residual stream flowing through. Each layer the new embedding is the activation vector.

Now this vector is a direction. A point in high dimensional space. The embedding/ activation same size but space means different things at each layer. But the direction in space encodes meaning. (Man king queeen example?)

Identifying concept. Technique called mean differencing. How I did it.

Pickle.
Golden gate- why it failed. Super position.
Three together.

Outro of how this is used, why interesting.