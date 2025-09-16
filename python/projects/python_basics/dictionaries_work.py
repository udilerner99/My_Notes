thisdict = {
  "brand": "Ford",
  "model": "Mustang",
  "year": 1964
}
print(thisdict)

print (thisdict["brand"])

# Duplicate values will overwrite existing values:

thisdict = {
  "brand": "Ford",
  "model": "Mustang",
  "year": 1964,
  "year": 2020
}
print(thisdict)

# Get the value of the "model" key:

x = thisdict.get("model")
print (x)

# Get a list of the keys:

x = thisdict.keys()
print (x)

# Get a list of the values:

x = thisdict.values()
print (x)