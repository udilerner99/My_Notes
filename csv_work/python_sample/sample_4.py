# ✅ Python Question 4 — Customer With Largest Single Order
# Problem:
# Given a list of orders, where each order is a tuple (customer_name: str, amount: int), return the customer(s) with the largest single order. If multiple customers tie, 
# return all names sorted alphabetically.
# Function Signature:
# def largest_order(orders: list[tuple[str, int]]) -> list[str]:
#     pass
# Sample Input:

# orders = [
#     ('Dana', 400), ('Dana', 150), ('Eli', 900), ('Fatma', 500)
# ]
# Expected Output:
# ['Eli']


def largest_order(orders: list[tuple[str, int]]) -> list[str]:
    max_amount = -1
    customer_with_max = []
    
    for customer, amount in orders:
        if amount > max_amount:
            max_amount = amount
            customer_with_max = [customer]
        elif amount == max_amount:
            customer_with_max.append(customer)
    return sorted(set(customer_with_max))

orders = [('Dana', 400), ('Dana', 150), ('Eli', 900), ('Fatma', 500)]

print(largest_order(orders))