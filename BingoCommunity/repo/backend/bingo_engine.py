# FILE: bingo_engine.py
def __init__(self):
self.card = {
letter: random.sample(list(numbers), 5)
for letter, numbers in BINGO_LETTERS.items()
}
self.card["N"][2] = "X" # Free space


def mark(self, number):
for letter in self.card:
for i, value in enumerate(self.card[letter]):
if value == number:
self.card[letter][i] = "X"


def has_bingo(self):
grid = [self.card[l] for l in "BINGO"]
for row in zip(*grid):
if all(v == "X" for v in row): return True
for col in grid:
if all(v == "X" for v in col): return True
if all(grid[i][i] == "X" for i in range(5)): return True
if all(grid[i][4-i] == "X" for i in range(5)): return True
return False




class BingoGame:
def __init__(self):
self.deck = [f"{l}{n}" for l, nums in BINGO_LETTERS.items() for n in nums]
random.shuffle(self.deck)
self.called = []


def draw(self):
if not self.deck: return None
call = self.deck.pop()
self.called.append(call)
return call