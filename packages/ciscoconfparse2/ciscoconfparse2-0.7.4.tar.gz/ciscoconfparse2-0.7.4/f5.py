from ciscoconfparse2 import CiscoConfParse
from ciscoconfparse2 import BraceParse

config = """foo
sys syslog {
    remote-servers {
        /Common/remotesyslog1 {
           host 10.0.0.45   }
    }
}
sys diags ihealth {
    expiration 30
    no-ihealth false
    options none
    password none
    user none
}"""

config = """foo1
foo2 {
    bar1 { this }
    bar2 { that }
}"""

config = """cm device /Common/client.domain.net {
    active-modules { "Local Traffic Manager, i2600|PXUPGKH-IKYHGFK|Rate Shaping|APM, Limited|Anti-Virus Checks|Base Endpoint Security Checks|Firewall Checks|Network Access|Secure Virtual Keyboard|APM, Web Application|Machine Certificate Checks|Protected Workspace|Remote Desktop|App Tunnel|Max SSL, i2600|Max Compression, i2600" }
    base-mac 00:94:a1:e7:94:00
    build 0.0.28
    cert /Common/dtdi.crt
    chassis-id "f5-itku-fdfl   "
    edition "Point Release 2"
    hostname my-host
    key /Common/dtdi.key
    management-ip 10.6.252.2
    marketing-name "BIG-IP i2600"
    optional-modules { "Access Policy Manager, Base, i26XX" "Access Policy Manager, Max, i26XX" "Advanced Firewall Manager, i2XXX" "Advanced Protocols" "Advanced Web Application Firewall, i2XXX" "Anti-Bot Mobile, i2XXX" "App Mode (TMSH Only, No Root/Bash)" "Application Security Manager, i2XXX" "ASM to AWF Upgrade, i2XXX" "BIG-IP, DNS (1K)" "BIG-IP, DNS and GTM Upgrade (1K TO MAX)" "BIG-IP, Multicast Routing" "BIG-IP, Privileged User Access, 100 Endpoints" "BIG-IP, Privileged User Access, 1000 Endpoints" "BIG-IP, Privileged User Access, 250 Endpoints" "BIG-IP, Privileged User Access, 50 Endpoints" "BIG-IP, Privileged User Access, 500 Endpoints" "Carrier Grade NAT, i2XXX" "DataSafe, i2XXX" "DNS Services" "External Interface and Network HSM" "Intrusion Prevention System, i2XXX" "IP Intelligence, 1Yr" "IP Intelligence, 1Yr, 1600" "IP Intelligence, 3Yr" "IP Intelligence, 3Yr, 1600" "IPS, 1Yr" "IPS, 3Yr" "Link Controller" "Performance Upgrade, i26XX to i28XX" "RAX Module Add-on, i2600" "Routing Bundle" SM2_SM3_SM4 "SSL Orchestrator, 2XXX/i2XXX" "SSL, Forward Proxy, 2XXX/i2XXX" "Threat Campaigns, 1Yr" "Threat Campaigns, 3Yr" "URL Filtering, 1Yr" "URL Filtering, 3Yr" "VPN Users" }
    platform-id C117
    product BIG-IP
    self-device true
    time-zone Europe/Paris
    version 16.1.2.2
}
cm device-group /Common/device_trust_group {
    auto-sync enabled
    devices {
        /Common/client.domain.net { }
    }
    hidden true
    network-failover disabled
}
cm device-group /Common/gtm {
    devices {
        /Common/client.domain.net { }
    }
    hidden true
    network-failover disabled
}"""



config = """
when CLIENT_ACCEPTED {
if { [IP::addr [IP::client_addr] equals 192.168.96.176%10/28] } {
log -noname local0. "[IP::client_addr] connected... Applying SNAT - Automap"
    snat automap
  } else {
    snat none
  }
}
}
"""

# Look at parse_line_braces() and convert to an object
#parse = CiscoConfParse('ltm.conf', syntax="junos", factory=False)
config = open('tests/fixtures/configs/sample_02.junos').read()

braces = BraceParse(config)
if False:
    for obj in braces.get_junoscfgline_list():
        print(obj)

    print(len(braces.get_junoscfgline_list()))

parse = CiscoConfParse('tests/fixtures/configs/sample_03.junos', syntax="junos",)
for obj in parse.find_object_branches([r'when',]):
    print(obj)
