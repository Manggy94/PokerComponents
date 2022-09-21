class Pot:
    highest_bet: float
    min_bet: float
    max_bet: float
    value: float

    def __init__(self):
        self.value = 0
        self.highest_bet = 0
        self.max_bet = 0

    def add(self, amount):
        if amount < 0:
            raise ValueError("amount added to pot can only be positive")
        self.value += amount

