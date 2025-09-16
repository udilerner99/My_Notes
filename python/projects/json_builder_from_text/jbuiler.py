# """
# This program will create a json dump from reading a text file
# each line will transform into a sub dictionary ,
# and will count the number of words in the line
# """

f = open("demofile.txt", "r")
for x in f:
    print("current line is: {}".format(x))
    print("number of words in line is: ".format(x.split(" ")))
    print(len(x.split(" ")))

f.close()
