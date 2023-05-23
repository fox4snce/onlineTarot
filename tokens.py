# tokens.py
class TokenManager:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.tokenTotal = 0
            cls._instance.totalCost = 0.0
        return cls._instance

    def update_tokens(self, total_tokens):
        self.tokenTotal += total_tokens
        cost = total_tokens * 0.002 / 1000
        self.totalCost += cost

    def get_totals(self):
        return self.tokenTotal, self.totalCost

    def print_totals(self):
        print(f"Token total: {self.tokenTotal}")
        print(f"Total cost: ${self.totalCost:.5f}")
