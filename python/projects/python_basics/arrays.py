# Arrays
# Note: This page shows you how to use LISTS as ARRAYS, however, to work with arrays in Python you will have to import a library, like the NumPy library.
#
# Arrays are used to store multiple values in one single variable:
#
# Example
# Create an array containing car names:

cars = ["Ford", "Volvo", "BMW"]

# What is an Array?
# An array is a special variable, which can hold more than one value at a time.
#
# If you have a list of items (a list of car names, for example), storing the cars in single variables could look like this:
#
# car1 = "Ford"
# car2 = "Volvo"
# car3 = "BMW"
# However, what if you want to loop through the cars and find a specific one? And what if you had not 3 cars, but 300?
#
# The solution is an array!
#
# An array can hold many values under a single name, and you can access the values by referring to an index number.
#
# Access the Elements of an Array
# You refer to an array element by referring to the index number.
#
# Example
# Get the value of the first array item:

x = cars[0]

# Example
# Modify the value of the first array item:

cars[0] = "Toyota"

# The Length of an Array
# Use the len() method to return the length of an array (the number of elements in an array).
#
# Example
# Return the number of elements in the cars array:

x = len(cars)

# Looping Array Elements
# You can use the for in loop to loop through all the elements of an array.
#
# Example
# Print each item in the cars array:

for x in cars:
  print(x)

# Adding Array Elements
# You can use the append() method to add an element to an array.
#
# Example
# Add one more element to the cars array:

cars.append("Honda")

# Removing Array Elements
# You can use the pop() method to remove an element from the array.
#
# Example
# Delete the second element of the cars array:

cars.pop(1)

# You can also use the remove() method to remove an element from the array.
#
# Example
# Delete the element that has the value "Volvo":

cars.remove("Volvo")