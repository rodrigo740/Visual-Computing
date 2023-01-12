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
            if 'value' in item.attrib:
                val = item.attrib['value']
                
                # get figures: pcs, sw, etc
                for figure in item.findall('mxGeometry'):
                    x = figure.get('x')
                    y = figure.get('y')
                    w = figure.get('width')
                    h = figure.get('height')
                    ip = val

                    if (x != None) and (y != None):
                        coords.append((x,y,w,h,ip))

                    # get connections aka paths
                    for con in figure.findall('mxPoint'):
                        temp.append(val)
                        x = con.get('x')
                        y = con.get('y')
                        if (x != None) and (y != None):
                            temp.append((x, y))
            
    paths = []
    k = 0
    for i in range(0, len(temp), 4):
        paths.append((temp[i], temp[i+1], temp[i+3]))
        k += 1

    return coords, paths
