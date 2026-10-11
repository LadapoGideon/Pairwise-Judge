import unittest

from pairwise import map_to_model, position_bias, swap_consistency, win_rates


class PairwiseTests(unittest.TestCase):
    def test_map_to_model_follows_the_response_not_the_position(self):
        self.assertEqual(map_to_model("A", ("gpt", "claude")), "gpt")
        self.assertEqual(map_to_model("B", ("gpt", "claude")), "claude")
        self.assertEqual(map_to_model("tie", ("gpt", "claude")), "tie")

    def test_position_bias_detects_a_favourite_slot(self):
        verdicts = ["A", "A", "A", "B"]
        self.assertEqual(position_bias(verdicts), 0.75)

    def test_position_bias_ignores_ties(self):
        self.assertEqual(position_bias(["A", "B", "tie", "tie"]), 0.5)

    def test_swap_consistency(self):
        pairs = [("gpt", "gpt"), ("gpt", "claude"), ("claude", "claude"), ("tie", "tie")]
        self.assertEqual(swap_consistency(pairs), 0.75)

    def test_win_rates_count_ties_as_half(self):
        results = ["gpt", "gpt", "claude", "tie"]
        rates = win_rates(results)
        self.assertEqual(rates["gpt"], round((2 + 0.5) / 4, 4))
        self.assertEqual(rates["claude"], round((1 + 0.5) / 4, 4))

    def test_empty_inputs_raise(self):
        with self.assertRaises(ValueError):
            position_bias([])
        with self.assertRaises(ValueError):
            swap_consistency([])


if __name__ == "__main__":
    unittest.main()
