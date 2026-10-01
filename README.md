# Poker Lab

Equity + EV calculator for Texas Hold'em.

## Setup
    pip install -r requirements.txt

## Usage
    python main.py --hand AhKd --range "TT+, AQs+, AKo" --board Qs7c2d --pot 100 --bet 75

Range syntax: `AA`, `AKs`, `AKo`, `AK` (suited + offsuit), `TT+`, `A9s+`, `AhKh`.
