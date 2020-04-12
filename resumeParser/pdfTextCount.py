from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage
from pdfminer.converter import XMLConverter, HTMLConverter, TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfparser import PDFParser
import io
import os, sys

def textCount(filename):
    fp = open(filename, 'rb')
    rsrcmgr = PDFResourceManager()
    retstr = io.StringIO()
    # print(type(retstr))
    codec = 'utf-8'
    laparams = LAParams()
    device = TextConverter(rsrcmgr, retstr, codec=codec, laparams=laparams)
    interpreter = PDFPageInterpreter(rsrcmgr, device)

    page_no = 0
    textCount = []
    linesCount = []
    mixedCount = []
    for pageNumber, page in enumerate(PDFPage.get_pages(fp)):
        linesInPage = 0
        textInPage = 0
        interpreter.process_page(page)

        data = retstr.getvalue()
        lines = data.split("\n")
        for l in lines:
            if not l.isspace():
                linesInPage +=1
                textInPage += len(l)
        # linesCount.append(str(pageNumber) + "-" + str(linesInPage))
        # textCount.append(str(pageNumber) + "-" + str(textInPage))
        mixedCount.append(str(pageNumber) + "-" + str(linesInPage) + "," + str(textInPage))
    # textCount = ",".join(textCount)
    # linesCount = ",".join(linesCount)
    # print(textCount, linesCount)
    mixedCount = "\n".join(mixedCount)
    # print(mixedCount)
    return mixedCount