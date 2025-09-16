thisdict = {
  "brand": "Ford",
  "model": "Mustang",
  "year": 1964
}
x = thisdict["model"]

# Get the value of the "model" key:

x = thisdict.get("model")

# Get a list of the keys:

x = thisdict.keys()

print (x)

# Add a new item to the original dictionary, and see that the keys list gets updated as well:

car = {
"brand": "Ford",
"model": "Mustang",
"year": 1964
}

y = car.keys()

print(y) #before the change

car["color"] = "white"

print(y) #after the change