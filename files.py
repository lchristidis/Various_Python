f = open("text.txt")
print(f) ##<_io.TextIOWrapper name='text.txt' mode='r' encoding='cp1252'>

output = f.read() #read goes at the end of the file and stays there. In order to reread the file we should use seek()
f.close() #close reference to file
print(output)

input("press any key to continue \n")

print(output.split())

input("press any key to continue \n")

with open("text.txt") as file:   ####with this method close() occurs automatically
    output1 = file.read()

print(output1[0:5])

input("press any key to continue \n")

fullfill = open("new_file.txt", mode="w")  #beware it destroys the file

fullfill.write("some bullshit\n")
fullfill.write("some bullshit\n")
fullfill.write("some bullshit\n")
fullfill.write("some bullshit\n")

fullfill = open("new_file.txt", mode="a")  #This will append into file

fullfill.write("some bullshit1\n")
fullfill.write("some bullshit2\n")
fullfill.write("some bullshit3\n")
fullfill.write("some bullshit4\n")

