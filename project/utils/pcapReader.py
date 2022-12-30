from scapy.all import *
from os import listdir
from os.path import isfile, join

path = "captures/"
files = [f for f in listdir(path) if isfile(join(path, f))]


"""
scapy_cap = rdpcap('../captures/sw1_pc1.pcap')
print(type(scapy_cap))

for packet in scapy_cap:
    if packet.haslayer(IP):
        print (packet[IP].src)
        print (packet[IP].dst)
"""

def getIPs():

    #msgs = []
    dict = {}
    for f in files:
        key = f.replace(".pcap", "").split(" ")
        dict[key[1]] = list((p['IP'].src, p['IP'].dst, p.time, 0) for p in PcapReader(path + f) if 'IP' in p)
        #msgs += list((p['IP'].src, p['IP'].dst, p.time) for p in PcapReader(path + f) if 'IP' in p)
    
    for k in dict:
        for i in range(1, len(dict[k])):
            (src, dst, time, delay) = dict[k][i-1]
            dict[k][i-1] = (src, dst, time, dict[k][i][2] - dict[k][i-1][2])
    print(dict)
    return dict
    #print(merda)

    """
    for p in msgs:
        print("IP src: " + p[0] + " , IP dst: " + p[1])
    """
