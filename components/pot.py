class Pot:
    highest_bet: float
    value: float

    def __init__(self):
        self.value = 0
        self.highest_bet = 0
        self.is_full = False

    def add(self, amount):
        if amount < 0:
            raise ValueError("amount added to pot can only be positive")
        self.value += amount

