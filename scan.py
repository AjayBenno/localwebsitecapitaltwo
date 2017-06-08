from wifi import Cell,Scheme
from scapy.all import *


val = Cell.all('wlan0');

vals = map(lambda x: x.ssid,val)

print vals
print len(val)

# ap_list = []

# for v in val:
    # if v.ssid not in ap_list:
        # ap_list.append(v.ssid)
        # print v.ssid," ",v.address
        # print "\n"
