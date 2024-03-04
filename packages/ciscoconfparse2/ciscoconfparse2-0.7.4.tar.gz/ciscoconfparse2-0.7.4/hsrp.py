from ciscoconfparse2 import CiscoConfParse

parse = CiscoConfParse("tests/fixtures/configs/sample_08.ios", syntax="ios", factory=True)
intf = parse.find_objects("interface FastEthernet0/0")[0]
print(intf.get_hsrp_groups())
print(dir(intf.get_hsrp_groups()[1].get_hsrp_tracking_interfaces()[0]))
print(intf.get_hsrp_groups()[1].get_hsrp_tracking_interfaces()[0].interface_name)
