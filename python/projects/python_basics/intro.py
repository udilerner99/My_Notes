print("Hello, World!")

# Python Indentation
# Python uses indentation to indicate a block of code.
if 5 > 2:
    print("Five is greater than two!")

# Python Variables
# Python has no command for declaring a variable.
x = 5
y = "Hello, World!"

# Comments
# Comments start with a #, and Python will render the rest of the line as a comment
# This is a comment.
print("Hello, World!")

# Variables
# Variables are containers for storing data values.
#
# Creating Variables
# Python has no command for declaring a variable.
#
# A variable is created the moment you first assign a value to it.

x = 5
y = "John"
print(x)
print(y)

# Variables do not need to be declared with any particular type, and can even change type after they have been set.
x = 4       # x is of type int
x = "Sally" # x is now of type str
print(x)

# Casting
# If you want to specify the data type of a variable, this can be done with casting.
x = str(3)    # x will be '3'
y = int(3)    # y will be 3
z = float(3)  # z will be 3.0

# Get the Type
# You can get the data type of a variable with the type() function.
x = 5
y = "John"
print(type(x))
print(type(y))

# Single or Double Quotes?
# String variables can be declared either by using single or double quotes:
x = "John"
# is the same as
x = 'John'

# Case-Sensitive
# Variable names are case-sensitive.
a = 4
A = "Sally"
# A will not overwrite a

# Variable Names
# A variable can have a short name (like x and y) or a more descriptive name (age, carname, total_volume). Rules for Python variables:
#     A variable name must start with a letter or the underscore character
# A variable name cannot start with a number
# A variable name can only contain alpha-numeric characters and underscores (A-z, 0-9, and _ )
# Variable names are case-sensitive (age, Age and AGE are three different variables)

myvar = "John"
my_var = "John"
_my_var = "John"
myVar = "John"
MYVAR = "John"
myvar2 = "John"

# Multi Words Variable Names
# Variable names with more than one word can be difficult to read.
#
# There are several techniques you can use to make them more readable:
#
# Camel Case
# Each word, except the first, starts with a capital letter:

myVariableName = "John"

# Pascal Case
# Each word starts with a capital letter:

MyVariableName = "John"

# Snake Case
# Each word is separated by an underscore character:

my_variable_name = "John"

# Many Values to Multiple Variables
# Python allows you to assign values to multiple variables in one line:

x, z, y = "Orange", "Banana", "Cherry"
print(x)
print(y)
print(z)

# One Value to Multiple Variables
# And you can assign the same value to multiple variables in one line:

x = y = z = "Orange"
print(x)
print(y)
print(z)

# Unpack a Collection
# If you have a collection of values in a list, tuple etc. Python allows you extract the values into variables.
# This is called unpacking.

fruits = ["apple", "banana", "cherry"]
x, z, y = fruits
print(x)
print(y)
print(z)

# Output Variables
# The Python print statement is often used to output variables.
#
# To combine both text and a variable, Python uses the + character:

x = "awesome"
print("Python is " + x)

x = "Python is "
y = "awesome"
z =  x + y
print(z)

# For numbers, the + character works as a mathematical operator:
x = 5
y = 10
print(x + y)

# If you try to combine a string and a number, Python will give you an error:

# Global Variables
# Variables that are created outside of a function (as in all of the examples above) are known as global variables.
#
# Global variables can be used by everyone, both inside of functions and outside.

x = "awesome"

def myfunc():
    print("Python is " + x)

myfunc()

x = "awesome"

def myfunc():
    x = "fantastic"
    print("Python is " + x)

myfunc()

print("Python is " + x)

# The global Keyword
# Normally, when you create a variable inside a function, that variable is local, and can only be used inside that function.
#
# To create a global variable inside a function, you can use the global keyword.

def myfunc():
    global x
    x = "fantastic!"

myfunc()

print("Python is " + x)

# Also, use the global keyword if you want to change a global variable inside a function.
x = "awesome"

def myfunc():
    global x
    x = "fantastic!!!"

myfunc()

print("Python is " + x)