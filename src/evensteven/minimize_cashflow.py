from collections import defaultdict

def split_expenses(transactions):
    # Step 1: Calculate the total expense
    total_expense = sum(amount for _, _, amount in transactions)

    # Step 2: Calculate the expense for each person
    person_expenses = defaultdict(float)
    for person, item, amount in transactions:
        person_expenses[person] += amount

    # Step 3: Calculate the net balance for each person
    net_balances = defaultdict(float)
    for payer, _, amount in transactions:
        net_balances[payer] -= amount
    for person, expense in person_expenses.items():
        net_balances[person] += expense

    # Step 4: Minimize transfers by matching lenders and borrowers
    lenders = []
    borrowers = []
    for person, balance in net_balances.items():
        if balance > 0:
            lenders.append((person, balance))
        elif balance < 0:
            borrowers.append((person, -balance))

    lenders.sort(key=lambda x: x[1], reverse=True)
    borrowers.sort(key=lambda x: x[1])

    transfers = []
    i, j = 0, 0
    while i < len(lenders) and j < len(borrowers):
        lender, lender_balance = lenders[i]
        borrower, borrower_balance = borrowers[j]

        transfer_amount = min(lender_balance, borrower_balance)
        transfers.append((lender, borrower, transfer_amount))

        lender_balance -= transfer_amount
        borrower_balance -= transfer_amount

        if lender_balance == 0:
            i += 1
        if borrower_balance == 0:
            j += 1

    return transfers

# Example usage
transactions = [
    ('Alice', 'pasta', 50),
    ('Alice', 'water', 5),
    ('Bob', 'beer', 15),
    ('Charlie', 'cheese plate', 40),
    ('David', 'cheese plate', 40),
    ('Charlie', 'drink', 10),
    ('David', 'drink', 10),
    ('David', 'total', 170)  # David paid the entire bill
]

result = split_expenses(transactions)
print(result)