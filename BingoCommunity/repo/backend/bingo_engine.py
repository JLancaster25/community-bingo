import random

BINGO_LETTERS = {
    "B": range(1, 16),
    "I": range(16, 31),
    "N": range(31, 46),
    "G": range(46, 61),
    "O": range(61, 76),
}


class BingoCard:
    def __init__(self):
        self.card = {
            letter: random.sample(list(numbers), 5)
            for letter, numbers in BINGO_LETTERS.items()
        }
        # Free space
        self.card["N"][2] = "X"

    def mark(self, number):
        for letter in self.card:
            for i, value in enumerate(self.card[letter]):
                if value == number:
                    self.card[letter][i] = "X"

    def has_bingo(self):
        grid = [self.card[l] for l in "BINGO"]

        # Rows
        for row in zip(*grid):
            if all(v == "X" for v in row):
                return True

        # Columns
        for col in grid:
            if all(v == "X" for v in col):
                return True

        # Diagonals
        if all(grid[i][i] == "X" for i in range(5)):
            return True

        if all(grid[i][4 - i] == "X" for i in range(5)):
            return True

        return False


class BingoGame:
    def __init__(self):
        self.deck = [
            f"{letter}{num}"
            for letter, nums in BINGO_LETTERS.items()
            for num in nums
        ]
        random.shuffle(self.deck)
        self.called = []

    def draw(self):
        if not self.deck:
            return None

        call = self.deck.pop()
        self.called.append(call)
        return call
