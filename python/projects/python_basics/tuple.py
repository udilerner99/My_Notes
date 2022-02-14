thistuple = ("a", "b", "c")
print (thistuple)

print (len(thistuple))

oneItemTuple = ('a',)
print (type(oneItemTuple))

print (thistuple[1])

print (thistuple[-1])

print (thistuple[1:2])

x = ("a", "b", "c")
y = list(x)
y[1] = "z"
x = tuple(y)
print (x)

for i in thistuple:
    print (i)

for i in range(len(thistuple)):
    print (thistuple[i])

tuple1 = ('g', 'c', 's')
tuple2 = (1, 2, 3)

tuple3 = tuple1 + tuple2
print (tuple3)

tuple4 = tuple3*2
print (tuple4)