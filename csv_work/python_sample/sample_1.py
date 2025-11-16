# ✅ Python Question 1 — Most Frequent Item
# Problem:
# Given a list of strings items, return the item that appears most frequently. If multiple items are tied, 
# return the lexicographically smallest one
# Function Signature:
# def most_frequent_item(items: list[str]) -> str:
#     pass
# Sample Input:
# ['apple', 'banana', 'apple', 'orange', 'banana', 'banana']
# Expected Output:
# 'banana'

from collections import Counter

def most_frequent_item(items: list[str]) -> str:
    counts = Counter(items)
    max_count = max(counts.values())
    
    # get all items tied for max frequency
    candidates = [item for item, cnt in counts.items() if cnt == max_count]
    
    return min(candidates)  # lexicographically smallest


mylist = ['apple', 'banana', 'apple', 'orange', 'banana', 'banana']

print(most_frequent_item(mylist))