"""Adaptive online ensemble for the freeCodeCamp RPS challenge."""
from collections import Counter, deque
MOVES = "RPS"
COUNTER = {"R": "P", "P": "S", "S": "R"}

def _predict(my_moves, their_moves):
    predictions = {}
    if len(their_moves) >= 10 and their_moves[-5:] == their_moves[-10:-5]:
        predictions["periodic"] = their_moves[-5]
    predictions["reactive"] = COUNTER[my_moves[-1]] if my_moves else "P"
    recent = ([""] + my_moves)[-10:]
    counts = Counter(recent)
    max_count = max(counts.values())
    leaders = [move for move, count in counts.items() if count == max_count]
    if len(leaders) == 1:
        predictions["frequency"] = COUNTER[leaders[0] if leaders[0] else "S"]
    h = ["R"] + my_moves
    pairs = Counter(a + b for a, b in zip(h, h[1:]))
    previous = h[-1]
    predictions["transition"] = COUNTER[max(MOVES, key=lambda move: pairs[previous + move])]
    for k in (4, 3, 2, 1):
        if len(their_moves) >= k + 5:
            context = their_moves[-k:]
            follows = Counter(their_moves[i+k] for i in range(len(their_moves)-k)
                              if their_moves[i:i+k] == context)
            if sum(follows.values()) >= 2:
                predictions["ngram"] = follows.most_common(1)[0][0]
                break
    return predictions

def player(prev_play, state={}):
    """Return R/P/S while learning which opponent model is most accurate."""
    if not prev_play or "mine" not in state:
        state.clear()
        state.update(mine=[], theirs=[], prior={}, results={})
    else:
        state["theirs"].append(prev_play)
        for name, guess in state["prior"].items():
            state["results"].setdefault(name, deque(maxlen=40)).append(int(guess == prev_play))
    predictions = _predict(state["mine"], state["theirs"])
    def quality(name):
        record = state["results"].get(name, ())
        return (sum(record) / len(record) if record else 0.0, len(record))
    candidates = [name for name in predictions if len(state["results"].get(name, ())) >= 4]
    if candidates:
        guess = predictions[max(candidates, key=quality)]
    elif "periodic" in predictions:
        guess = predictions["periodic"]
    else:
        guess = predictions.get("transition", "R")
    action = COUNTER[guess]
    state["prior"] = predictions
    state["mine"].append(action)
    return action
