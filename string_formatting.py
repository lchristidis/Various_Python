
ip_addr1 = '172.16.0.1'
ip_addr2 = '172.31.16.243'
ip_addr3 = '10.1.24.5'

print("\n")
print("-" * 80)
print(ip_addr1, ip_addr2, ip_addr3)
print("{ip1:^20}{ip2:^20}{ip3:^20}".format(ip1=ip_addr1,ip3=ip_addr2,ip2=ip_addr3)) #positional formatting arguments
print("-" * 80)
print("\n")


ip_addr = "192.168.1.1"
octets = ip_addr.split(".")
print("\n")
print("-" * 40)
print("{:10}{:10}{:10}{:10}".format(octets[0],octets[1],octets[2],octets[3])) 
print("-" * 40)
print("\n")

print("-" * 40)
print("\n")
print("{:10}{:10}{:10}{:10}".format(*octets)) #this is better than line 18

print("-" * 40)
print("-" * 40)
print("-" * 40)
print("-" * 40)

ip_addrZ = "192.168.2.1"
ip_addrX = "192.168.3.1"
portZ = 80
portX = 8080

print("%s %s" % (ip_addrZ, ip_addrX)) #old way but someone could use this format

print("-" * 40)
print("-" * 40)
print("-" * 40)
print("-" * 40)

print(f"My Ip address is: {ip_addrZ}") #output is 'My Ip address is: 192.168.2.1'
print(f"My Ip address is: {ip_addrX:^20}") #output is 'My Ip address is:     192.168.3.1     '

print(f"My Ip address is: {ip_addrZ} {portZ:^8}") #output is 'My Ip address is: 192.168.2.1'
print(f"My Ip address is: {ip_addrX:>20}:{portX:<8}") #output is 'My Ip address is:     192.168.3.1:8080'


#JOIN 
kick = ip_addrZ.split(".") #takes string, splits int list for every "."
print(kick)             #Verify output
print(".".join(kick))       #print list as an ip address



input()