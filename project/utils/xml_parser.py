import xml.etree.ElementTree as ET

def parseXML(xmlfile):
  
    # create element tree object
    tree = ET.parse(xmlfile)
  
    # get root element
    root = tree.getroot()

    # create empty list for news items
    coords = []
    temp = []
  
    # iterate news items
    for _ in root:
        for item in _.findall('mxCell'):
            #print(item.tag, item.attrib)

            # get figures: pcs, sw, etc
            for figure in item.findall('mxGeometry'):
                x = figure.get('x')
                y = figure.get('y')
                w = figure.get('width')
                h = figure.get('height')
                if (x != None) and (y != None):
                    #print(x, y)
                    coords.append((x,y,w,h))

                # get connections aka paths
                for con in figure.findall('mxPoint'):
                    x = con.get('x')
                    y = con.get('y')
                    if (x != None) and (y != None):
                        temp.append((x, y))

        #for item in _:
        #    print(item.tag, item.attrib)
    #print(temp)
    paths = []
    k = 0
    for i in range(0, len(temp), 2):
        #print(i)
        paths.append((temp[i], temp[i+1]))
        k += 1

    print("Paths: " + str(paths))
    return coords, paths
