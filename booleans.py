


my_val = 1

a = 'whatever' if my_val > 2 else 'something'   #ternary operator

print(a)


##for loops

ip_list = ['192.168.1.1', '10.1.1.1', '10.10.20.30', '172.16.31.254']


for ip in ip_list:
    print(ip)


#What if we want to keep track of the list position 0, 1, 2, 3 etc

for my_var in enumerate(ip_list): 
    print(my_var)    #output is a tuple!!! (0, '192.168.1.1') nice way to fill in db or smth

var1, var2 = my_var     
print(var1)
print(var2)    

for i, ip_addr in enumerate(ip_list):  #so what happens here, it assigns i the number of the position in list 
    print(ip_addr)              #and assigns ip_addr the data from ip_list[i]
    print('-' * 30)


#BREAK and Continue

for ip in ip_list:
    print("breaking? no " + ip)
    if ip == '10.10.20.30':
        print("breaking? Yes since I detected 10.10.20.30")
        break

for ip in ip_list:
    print("Hello ")
    if ip == '10.10.20.30':
        continue            #SO for loop stops here and continues increasing ip+1 in order to end the for loop
    print(ip)

for ip in ip_list:
    pass       #nice way to place a place holder to continue in this for loop


