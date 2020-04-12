from bs4 import BeautifulSoup
import xml

def xmlParser(filename):
    xmldoc = xml.dom.minidom.parse(filename)
    itemlist = xmldoc.getElementsByTagName('text')

    fonts = []
    for i in range(len(itemlist)):
        c = itemlist[i].attributes.length
        if c >= 3: #check if font, size can be checked in attribute keys 
            fonts.append((itemlist[i].attributes['font'].value, itemlist[i].attributes['size'].value))

    fonts = list(set(fonts))
    # print(fonts)
    fontsString = ""
    for i in fonts:
        fontsString += i[0] + "-" + i[1] + "\n"
    
    ugl1 = xml.dom.minidom.parse(filename).toprettyxml()

    y = BeautifulSoup(ugl1, 'xml')
    images = y.findAll('image')
    numImages = 0
    if images is not None:
        numImages = len(images)

    return fontsString, numImages