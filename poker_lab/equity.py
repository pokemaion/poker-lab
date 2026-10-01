"""Monte Carlo equity: your hand vs an opponent's range."""
import random

from treys import Card, Evaluator

from .ranges import RANKS, SUITS

FULL_DECK = [r + s for r in RANKS for s in SUITS]
_evaluator = Evaluator()


def split_cards(text):
    """'AhKd' -> ['Ah', 'Kd']"""
    text = text.replace(" ", "")
    if len(text) % 2:
        raise ValueError(f"Bad card string: {text!r}")
    cards = [text[i].upper() + text[i + 1].lower() for i in range(0, len(text), 2)]
    for c in cards:
        if c not in FULL_DECK:
            raise ValueError(f"Not a card: {c!r}")
    if len(set(cards)) != len(cards):
        raise ValueError(f"Duplicate card in {text!r}")
    return cards


def equity_vs_range(hero, villain_range, board=None, iters=20000, seed=None):
    """
    hero: ['Ah', 'Kd']
    villain_range: list of (card, card) combos
    board: 0, 3, 4, or 5 cards
    Returns a dict with equity plus blocker info.
    """
    board = board or []
    if len(board) not in (0, 3, 4, 5):
        raise ValueError("Board must have 0, 3, 4, or 5 cards")

    dead = set(hero) | set(board)

    # Blockers: combos that use a card you can see are impossible
    live = [c for c in villain_range if not (set(c) & dead)]
    if not live:
        raise ValueError("Every combo in the villain range is blocked by known cards")

    rng = random.Random(seed)
    hero_int = [Card.new(c) for c in hero]
    board_int = [Card.new(c) for c in board]
    to_deal = 5 - len(board)

    wins = ties = 0
    for _ in range(iters):
        v = rng.choice(live)  # each combo equally likely
        used = dead | set(v)
        remaining = [c for c in FULL_DECK if c not in used]
        runout = board_int + [Card.new(c) for c in rng.sample(remaining, to_deal)]

        hero_score = _evaluator.evaluate(runout, hero_int)
        vill_score = _evaluator.evaluate(runout, [Card.new(c) for c in v])
        # treys: lower score = stronger hand
        if hero_score < vill_score:
            wins += 1
        elif hero_score == vill_score:
            ties += 1

    return {
        "equity": (wins + ties / 2) / iters,
        "win": wins / iters,
        "tie": ties / iters,
        "combos_total": len(villain_range),
        "combos_live": len(live),
        "combos_blocked": len(villain_range) - len(live),
    }
