# Change the "year" to 2018:

thisdict = {
  "brand": "Ford",
  "model": "Mustang",
  "year": 1964
}

y = thisdict.values()

print(y) #before the change

thisdict["year"] = 2018

y = thisdict.values()

print(y) #after the change


# Update the "year" of the car by using the update() method:

thisdict = {
  "brand": "Ford",
  "model": "Mustang",
  "year": 1964
}
thisdict.update({"year": 2020})
