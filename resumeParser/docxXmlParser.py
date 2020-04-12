import os                                                                                        
import zipfile                                                                                   
import re                                                                                        
import xml.dom.minidom
from bs4 import BeautifulSoup
import sys


def docxXmlParser(filename):
    document = zipfile.ZipFile(filename)
    ugl1 = xml.dom.minidom.parseString(document.read('word/styles.xml')).toprettyxml()
    # print(ugl1)
    # print(type(ugl1))

    y = BeautifulSoup(ugl1, 'xml')
    fonts = y.findAll('w:rFonts')
    sizes = y.findAll('w:sz')
    # print(len(fonts), len(sizes))
    sizes = y.findAll('w:rPr')
    # print(sizes)
    # print(sizes[0])
    fonts = []
    for i in sizes:
        # print(type(i))

        if i is not None:
            # vc = BeautifulSoup(i, 'xml')
            try:
                x = i.find('w:rFonts').attrs
                # x = i.fine('w:rFonts')
                x = x['w:ascii']
                # print(x)
                # print(x)
                # x = x.find('w:ascii')
                z = i.find('w:sz').attrs
                # print (x, z)
                z = z['w:val']
                fonts.append((x,z))
            except Exception as e:
                pass

    fonts = list(set(fonts))
    fontsString = ""
    for element in fonts:
        fontsString += str(element[0]) + "-" + str(element[1]) + "\n"
    # return fontsString
    # print(fontsString)

    tableCount = 0
    # print((tables[0].find('w:style')))
    # print(y.style.type)
    tables = y.findAll('w:style')
    for t in tables:
        if t is not None:
            try:
                tableTag = t.attrs['w:type']
                if tableTag == "table":
                    tableCount +=1
                # print(tableTag)
            except Exception as e:
                # print(e)
                pass
    

    ugl2 = xml.dom.minidom.parseString(document.read('word/document.xml')).toprettyxml() 
    soup2 = BeautifulSoup(ugl2, 'xml')
    images = soup2.findAll('w:drawing')
    imgCount = 0
    if images is not None:
        imgCount = len(images)

    return fontsString, tableCount, imgCount