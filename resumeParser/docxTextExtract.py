import sys
import docx
import docx2txt
import re

def getText(filename):
    text = docx2txt.process(filename)
    arr=[]
    arr=text.split('\n')
    LinkedInLink = "Linkedin.com"
    linkedinlink = "linkedin.com"

    linkedinAns = ""
    mobileNumber = ""
    for i in arr:
        #print(text)
        if i.find(LinkedInLink) >=0 or i.find(linkedinlink) >=0:
            linkedinAns = i

    match4 = re.search(r'''(\d{9}|\d{3}[-\.\s]??\d{3}[-\.\s]??\d{4}|\(\d{3}\)
                        [-\.\s]*\d{3}[-\.\s]??\d{4}|\d{3}[-\.\s]??\d{4}|[\+\(]?[1-9][0-9 .\-\(\)]{8,}[0-9])''', text)
    
    if match4 is not None:
        mobileNumber = match4.group(0)


    return linkedinAns, mobileNumber

# print(getText(sys.argv[1]))