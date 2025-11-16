# ✅ Python Question 5 — Employees With Multiple Managers
# Problem:
# Given a list of employee-manager assignments (emp_name: str, manager_name: str), 
# return a list of employees with more than one unique manager, sorted alphabetically.
# Function Signature:
# def employees_multiple_managers(assignments: list[tuple[str, str]]) -> list[str]:
#     pass

# Sample Input:
# assignments = [
#     ('Tom', 'Alice'), ('Tom', 'Bob'),
#     ('Jane', 'Alice'), ('Sam', 'Carol'), ('Sam', 'Dave')
# ]
# Expected Output:
# ['Sam', 'Tom']

def employees_with_multiple_managers(records: list[tuple[str, int]]) -> list[str]:
    emp_to_managers = {}

    for emp, mgr in records:
        if emp not in emp_to_managers:
            emp_to_managers[emp] = set()
        emp_to_managers[emp].add(mgr)

    result = [emp for emp, mgrs in emp_to_managers.items() if len(mgrs) > 1]

    return sorted(result)

assignments = [
    ('Tom', 'Alice'), ('Tom', 'Bob'),
    ('Jane', 'Alice'), ('Sam', 'Carol'), ('Sam', 'Dave')
]

print(employees_with_multiple_managers(assignments))