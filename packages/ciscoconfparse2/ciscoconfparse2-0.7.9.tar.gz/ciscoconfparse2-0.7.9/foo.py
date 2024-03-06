from ciscoconfparse2 import CiscoConfParse

config = """!
interface Ethernet 1/1
 ip address 172.16.1.1 255.255.255.0
 !no ip proxy-arp
!""".splitlines()

parse = CiscoConfParse(config, syntax="ios", factory=False)
print(parse.find_objects(r'.')[3].is_comment)

