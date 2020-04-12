from io import StringIO
from pdfminer3.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer3.converter import TextConverter
from pdfminer3.layout import LAParams
from pdfminer3.pdfpage import PDFPage
import re
import sys

def get_text_info(cv_path):
    pagenums = set()
    output = StringIO()
    manager = PDFResourceManager()
    converter = TextConverter(manager, output, laparams=LAParams())
    interpreter = PDFPageInterpreter(manager, converter)
    infile = open(cv_path, 'rb')
    for page in PDFPage.get_pages(infile, pagenums):
        interpreter.process_page(page)
    infile.close()
    converter.close()
    text = output.getvalue()
    output.close()
    # print(text)
    # match = re.search(r'[\w\.-]+@[\w\.-]+', text)
    # if match is not None:
    #     email = match.group(0)
    #     return email

    lines = text.split("\n")
    # print(len(lines))
    LinkedInLink = "Linkedin.com"
    linkedinlink = "linkedin.com"

    linkedinAns = ""
    mobileNumber = ""
    for i in lines:
        # print(i).
        if i.find(LinkedInLink) >=0 or i.find(linkedinlink) >=0:
            linkedinAns = i

    match4 = re.search(r'''(\d{9}|\d{3}[-\.\s]??\d{3}[-\.\s]??\d{4}|\(\d{3}\)
                        [-\.\s]*\d{3}[-\.\s]??\d{4}|\d{3}[-\.\s]??\d{4}|[\+\(]?[1-9][0-9 .\-\(\)]{8,}[0-9])''', text)
    
    if match4 is not None:
        mobileNumber = match4.group(0)

    return linkedinAns, mobileNumber