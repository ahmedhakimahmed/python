A = """!
hostname my-example-switch
!
!
vlan 200
 name Segment_A
!
vlan 200
 name Segment_B
!
interface Loopback0
 description Management IP address
 ip address 1.1.1.1 255.255.255.255
!
interface Vlan1
 no ip address
!
interface Vlan200
 ip address 10.1.1.1 255.255.255.0
 ip helper-address 10.254.0.100
 no ip redirects
 no ip unreachables
 no ip proxy-arp
!
interface Vlan300
 description vlan 300 interface (no ospf neighbors)
 ip address 10.2.2.1 255.255.255.0
 no ip redirects
 no ip unreachables
 no ip proxy-arp
!
interface FastEthernet1/1
 no switchport
 description routed port Fa1/1
 ip address 10.3.3.1 255.255.255.0
!
router ospf 1
 router-id 1.1.1.1
 log-adjacency-changes detail
 auto-cost reference-bandwidth 100000
 passive-interface Vlan300
 network 10.1.1.1 0.0.0.0 area 0
 network 10.2.2.1 0.0.0.0 area 0
 default-information originate
!
!"""

# Put result in dictionnary
result = {
    "features" : [],
    "interfaces" :{}
}

import re
import sys
import json

#Check if the opsf configured
ospf_config = r"^router ospf \d+$"
is_ospf_configured = True if re.search(ospf_config, A, re.MULTILINE) else False

#is_ospf_configured = True if re.search(r"^router ospf \d+$", A, re.MULTILINE) else False

if is_ospf_configured:
    print ("== OSPF is being configured here")
    result["features"].append("ospf")
else:
    print ("=! OSPF is not used here")

# Check if the ISIS configured
isis_config = r"^router isis \d+$"
is_isis_configured = Ture if re.search(isis_config, A, re.MULTILINE) else False

if is_isis_configured:
    print ("== ISIS configured here")
else:
    print ("=! ISIS NOT configured here")

print "_._"*50
print ("\n")

# extract the interface name and description
interface_descriptions = re.finditer(r"^(interface (?P<intf_name>\S+))\n"
                                         r"( .*\n)*"
                                         r"( description (?P<description>.*))\n",
                                         A,
                                         re.MULTILINE)

for intf_part in interface_descriptions:
        print("==> found interface '%s' with description '%s'" % (intf_part.group("intf_name"),
                                                                  intf_part.group("description")))
        result["interfaces"][intf_part.group("intf_name")] = {
            "description": intf_part.group("description") if intf_part.group("description") else "not set"
        }

print "_+"*75
print ("\n")

# extract the IPv4 address of the interfaces
interface_ips = re.finditer(r"^(interface (?P<intf_name>.*)\n)"
                                r"( .*\n)*"
                                r"( ip address (?P<ipv4_address>\S+) (?P<subnet_mask>\S+))\n",
                                A,
                                re.MULTILINE)

for intf_ip in interface_ips:
        print("==> found interface '%s' with ip '%s/%s'" % (intf_ip.group("intf_name"),
                                                           intf_ip.group("ipv4_address"),
                                                           intf_ip.group("subnet_mask")))


print("\nEXTRACTED PARAMETERS\n")

