"""Parse poker range notation (e.g. "TT+, AQs+, AKo, KQ") into card combos.

Every hand class expands into its actual combinations:
  pairs    -> 6 combos  (e.g. AA)
  suited   -> 4 combos  (e.g. AKs)
  offsuit  -> 12 combos (e.g. AKo)
  both     -> 16 combos (e.g. AK)
This is why AK shows up far more often than AA.
"""
from itertools import combinations

RANKS = "23456789TJQKA"
SUITS = "shdc"


def pair_combos(r):
    return [(r + s1, r + s2) for s1, s2 in combinations(SUITS, 2)]


def suited_combos(r1, r2):
    return [(r1 + s, r2 + s) for s in SUITS]


def offsuit_combos(r1, r2):
    return [(r1 + s1, r2 + s2) for s1 in SUITS for s2 in SUITS if s1 != s2]


def _class_combos(high, low, kind):
    if high == low:
        return pair_combos(high)
    if kind == "s":
        return suited_combos(high, low)
    if kind == "o":
        return offsuit_combos(high, low)
    return suited_combos(high, low) + offsuit_combos(high, low)


def parse_token(token):
    token = token.strip()
    if not token:
        return []

    # Specific combo like "AhKh"
    if len(token) == 4 and token[1] in SUITS and token[3] in SUITS:
        return [(token[:2], token[2:])]

    plus = token.endswith("+")
    body = token.rstrip("+")
    if len(body) not in (2, 3):
        raise ValueError(f"Can't parse range token: {token!r}")

    r1, r2 = body[0].upper(), body[1].upper()
    kind = body[2].lower() if len(body) == 3 else ""
    if r1 not in RANKS or r2 not in RANKS or kind not in ("", "s", "o"):
        raise ValueError(f"Can't parse range token: {token!r}")

    # Put the higher rank first
    if RANKS.index(r2) > RANKS.index(r1):
        r1, r2 = r2, r1

    if not plus:
        return _class_combos(r1, r2, kind)

    combos = []
    if r1 == r2:
        # "TT+" -> TT, JJ, QQ, KK, AA
        for r in RANKS[RANKS.index(r1):]:
            combos += pair_combos(r)
    else:
        # "A9s+" -> A9s, ATs, ... AKs (kicker climbs, top card fixed)
        for low in RANKS[RANKS.index(r2):RANKS.index(r1)]:
            combos += _class_combos(r1, low, kind)
    return combos


def parse_range(text):
    """Return a de-duplicated list of 2-card combos."""
    seen = set()
    result = []
    for token in text.split(","):
        for combo in parse_token(token):
            key = frozenset(combo)
            if key not in seen:
                seen.add(key)
                result.append(combo)
    return result
