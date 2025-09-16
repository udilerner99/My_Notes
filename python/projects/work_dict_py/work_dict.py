#in python
# import json

my_dict = [
    {"id":123,
     "first_name":"Danny",
     "last_name":"choen",
     "sales": 100},
    {"id":456,
     "first_name":"Rick",
     "last_name":"rude",
     "sales": 400},
    {"id":123,
     "first_name":"Jhonny",
     "last_name":"be-good",
     "sales": 800}
]

sales = 0

for item in my_dict:
    # print for check
    # print(item)

    # change into uppercase
    item['last_name']=item['last_name'].title()

    # total sales
    sales = sales + item['sales']

    # print for check
    print(item)

# average sales
avg_sales = sales / len(my_dict)
print (f"average sales is: {avg_sales}")

# Add new column 'above_avg' based on sales comparison with average
for item in my_dict:
    if item['sales'] > avg_sales:
        item['above_avg'] = 'Y'
    else:
        item['above_avg'] = 'N'

    # Print the updated item
    print(item)
