"""Poker Lab CLI.

Example:
  python main.py --hand AhKd --range "TT+, AQs+, AKo" --board Qs7c2d --pot 100 --bet 75
"""
import argparse

from poker_lab.equity import equity_vs_range, split_cards
from poker_lab.ev import call_ev, required_equity
from poker_lab.ranges import parse_range


def main():
    p = argparse.ArgumentParser(description="Equity + EV calculator")
    p.add_argument("--hand", required=True, help="Your hole cards, e.g. AhKd")
    p.add_argument("--range", required=True, help='Villain range, e.g. "TT+, AQs+, AKo"')
    p.add_argument("--board", default="", help="Board cards, e.g. Qs7c2d")
    p.add_argument("--pot", type=float, help="Pot before villain's bet")
    p.add_argument("--bet", type=float, help="Villain's bet size")
    p.add_argument("--iters", type=int, default=20000, help="Simulations to run")
    p.add_argument("--seed", type=int, help="Random seed for repeatable results")
    args = p.parse_args()

    hero = split_cards(args.hand)
    board = split_cards(args.board) if args.board else []
    villain = parse_range(args.range)

    r = equity_vs_range(hero, villain, board, args.iters, args.seed)

    print(f"\nHand:  {' '.join(hero)}   Board: {' '.join(board) or '(preflop)'}")
    print(f"Range: {args.range}")
    print(f"Combos: {r['combos_live']} live / {r['combos_total']} total "
          f"({r['combos_blocked']} blocked by your cards + board)")
    print(f"\nEquity: {r['equity']:.1%}  (win {r['win']:.1%}, tie {r['tie']:.1%})")

    if args.pot is not None and args.bet is not None:
        need = required_equity(args.pot, args.bet)
        ev = call_ev(r["equity"], args.pot, args.bet)
        print(f"\nFacing {args.bet:g} into {args.pot:g}")
        print(f"Break-even equity: {need:.1%}")
        print(f"EV of calling:     {ev:+.2f}")
        print(f"Decision:          {'CALL' if ev > 0 else 'FOLD'}")
    print()


if __name__ == "__main__":
    main()
