from netmiko import Netmiko
from getpass import getpass

my_device = { 
    'host' : "cisco1.twb-tech.com",
    'username' : user,
    'password' : getpass(),
    'device_type' : 'cisco_ios'
}

user = input("Enter your LDAP: ")
print(username)


net_conn = Netmiko(**my_device)

print(net_conn.find_prompt())