class Transactions:
    def __init__(self, data_point):
        self.date = data_point[0]
        self.payer = data_point[1]
        self.payee = data_point[2]
        self.reason = data_point[3]
        self.amount = float(data_point[4])

    def __repr__(self):
        return f"Date {self.date}, Reason {self.reason}"
