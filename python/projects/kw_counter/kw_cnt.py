# """
# This program will count key word in the given text from a file
# seperator is a white space
# """

f = open("demofile.txt", "r")
for x in f:
    print("current line is: {}".format(x))
    print("number of words in line is: ".format(x.split(" ")))
    print(len(x.split(" ")))
f.close()
