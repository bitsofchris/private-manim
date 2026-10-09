# Matrix Multiplication Explained Visually (x @ W)

`vo_raw.m4a`: 62.5 s, cut from `002-linear-algebra-shorts-ALL.m4a` at 193.09–255.55 s (episode announcement removed). Planned script: `../SCRIPTS.md`.

## As recorded

X at W is just a weighted sum of W's rows. It's the one operation inside every linear layer. Take X equals one, two, minus one, and W a three by two matrix

Three rows, one for each input direction, each a 2D landing spot. Now turn X sideways so it sits beside W. Now each number in X is a weight for one row. One times the first row, two times the second row, minus one times the third row. Now we have three weighted 2D vectors., To add vectors, you add first coordinates together and second coordinates together.

That's summing down the columns. Four minus one, that's X at W Rows are where input directions land. Columns are the totals in each output direction. Add the bias and you have one row of a linear layer's output, four point one minus one point two. Each number in X weights a row of W. Add the rows and you're done
