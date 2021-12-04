# List
# Lists are used to store multiple items in a single variable.
#
# Lists are one of 4 built-in data types in Python used to store collections of data, the other 3 are Tuple, Set, and Dictionary, all with different qualities and usage.
#
# Lists are created using square brackets:
#
# Example
# Create a List:

thislist = ["apple", "banana", "cherry"]
print(thislist)

# List Items
# List items are ordered, changeable, and allow duplicate values.
#
# List items are indexed, the first item has index [0], the second item has index [1] etc.
#
# Ordered
# When we say that lists are ordered, it means that the items have a defined order, and that order will not change.
#
# If you add new items to a list, the new items will be placed at the end of the list.
# Changeable
# The list is changeable, meaning that we can change, add, and remove items in a list after it has been created.
#
# Allow Duplicates
# Since lists are indexed, lists can have items with the same value:
#
# Example
# Lists allow duplicate values:

thislist = ["apple", "banana", "cherry", "apple", "cherry"]
print(thislist)

# Access Items
# List items are indexed and you can access them by referring to the index number:
#
# Example
# Print the second item of the list:

thislist = ["apple", "banana", "cherry"]
print(thislist[1])

# Negative Indexing
# Negative indexing means start from the end
#
# -1 refers to the last item, -2 refers to the second last item etc.
#
# Example
# Print the last item of the list:

thislist = ["apple", "banana", "cherry"]
print(thislist[-1])

# Range of Indexes
# You can specify a range of indexes by specifying where to start and where to end the range.
#
# When specifying a range, the return value will be a new list with the specified items.
#
# Example
# Return the third, fourth, and fifth item:

thislist = ["apple", "banana", "cherry", "orange", "kiwi", "melon", "mango"]
print(thislist[2:5])

# By leaving out the start value, the range will start at the first item:
#
# Example
# This example returns the items from the beginning to, but NOT including, "kiwi" to the end:

thislist = ["apple", "banana", "cherry", "orange", "kiwi", "melon", "mango"]
print(thislist[:4])

# By leaving out the end value, the range will go on to the end of the list:
#
# Example
# This example returns the items from "cherry" to the end:

thislist = ["apple", "banana", "cherry", "orange", "kiwi", "melon", "mango"]
print(thislist[2:])

# Change Item Value
# To change the value of a specific item, refer to the index number:
#
# Example
# Change the second item:

thislist = ["apple", "banana", "cherry"]
thislist[1] = "blackcurrant"
print(thislist)

# Change a Range of Item Values
# To change the value of items within a specific range, define a list with the new values, and refer to the range of index numbers where you want to insert the new values:
#
# Example
# Change the values "banana" and "cherry" with the values "blackcurrant" and "watermelon":

thislist = ["apple", "banana", "cherry", "orange", "kiwi", "mango"]
thislist[1:3] = ["blackcurrant", "watermelon"]
print(thislist)

# If you insert more items than you replace, the new items will be inserted where you specified, and the remaining items will move accordingly:
#
# Example
# Change the second value by replacing it with two new values:

thislist = ["apple", "banana", "cherry"]
thislist[1:2] = ["blackcurrant", "watermelon"]
print(thislist)

# If you insert less items than you replace, the new items will be inserted where you specified, and the remaining items will move accordingly:
#
# Example
# Change the second and third value by replacing it with one value:

thislist = ["apple", "banana", "cherry"]
thislist[1:3] = ["watermelon"]
print(thislist)

# Insert Items
# To insert a new list item, without replacing any of the existing values, we can use the insert() method.
#
# The insert() method inserts an item at the specified index:
#
# Example
# Insert "watermelon" as the third item:

thislist = ["apple", "banana", "cherry"]
thislist.insert(2, "watermelon")
print(thislist)

# Append Items
# To add an item to the end of the list, use the append() method:
#
# Example
# Using the append() method to append an item:

thislist = ["apple", "banana", "cherry"]
thislist.append("orange")
print(thislist)

# Insert Items
# To insert a list item at a specified index, use the insert() method.
#
# The insert() method inserts an item at the specified index:
#
# Example
# Insert an item as the second position:

thislist = ["apple", "banana", "cherry"]
thislist.insert(1, "orange")
print(thislist)

# Extend List
# To append elements from another list to the current list, use the extend() method.
#
# Example
# Add the elements of tropical to thislist:

thislist = ["apple", "banana", "cherry"]
tropical = ["mango", "pineapple", "papaya"]
thislist.extend(tropical)
print(thislist)

# Remove Specified Item
# The remove() method removes the specified item.
#
# Example
# Remove "banana":

thislist = ["apple", "banana", "cherry"]
thislist.remove("banana")
print(thislist)

# Remove Specified Index
# The pop() method removes the specified index.
#
# Example
# Remove the second item:

thislist = ["apple", "banana", "cherry"]
thislist.pop(1)
print(thislist)

# If you do not specify the index, the pop() method removes the last item.

# Example
# Remove the last item:

thislist = ["apple", "banana", "cherry"]
thislist.pop()
print(thislist)

# The del keyword also removes the specified index:
#
# Example
# Remove the first item:

thislist = ["apple", "banana", "cherry"]
del thislist[0]
print(thislist)

# The del keyword can also delete the list completely.
#
# Example
# Delete the entire list:

thislist = ["apple", "banana", "cherry"]
del thislist

# Clear the List
# The clear() method empties the list.
#
# The list still remains, but it has no content.
#
# Example
# Clear the list content:
thislist = ["apple", "banana", "cherry"]
thislist.clear()
print(thislist)

# Loop Through a List
# You can loop through the list items by using a for loop:
#
# Example
# Print all items in the list, one by one:

thislist = ["apple", "banana", "cherry"]
for x in thislist:
  print(x)

# Example
# Print all items by referring to their index number:
count=0
thislist = ["apple", "banana", "cherry"]
for i in range(len(thislist)):
  count += 1
  print(count, thislist[i])

# Example
# Print all items, using a while loop to go through all the index numbers

thislist = ["apple", "banana", "cherry"]
i = 0
while i < len(thislist):
  print(thislist[i])
  i = i + 1