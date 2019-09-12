class User:
    def __init__(self, name, balance=0):
        self.name = name
        self.balance = balance

    def get_balance(self):
        return self.balance

    def remove_money(self, quantity):
        self.balance -= float(quantity)

    def add_money(self, quantity):
        self.balance += float(quantity)
