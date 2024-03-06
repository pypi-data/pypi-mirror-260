from ciscoconfparse2 import CiscoConfParse, Diff

config1 = """router bgp 777
 neighbor 192.0.2.1 remote-as 778
 address-family ipv4 unicast
  neighbor 192.0.2.1 activate
  network 10.0.0.0
"""

config2 = """router bgp 777
 neighbor 192.0.2.5 remote-as 778
 address-family ipv4 unicast
  neighbor 192.0.2.5 activate
  network 10.0.0.0
"""

diff = Diff(config1, config2)
for line in diff.get_diff():
    print(line)

parse = CiscoConfParse(config1.splitlines())
obj = parse.find_objects("router bgp")[0]
for this in obj.re_list_iter_typed("(neighbor\s.+)"):
    print(this)

