import uuid
from evensteven.user import Group, User

class Transaction:
    def __init__(
        self,
        name: str,
        paid_by: int | list[int],
        owed_by: int | list[int],
        amount: float,
        currency: str
    ):
        self.id = uuid.uuid4().hex[:8]  # Generate random transaction ID
        self.name = name
        self.paid_by = paid_by
        self.owed_by = owed_by
        self.amount = amount
        self.currency = currency
    
    def __str__(self):
        return f"Transaction(id={self.id}, name='{self.name}', paid_by={self.paid_by}, owed_by={self.owed_by}, amount={self.amount}, currency='{self.currency}')"

    
    @staticmethod
    def create_new_transaction(name: str, paid_by: int | list[int], owed_by: int | list[int], amount: float, currency: str):
        return Transaction(name, paid_by, owed_by, amount, currency)


class TransactionAnalyzer:
    def __init__(self):
        self.transactions = {}

    def add_transaction(self, transaction):
        if transaction.paid_by not in self.transactions:
            self.transactions[transaction.paid_by] = {}
        if isinstance(transaction.owed_by, int):
            transaction.owed_by = [transaction.owed_by]
        for owed_to in transaction.owed_by:
            if owed_to not in self.transactions[transaction.paid_by]:
                self.transactions[transaction.paid_by][owed_to] = 0
            self.transactions[transaction.paid_by][owed_to] += transaction.amount

    def calculate_summary(self):
        summary = {}
        for payer, debts in self.transactions.items():
            for debtor, amount in debts.items():
                if debtor not in summary:
                    summary[debtor] = {}
                if payer not in summary:
                    summary[payer] = {}
                if debtor not in summary[payer]:
                    summary[payer][debtor] = 0
                if payer not in summary[debtor]:
                    summary[debtor][payer] = 0
                summary[payer][debtor] += amount
                summary[debtor][payer] -= amount
        return summary


class Transactions:
    def __init__(self,
        group_id: int,
        list_of_transactions: list[Transaction] = []
    ):
        self.group_id = group_id
        self.list_of_transactions = list_of_transactions if len(list_of_transactions)>0 else []
    
    def add_transactions(self, transaction: Transaction | list[Transaction]):
        if not isinstance(transaction, list):
            transaction = [transaction]
        self.list_of_transactions.extend(transaction)
    
    def remove_transaction(self, transaction: Transaction):
        self.list_of_transactions[:] = [item for item in self.list_of_transactions if item.id != transaction.id]
    
    def analyze_transactions(self):
        analyzer = TransactionAnalyzer()
        for transaction in self.list_of_transactions:
            analyzer.add_transaction(transaction)
        return analyzer.calculate_summary()


if __name__ == "__main__":
    user_group = Group()
    user1 = User("Alice")
    user2 = User("Bob")
    user_group.add_user(user1)
    user_group.add_user(user2)

    print("List of users:")
    for user in user_group.list_all_users():
        print(user)

    db = Transactions(user_group.id)
    transaction_1 = Transaction("lidl", user1.id, user2.id, 15.25, "DKK")
    transaction_2 = Transaction("bilka", user2.id, user1.id, 25.25, "DKK")
    db.add_transactions([transaction_1, transaction_2])

    print("\nList of transactions:")
    for transaction in db.list_of_transactions:
        print(transaction)

    summary = db.analyze_transactions()
    print("\nSummary of transactions:")
    print(summary)