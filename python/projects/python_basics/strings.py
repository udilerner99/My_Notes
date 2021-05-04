# Strings in python are surrounded by either single quotation marks, or double quotation marks.
# 'hello' is the same as "hello".
# You can display a string literal with the print() function:
print("Hello")
print('Hello')

# You can assign a multiline string to a variable by using three quotes:
a = """Lorem ipsum dolor sit amet,
consectetur adipiscing elit,
sed do eiusmod tempor incididunt
ut labore et dolore magna aliqua."""
print(a)

# Or three single quotes:
a = '''Lorem ipsum dolor sit amet,
consectetur adipiscing elit,
sed do eiusmod tempor incididunt
ut labore et dolore magna aliqua.'''
print(a)

# Strings are Arrays
# Like many other popular programming languages, strings in Python are arrays of bytes representing unicode characters.
# However, Python does not have a character data type, a single character is simply a string with a length of 1.
# Square brackets can be used to access elements of the string.
a = "Hello, World!"
print(a[1])

# Since strings are arrays, we can loop through the characters in a string, with a for loop.
for x in "banana":
    print(x)

# To get the length of a string, use the len() function.

