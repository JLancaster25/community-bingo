import random

PHRASES = {
    "B": [
        "B {n}, beginners luck",
        "B {n}, early bird",
        "B {n}, number {n}"
    ],
    "I": [
        "I {n}, legs eleven",
        "I {n}, straight down the middle",
        "I {n}, coming alive"
    ],
    "N": [
        "N {n}, halfway there",
        "N {n}, lucky number",
        "N {n}, right on time"
    ],
    "G": [
        "G {n}, gateway to bingo",
        "G {n}, great pick",
        "G {n}, getting close"
    ],
    "O": [
        "O {n}, almost there",
        "O {n}, outer limits",
        "O {n}, eyes open"
    ]
}

def call(number):
    if number <= 15: l = "B"
    elif number <= 30: l = "I"
    elif number <= 45: l = "N"
    elif number <= 60: l = "G"
    else: l = "O"

    return random.choice(PHRASES[l]).format(n=number)
