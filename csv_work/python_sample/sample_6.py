# ✅ SECTION 1 — Python Coding Questions (with answers)
# 1️⃣ Find the first non-repeating character in a string
# Question
# Given a string, return the first character that appears exactly once.
# If none exist, return "_".
# Solution
def first_unique_char(s: str) -> str:
    counts = {}

    for c in s:
        counts[c] = counts.get(c, 0) + 1

    for c in s:
        if counts[c] == 1:
            return c

    return "_"

print(first_unique_char("swiss"))  # Output: "w"

# # 2️⃣ Rotate array to the right by K steps
# # Question
# # Rotate the array to the right by K positions.
# # Solution
def rotate_array(arr: list[int], k: int) -> list[int]:
    if not arr:
        return arr
    k %= len(arr)
    return arr[-k:] + arr[:-k]

# # 3️⃣ Check if parentheses/brackets are balanced
# # Question
# # Given a string with (), {}, [], determine if it's properly balanced.
# # Solution
def is_balanced(s: str) -> bool:
    pairs = {')': '(', ']': '[', '}': '{'}
    stack = []

    for c in s:
        if c in pairs.values():
            stack.append(c)
        elif c in pairs:
            if not stack or stack.pop() != pairs[c]:
                return False

    return len(stack) == 0

# # 4️⃣ Count distinct values
# # Question
# # Given a list of ints, return the number of unique values.
# # Solution
def count_distinct(nums: list[int]) -> int:
    return len(set(nums))

# # 5️⃣ Frog jump (classic Codility)
# # Question
# # Given integers X, Y, and D, find minimum jumps from X to reach Y or beyond.
# # Solution
# import math

def frog_jump(X: int, Y: int, D: int) -> int:
    return math.ceil((Y - X) / D)

# 🟦 Python Question 1 — Longest Even-Sum Subarray (Medium)
# Task
# You are given a list of integers.
# Return the length of the longest contiguous subarray whose sum is even.
# Example
# Input:  [5, 2, 4, 7, 6]
# Output: 4   # subarray [5,2,4,7] = 18 (even)
# ✅ Solution
def longest_even_sum_subarray(nums: list[int]) -> int:
    prefix_parity = {0: -1}  # parity -> earliest index
    current = 0
    longest = 0

    for i, n in enumerate(nums):
        current = (current + n) % 2  # 0 = even sum, 1 = odd

        if current in prefix_parity:
            longest = max(longest, i - prefix_parity[current])
        else:
            prefix_parity[current] = i

    return longest

# 🟦 Python Question 2 — Most Frequent Number (Easy)
# Task
# Return the number that appears most frequently.
# If tie → return the smallest such number.
# Example
# Input:  [4,4,2,2,3]
# Output: 2  # tie between 4 and 2, but 2 is smaller
# ✅ Solution
def most_frequent(nums: list[int]) -> int:
    freq = {}
    for x in nums:
        freq[x] = freq.get(x, 0) + 1

    max_count = max(freq.values())
    candidates = [k for k, v in freq.items() if v == max_count]

    return min(candidates)

# 🟦 Python Question 3 — Merge Overlapping Intervals (Medium)
# Task
# You receive a list of intervals [start, end].
# Merge overlapping ones and return the resulting list.
# Example
# Input:  [[1,4],[2,6],[7,9]]
# Output: [[1,6],[7,9]]
# ✅ Solution
def merge_intervals(intervals: list[list[int]]) -> list[list[int]]:
    if not intervals:
        return []

    intervals.sort()
    merged = [intervals[0]]

    for start, end in intervals[1:]:
        last = merged[-1]

        if start <= last[1]:  # overlap
            last[1] = max(last[1], end)
        else:
            merged.append([start, end])

    return merged

# 🟦 Python Question 4 — Count Islands in Matrix (Medium)
# Task
# You are given a 2D grid (0 = water, 1 = land).
# Return the number of connected islands (connected by up/down/left/right).
# Example
# Input:
# 1 1 0
# 0 1 0
# 1 0 1
# Output: 3
# ✅ Solution
def count_islands(grid: list[list[int]]) -> int:
    if not grid:
        return 0

    rows, cols = len(grid), len(grid[0])
    visited = set()

    def dfs(r, c):
        if (r, c) in visited or r < 0 or c < 0 or r >= rows or c >= cols or grid[r][c] == 0:
            return
        visited.add((r, c))
        dfs(r+1, c)
        dfs(r-1, c)
        dfs(r, c+1)
        dfs(r, c-1)

    count = 0
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == 1 and (r, c) not in visited:
                count += 1
                dfs(r, c)

    return count

# 🟦 Python Question 5 — Find the Missing Letter (Easy)
# Task
# You get a string containing consecutive letters, except one missing.
# Letters are all lowercase. Find the missing letter.
# Example
# Input:  "abcdf"
# Output: "e"
# ✅ Solution
def missing_letter(s: str) -> str:
    for i in range(len(s)-1):
        if ord(s[i+1]) != ord(s[i]) + 1:
            return chr(ord(s[i]) + 1)
    return "_"  # no missing letter