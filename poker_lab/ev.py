"""EV math for facing a bet.

Assumes the hand goes to showdown after you call (no further betting).
That's exact for all-ins and river calls, a simplification otherwise.

pot = pot size BEFORE the opponent's bet
bet = size of the opponent's bet (what you have to call)
"""


def required_equity(pot, bet):
    """Break-even equity: you risk `bet` to win `pot + bet`."""
    return bet / (pot + 2 * bet)


def call_ev(equity, pot, bet):
    """Expected chips won by calling (folding = 0)."""
    return equity * (pot + bet) - (1 - equity) * bet
