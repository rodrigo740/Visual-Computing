import xml.etree.ElementTree as ET

def parseXML(xmlfile):
  
    # create element tree object
    tree = ET.parse(xmlfile)
  
    # get root element
    root = tree.getroot()

    # create empty list for news items
    coords = []
  
    # iterate news items
    for _ in root:
        for item in _.findall('mxCell'):
            #print(item.tag, item.attrib)
            for figure in item.findall('mxGeometry'):
                x = figure.get('x')
                y = figure.get('y')
                w = figure.get('width')
                h = figure.get('height')
                if (x != None) and (y != None):
                    #print(x, y)
                    coords.append((x,y,w,h))
        #for item in _:
        #    print(item.tag, item.attrib)
    return coords
