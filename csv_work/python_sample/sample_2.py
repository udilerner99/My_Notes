# ✅ Python Question 2 — Products Never Purchased
# Problem:
# Given two lists:
# products — all product names
# orders — list of purchased product names
# Return a list of products never purchased, sorted alphabetically.
# Function Signature:
# def never_purchased(products: list[str], orders: list[str]) -> list[str]:
#     pass
# Sample Input:
# products = ['Laptop', 'Mouse', 'Keyboard', 'Monitor', 'Webcam']
# orders = ['Laptop', 'Mouse', 'Monitor']
# Expected Output:
# ['Keyboard', 'Webcam']

# ⭐ Optional Improvements (If you want cleaner or faster versions)
# 🔹 Using a list comprehension
# def never_purchased(products, orders):
#     return sorted([p for p in products if p not in orders])

# 🔹 Using a set for performance (recommended for large inputs)
# def never_purchased(products, orders):
#     orders_set = set(orders)
#     return sorted([p for p in products if p not in orders_set])
# This avoids repeated O(n) membership checks.

def never_purchased(products: list[str], orders: list[str]) -> list[str]:
    never_purchased_list = []
    for product in products:
        if product not in orders:
            never_purchased_list.append(product)
    return sorted(never_purchased_list)

products = ['Laptop', 'Mouse', 'Keyboard', 'Monitor', 'Webcam']
orders = ['Laptop', 'Mouse', 'Monitor']

print(never_purchased(products, orders))