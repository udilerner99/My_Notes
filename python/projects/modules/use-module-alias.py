# Naming a Module
# You can name the module file whatever you like, but it must have the file extension .py
#
# Re-naming a Module
# You can create an alias when you import a module, by using the as keyword:
#
# Example
# Create an alias for mymodule called mx:

import mymodule as mx

a = mx.person1["age"]
print(a)

# Built-in Modules
# There are several built-in modules in Python, which you can import whenever you like.
#
# Example
# Import and use the platform module:

import platform

x = platform.system()
print(x)

# Using the dir() Function
# There is a built-in function to list all the function names (or variable names) in a module. The dir() function:
#
# Example
# List all the defined names belonging to the platform module:

import platform

x = dir(platform)
print(x)