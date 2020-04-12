import camelot 
import sys

def pdfTableCount(filename):
    tables = camelot.read_pdf(filename)
    return tables.n