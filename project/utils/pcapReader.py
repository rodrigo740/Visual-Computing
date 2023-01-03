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

    msgs = []
    dict = {}
    i = 0
    for f in files:
        key = f.replace(".pcap", "").split(" ")
        dict[key[1]] = []
        #dict[key[1]] = list((p['IP'].src, p['IP'].dst, p.time, 0) for p in PcapReader(path + f) if 'IP' in p)
        msgs += list((p['IP'].src, p['IP'].dst, p.time, 0, key[1], p["IP"].id) for p in PcapReader(path + f) if 'IP' in p)
        
    sorted_list = sorted(
        msgs, 
        key= lambda t: t[2]
    )
    #print(msgs)
    #print("\n Sorted:\n")
    #print(sorted_list)

    f = sorted_list[0][2]
    (src, dst, time, delay, id, pid) = sorted_list[0]
    sorted_list[0] = (src, dst, 0, delay, id, pid)
    
    for i in range(1, len(sorted_list)):
        diff = sorted_list[i][2] - f
        (src, dst, time, delay, id, pid) = sorted_list[i]
        sorted_list[i] = (src, dst, diff, delay, id, pid)
        dict[id].append(sorted_list[i])

    fList = []

    lids = []

    for i in range(len(sorted_list)):
        pid = sorted_list[i][5]
        if pid not in lids:
            lids.append(pid)
            temp = [sorted_list[i]]
            for k in range(i+1, len(sorted_list)):
                aux = sorted_list[k][5]
                if pid == aux:
                    temp.append(sorted_list[k])
            if len(temp) != 1:
                for j in range(len(temp)):
                    (src, dst, time, delay, id, pid) = temp[j]
                    time += (j*1.5)
                    fList.append((src, dst, time, delay, id, pid))
            else:
                fList.append(temp[0])
    
    #print("\n FList:\n")

    fList = sorted(
        fList, 
        key= lambda t: t[2]
    )
        
    #for _ in fList:
    #    print(_)

    """
    for k in dict:
        for i in range(1, len(dict[k])):
            (src, dst, time, delay) = dict[k][i-1]
            diff = dict[k][i][2] - dict[k][i-1][2]
            dict[k][i-1] = (src, dst, time, diff)
    """

    #print("DICT")
    #print(dict)
    return dict, fList
    

    """
    for p in msgs:
        print("IP src: " + p[0] + " , IP dst: " + p[1])
    """
