import random


PHRASES = {
"B": ["B", "B-line", "Bee"],
"I": ["I", "Eye"],
"N": ["N", "En"],
"G": ["G", "Gee"],
"O": ["O", "Oh"]
}


EXTRAS = ["", "— lucky!", "— mark it!", "— eyes down!"]


def call_phrase(call):
letter, number = call[0], call[1:]
return f"{random.choice(PHRASES[letter])} {number} {random.choice(EXTRAS)}"