# in python
import json

# Open the JSON file
with open("D:\\workfiles\\my_notes\\My_Notes\\junk\\source.json") as f:
    # Load the JSON data
    d = json.load(f)
    
    # Iterate through each dictionary and update the 'name' field
    for item in d:
        # First check the name to see if it's Alice
        if item['name'] == 'Alice':
            item['department'] = 'Finance'
        
        # Then convert the name to uppercase
        item['name'] = item['name'].upper()

    # Print the modified data
    print(d)
    
    # Print the number of names (i.e., the number of dictionaries in the list)
    print(f"Number of names: {len(d)}")

# Open the JSON file for writing (overwriting the existing content)
with open("D:\\workfiles\\my_notes\\My_Notes\\junk\\source.json", "w") as f:
    # Save the modified data back to the file
    json.dump(d, f, indent=4)