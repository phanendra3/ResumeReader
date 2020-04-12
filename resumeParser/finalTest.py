from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage
from pdfminer.converter import XMLConverter, HTMLConverter, TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfparser import PDFParser
import io
import os, sys

fp = open(sys.argv[1], 'rb')
rsrcmgr = PDFResourceManager()
retstr = io.StringIO()
print(type(retstr))
codec = 'utf-8'
laparams = LAParams()
device = TextConverter(rsrcmgr, retstr, codec=codec, laparams=laparams)
interpreter = PDFPageInterpreter(rsrcmgr, device)

page_no = 0
for pageNumber, page in enumerate(PDFPage.get_pages(fp)):
    if pageNumber == page_no:
        interpreter.process_page(page)

        data = retstr.getvalue()

        # with open(os.path.join('../../', f'pdf page {page_no}.txt'), 'wb') as file:
            # file.write(data.endoe)
            # file.write(data.encode('utf-8'))
        # print(data.encode('utf-8'))
        # lines = data.encode('utf-8')
        # print(lines)
        if pageNumber >= 1: continue
        lines = data.split("\n")
        print(lines)
        for l in lines:
            print(l.isspace())
        # lines = str(lines)
        # print(lines)
        # print(lines.decode('utf-8'))
        # lines = lines.split("\n")
        # for l in lines:
        #     print(l)
        # print(len(lines))
        # print(lines)
        data = ''
        retstr.truncate(0)
        retstr.seek(0)

    page_no += 1