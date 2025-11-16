# ✅ Python Question 3 — Monthly Active Users
# Problem:
# Given a list of events as tuples (user_id: int, event_date: str) in 'YYYY-MM-DD' format, return a dictionary mapping 'YYYY-MM' to number of distinct users in that month.
# Function Signature:
# def monthly_active_users(events: list[tuple[int, str]]) -> dict[str, int]:
#     pass
# Sample Input:
# events = [
#     (101, '2025-01-04'), (101, '2025-01-15'),
#     (102, '2025-01-22'), (101, '2025-02-01'),
#     (103, '2025-02-20'), (102, '2025-03-05')
# ]
# Expected Output:
# {'2025-01': 2, '2025-02': 2, '2025-03': 1}

def monthly_active_users(events: list[tuple[int, str]]) -> dict[str, int]:
    monthly_users = {}

    for user_id, date_str in events:
        month = date_str[:7]  # YYYY-MM

        if month not in monthly_users:
            monthly_users[month] = set()

        monthly_users[month].add(user_id)

    # convert sets to counts
    return {month: len(users) for month, users in monthly_users.items()}


events = [
    (101, '2025-01-04'), 
    (101, '2025-01-15'),
    (102, '2025-01-22'), 
    (101, '2025-02-01'),
    (103, '2025-02-20'), 
    (102, '2025-03-05')
]

print(monthly_active_users(events))
