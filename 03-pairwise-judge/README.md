# Pairwise Judge Analyser

Helps you check whether your AI judge is fair. It looks for three things:

1. **Position bias.** Does the judge pick "A" more often than "B"?
2. **Swap consistency.** When you swap the two responses, does the judge still pick the same model?
3. **Win rates.** Which model wins, with ties counted as half a win.

**Skills shown:** designing comparison tests, spotting bias in evaluations, working with the data behind a verdict.

## Run the tests

```
python3 -m unittest -v
```

## Typical flow

1. Run each prompt twice, once with model X as A and once with X as B.
2. Convert each verdict to a model name with `map_to_model`.
3. Pass the pairs to `swap_consistency`. Low consistency means the judge is unreliable on that task.
4. Use `position_bias` to check for slot preference. A value far from 0.5 is a warning.
