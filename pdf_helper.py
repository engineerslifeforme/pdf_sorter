""" PDF helper functions """

import base64
from pathlib import Path
import datetime

import streamlit as st
import PyPDF2
import datefinder

def display_pdf(file: Path, location = None, page=0):
    if location is None:
        location = st
    # Opening file from file path
    pdf = PyPDF2.PdfReader(str(file))
    pdf_writer = PyPDF2.PdfWriter()
    pdf_writer.add_page(pdf.pages[page])
    temp_file = 'temp.pdf'
    with open(temp_file, 'wb') as fh:
        pdf_writer.write(fh)
    with open(temp_file, "rb") as f:
        base64_pdf = base64.b64encode(f.read()).decode('utf-8')

    # Embedding PDF in HTML
    pdf_display = F'<iframe src="data:application/pdf;base64,{base64_pdf}" width="1000" height="1000" type="application/pdf"></iframe>'

    # Displaying File
    location.markdown(pdf_display, unsafe_allow_html=True)

def get_dates(path: Path) -> list:
    text = get_text_from_pdf(path)
    raw_dates = datefinder.find_dates(text)
    return [item for item in raw_dates if item > datetime.datetime(2010, 1, 1) and item.date() < datetime.date.today()]

# creating a pdf file object
def get_text_from_pdf(pdf_path: Path):
    with open(pdf_path, 'rb') as pdfFileObj:

        # creating a pdf reader object 
        pdfReader = PyPDF2.PdfFileReader(pdfFileObj) 

        # printing number of pages in pdf file 
        numpages = pdfReader.numPages

        page = 0
        text = ''
        while page < numpages:
            # creating a page object 
            #pageObj = pdfReader.getPage(0)
            pageObj = pdfReader.pages[0]

            # extracting text from page 
            text += pageObj.extractText()
            page += 1
    return text