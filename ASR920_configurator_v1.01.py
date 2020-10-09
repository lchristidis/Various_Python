#!/usr/bin/env python
import xlrd


##################INITIALIZATION############################
print("#########################################################\n")
print("#####  ASR920 Provisioning Script by lchristidis    #####\n")
print("#### Always check generated config before commiting  ####\n")
print("#########################################################\n")
print("Initializing....Opening file.....please wait....\n")
mtu=9100 #Since vpls have different mtu's, this script will use one value for mtu ==9100
xlfile="NE_DSLAM_InventoryOneNET.xlsx"
element = "" # #checking rows column AZ thats why (row,51)
inter="Gi0/0/0"
exp=3
WCRM_checker = 0
row_beg=0
row = 5
VLAN = 0 #1XX (row,20) 4XX (row,30) 6XX (row, 32)
VLAN_v=0 #(row,31)
BDOMAIN = 0
NEI1=162
NEI2=159
dslam_name = ""
ip_addr = ""
voice_ip = 1     #Necessary value to generate first voice ip address as primary
sig_ip = ""      #necessary check value for L3 Voice configuration
workbook=xlrd.open_workbook(xlfile) #open workbook
sheet = workbook.sheet_by_index(0) #getting sheets names, info is the first excell sheet
print("Please provide information necessary to complete configuration\n")
print("Please provide name of file you want to export config eg ath-0317-mesw10.txt\n")
filename = input()
file = open(filename, 'w')
#############################################################

def vpls_print(): #l2 vfi print function
    file.write("\n!")
    file.write("\nl2 vfi "+str(vpls_name)+" manual")
    file.write("\nvpn id "+str(vpls_id))
    file.write("\nbridge-domain "+str(BDOMAIN))
    file.write("\nmtu "+str(mtu))
    file.write("\nneighbor 62.38.1."+str(NEI1)+" encapsulation mpls")
    file.write("\nneighbor 62.38.1."+str(NEI2)+" encapsulation mpls")
    file.write("\n!")
def svc_print_data():  #Service instance print function
    file.write("\nservice instance "+str(VLAN)+" ethernet")
    file.write("\ndescription DATA_LLI_"+str(dslam_name))
    file.write("\nencapsulation dot1q "+str(VLAN))
    file.write("\ncheck if necessary -> rewrite ingress tag translate 1-to-1 dot1q "+str(VLAN)+" symmetric")
    file.write("\nbridge-domain "+str(BDOMAIN)+" split-horizon group 1")
    file.write("\n!")
def svc_print_onenet():  #Service instance print function
    file.write("\nservice instance "+str(VLAN)+" ethernet")
    file.write("\ndescription ONENET_"+str(dslam_name))
    file.write("\nencapsulation dot1q "+str(VLAN))
    file.write("\nbridge-domain "+str(BDOMAIN)+" split-horizon group 1")
    file.write("\n!")
def svc_print_voice():  #Service instance print function
    file.write("\nservice instance "+str(VLAN_v)+" ethernet")
    file.write("\ndescription MSAN_VOICE_"+str(dslam_name))
    file.write("\nencapsulation dot1q "+str(VLAN_v))
    file.write("\nrewrite ingress tag pop 1 symmetric")
    file.write("\nbridge-domain "+str(BDOMAIN)+" split-horizon group 1")
    file.write("\n!")
def common_svc():
    file.write("\n!")
    file.write("\nservice instance "+str(VLAN)+" ethernet")
    file.write("\ndescription "+str(dslam_name))
    file.write("\nencapsulation dot1q "+str(VLAN))
    if exp == 4 or exp == 5 :
        file.write("\nservice-policy input set-exp-"+str(exp))
    file.write("\nrewrite ingress tag pop 1 symmetric")
    file.write("\nbridge-domain "+str(BDOMAIN)+" split-horizon group 1")
    file.write("\n!")



#########USER GUIDE####################


#######################################

##########USER INPUT###################

print("Site number (eg Chalandri = 317) :")
wcrm=int(input())
for row in range(sheet.nrows) :   #checking rows column G thats why (row,6)
    WCRM_checker = sheet.cell_value(row,6)
    if WCRM_checker==wcrm :
        print("\n\nSite number FOUND...")
        print("\nGENERATING CONFIG CAN COMMENCE...")
        break
    if WCRM_checker!=wcrm and row==sheet.nrows-1 :
        print("\n\nSite was not found....")
        print("\nProgram will exit...")
        print("\nPress enter to exit")
        input()
        quit()
print("\nPlease provide data VLAN aggregation routers")
print("Select 1 for adr-bar0X / 2 for med-bar0x / 3 for adr/med-ar90")
neighbor=int(input())
if neighbor !=1 and neighbor !=2 and neighbor !=3 :
    print("\nYou have inserted wrong aggregator value")
    print("Press enter to exit")
    input()
    quit()
print("Insert number X of interfaces on 920 Gi0/0/0-Gi0/0/X")
num_int=int(input())

print("\nStarting generating ASR920 CONFIG")

file.write("\nConfiguration for DSLAM interfaces\n")

file.write("\nint range gi0/0/0-"+str(num_int))
file.write("\nmtu 9100")
file.write("\nip arp inspection limit rate 768")
file.write("\nno ip address")
file.write("\nload-interval 30")
file.write("\nnegotiation auto")
file.write("\nservice-policy output PE-UPE-OUT-QG\n\n")



print("########Printing service instances per DSLAM interface########\n")
for row in range(sheet.nrows) :   #checking rows column G thats why (row,6)
    WCRM_checker = sheet.cell_value(row,6)

    if WCRM_checker==wcrm:
        VLAN = sheet.cell_value(row,20)
        row_beg=row         #file.write("\nrow number is :"+str(row_beg)) -> verified
        if VLAN !='-':      # by the excel file that means DATA_VLAN
            element=sheet.cell_value(row_beg,51)
            inter=sheet.cell_value(row_beg,52)
            dslam_name=sheet.cell_value(row_beg,0)
            BDOMAIN = 2601
            VLAN=round(VLAN)
            file.write("\n@"+str(element))
            file.write("\n\ninterface "+inter)
            svc_print_data()        #print VLAN 1XX
            VLAN = sheet.cell_value(row,30)
            VLAN=round(VLAN)
            svc_print_data()        #print VLAN 4XX
            VLAN = sheet.cell_value(row,32)
            VLAN=round(VLAN)
            svc_print_data()        #print VLAN 6XX
            VLAN = sheet.cell_value(row,21)
            if VLAN !='-':
                VLAN=round(VLAN)
                BDOMAIN=2630                        #print ONENET VLANS
                svc_print_onenet()
                VLAN = sheet.cell_value(row,22)
            if VLAN !='-':
                VLAN=round(VLAN)
                BDOMAIN=2660                        #print ONENET VLANS
                svc_print_onenet()  
        elif VLAN =='-': # Voice VLAN
            element=sheet.cell_value(row_beg,51)
            dslam_name=sheet.cell_value(row_beg,0)
            inter=sheet.cell_value(row_beg,52)
            inter=sheet.cell_value(row_beg,52)
            BDOMAIN = 599
            VLAN_v=sheet.cell_value(row,31)
            if VLAN_v != '-': # checking idz
                file.write("\n@"+str(element)+"  -> check if voice are on 3400 and add them on proper ASR920 port\n")
                file.write("\ninterface "+inter)
                VLAN_v=round(VLAN_v)
                svc_print_voice() # printing service instances
            


print("######  Printing common service istances for all DSLAMS  ######") 
file.write("\n######  Printing common service istances for all DSLAMS  ######") 
file.write("\n######  Add only service instance 5 for MSAN VOiCE  ###########") 
file.write("\n######  Add 27XX, 5, 90, 91, Video for data DSLAMS  ###########")
file.write("\n######  Add only svc 6 for Zhone DSLAMS IF present  ###########")  
#dslam management

VLAN=5
BDOMAIN=5
dslam_name="DSLAM_MGMT"
common_svc()

#zhone dslam management
VLAN=6
BDOMAIN=6
dslam_name="ZHONE_DSLAM_MGMT"
common_svc()
#90 VLAN CPE management management
VLAN=90
BDOMAIN=90
dslam_name="90_Cpe_mgmt_IBAS"
common_svc()

#91 VLAN CPE management
VLAN=91
BDOMAIN=91
dslam_name="91_CpeMgmt_Zhone"
common_svc()

#Video svc (row,29) service-policy input set-exp-4 ?
for row in range(sheet.nrows) : 
    WCRM_checker = sheet.cell_value(row,6)
    if WCRM_checker==wcrm:
        VLAN = sheet.cell_value(row,29)
        break
dslam_name = str(wcrm)+"_VIDEO"
VLAN=round(VLAN)
BDOMAIN=VLAN
exp=4
common_svc()
exp=3
#Voip HOL 2700 (row,23) service-policy input set-exp-5 ?
for row in range(sheet.nrows) : 
    WCRM_checker = sheet.cell_value(row,6)
    if WCRM_checker==wcrm:
        VLAN = sheet.cell_value(row,23)
        break
dslam_name = "Voip_HOL_2700"
VLAN=round(VLAN)
BDOMAIN=sheet.cell_value(row,24)
BDOMAIN=round(BDOMAIN)
BDOMAIN_HOL=BDOMAIN
exp=5
common_svc()
exp=3
#Voip CPE 2720 (row,25)

for row in range(sheet.nrows) : 
    WCRM_checker = sheet.cell_value(row,6)
    if WCRM_checker==wcrm:
        VLAN = sheet.cell_value(row,25)
        break
dslam_name = "Voip_VOD_CPE_2720"
VLAN=round(VLAN)
BDOMAIN=sheet.cell_value(row,26)
BDOMAIN=round(BDOMAIN)
BDOMAIN_CPE=BDOMAIN
exp=5
common_svc()

#VOIP PBX 2740 (row,27)
for row in range(sheet.nrows) : 
    WCRM_checker = sheet.cell_value(row,6)
    if WCRM_checker==wcrm:
        VLAN = sheet.cell_value(row,27)
        break
dslam_name = "Voip_VOD_PBX_2740"
VLAN=round(VLAN)
BDOMAIN=sheet.cell_value(row,28)
BDOMAIN=round(BDOMAIN)
BDOMAIN_PBX=BDOMAIN
exp=5
common_svc()




#print vpls for DATA 9XXXXX
if wcrm >= 1 and wcrm <= 999:
    vpls_id=str(90)+str(wcrm)
if wcrm >= 1000 and wcrm <= 9999:
    vpls_id=str(9)+str(wcrm)
if neighbor == 1 :
    NEI1=82
    NEI2=83
if neighbor == 2 :
    NEI1=84
    NEI2=85
if neighbor == 3 :
    NEI1=159
    NEI2=162
vpls_name=str(wcrm)+"_DATA_VFI"
BDOMAIN=2601
vpls_print()

#print vpls for ONENET_DATA 4XXXX
if wcrm >= 1 and wcrm <= 999:
    vpls_id=str(40)+str(wcrm)
if wcrm >= 1000 and wcrm <= 9999:
    vpls_id=str(4)+str(wcrm)
vpls_name=str(wcrm)+"_ONENET_DATA"
NEI1=82
NEI2=85
BDOMAIN=2660
vpls_print()
#print vpls for ONENET_VOICE 2XXXX
if wcrm >= 1 and wcrm <= 999:
    vpls_id=str(20)+str(wcrm)
if wcrm >= 1000 and wcrm <= 9999:
    vpls_id=str(2)+str(wcrm)
vpls_name=str(wcrm)+"_ONENET_VOICE"
BDOMAIN=2630
vpls_print()

#####COMMON VPLS BELOW###############
#print vpls for Dslam mgmt 5
vpls_name="5_DSLAM_MGMT"
NEI1=162
NEI2=162
BDOMAIN=5
vpls_id=5
vpls_print()
#print vpls for Zhone Mgmt 6
vpls_name="6_Zhone_MGMT"
NEI1=162
NEI2=162
BDOMAIN=6
vpls_id=6
vpls_print()
#print vpls for 91_Cpe_Mgmt 91
vpls_name="91_CpeMgmt_Zhone"
NEI1=162
NEI2=159
BDOMAIN=91
vpls_id=10112
vpls_print()
#print vpls for 90_cpe_Mgmt 90
vpls_name="90_CpeMgmt_Ibas"
NEI1=162
NEI2=159
BDOMAIN=90
vpls_id=10113
vpls_print()
#print vpls for 30000_VOICE_MSAN_ALU 603000X
vpls_name="30000_VOICE_MSAN_ALU"
NEI1=162
NEI2=162
BDOMAIN=3750
vpls_id="6030000_check"
vpls_print()
#print vpls for voip 370X_HOL_CPE 378X_VF_CPE 379X_VF_PBX 

vpls_name=str(BDOMAIN_HOL)+"_HOL_CPE"
NEI1=162
NEI2=159
BDOMAIN=BDOMAIN_HOL
vpls_id="71000_check"

vpls_print()

vpls_name=str(BDOMAIN_CPE)+"_VF_CPE"
NEI1=162
NEI2=159
BDOMAIN=BDOMAIN_CPE
vpls_id="72000_check"
vpls_print()

vpls_name=str(BDOMAIN_PBX)+"_VF_PBX"
NEI1=162
NEI2=159
BDOMAIN=BDOMAIN_PBX
vpls_id="73000_check"
vpls_print()

file.write("\n\nL3 Interfaces\n")
file.write("\nNOTE!!! For Voice L3 please check secondary ip addresses!!!\n")
file.write("\ninterface BDI599")
file.write("\nshutdown")
file.write("\ndescription "+str(wcrm)+"_VOICE_MSAN")
file.write("\nip vrf forwarding VoiceMSAN")
for row in range(sheet.nrows) :   #checking rows column G thats why (row,6)
    WCRM_checker = sheet.cell_value(row,6)
    if WCRM_checker==wcrm:
        row_beg=row
        VLAN_v = sheet.cell_value(row,31)
        ip_addr=sheet.cell_value(row_beg,42)
        sig_ip=sheet.cell_value(row_beg,38)
        #file.write("\nrow number is :"+str(row_beg)) -> verified
        if VLAN_v !='-' and voice_ip == 0 and sig_ip != "-" : # Voice VLAN
            file.write("\nip address "+str(ip_addr)+" 255.255.255.248 secondary")
        if VLAN_v !='-' and voice_ip == 1 and sig_ip != "-" : # Voice VLAN
            ip_addr=sheet.cell_value(row_beg,42)
            file.write("\nip address "+str(ip_addr)+" 255.255.255.248")
            voice_ip = 0 
file.write("\narp timeout 290\n") 


for row in range(sheet.nrows) : 
    WCRM_checker = sheet.cell_value(row,6)
    if WCRM_checker==wcrm:
        row_beg=row 
        VLAN = sheet.cell_value(row,29)
        break
VLAN=round(VLAN)
ip_addr=sheet.cell_value(row_beg,49)
file.write("\ninterface BDI"+str(VLAN))
file.write("\nshutdown")
file.write("\ndescription "+str(wcrm)+"_VIDEO")
file.write("\nip address "+str(ip_addr)+" 255.255.224.0 #check correct mask")
file.write("\nip helper-address 172.31.255.10")
file.write("\nno ip proxy-arp")
file.write("\nip pim sparse-mode")
file.write("\nip access-group Video in")
file.write("\narp timeout 290")
file.write("\n\n")
file.write("\nrouter ospf 3329")
file.write("\nnetwork "+str(ip_addr)+" 0.0.15.255 area 0")
file.write("\npassive-interface BDI"+str(VLAN))
file.write("\n\n")
file.write("\nPlease note!!!!!!!!!!!\n")
file.write("\nCheck neighborships, vpn id's since they are not documented, and different per AK")
file.write("\nVoip HOL_VOD-CPE_VOD-PBX YOU must check vpls id and neighbors for sure")
print("ASR920 configuration complete")
print("Press any key to exit")
file.close() 

input()