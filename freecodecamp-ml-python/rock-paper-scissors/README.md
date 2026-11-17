# Adaptive Rock–Paper–Scissors AI

An online ensemble learns which opponent behavior is most accurate: periodic sequences, reaction to our last play, frequency response, transition modeling, or n-gram patterns.

**Run:** `python main.py`. **Official tests:** `python -m unittest test_module.py`.

In a local 1,000-game test against each bot: Quincy ~99.6%, Abbey 100%, Kris ~99.9%, Mrugesh ~89% (win rate excludes ties). This clears the 60% threshold in those local tests; outcomes can vary.

Only `RPS.py` is the authored solution. `RPS_game.py`, `test_module.py` and `main.py` are credited, unchanged freeCodeCamp project starters from https://github.com/freeCodeCamp/boilerplate-rock-paper-scissors.
