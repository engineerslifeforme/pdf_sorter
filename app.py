""" PDF sorter """

from pathlib import Path
import shutil
import datetime

import streamlit as st

from pdf_helper import display_pdf, get_dates

st.set_page_config(layout="wide")

"""# PDF Sorter"""


pdf_dir = Path(st.text_input("PDF Directory", value='~/Documents/Doxie_Output'))
if not pdf_dir.exists():
    st.error(f'{pdf_dir} does not exist')
if pdf_dir == '':
    st.error('Chose a PDF directory')
    st.stop()
pdf_files = list(pdf_dir.glob('*.pdf'))
st.markdown(f'{len(pdf_files)} PDF files found!')

output_dir = Path(st.text_input("PDF Output Directory"))
output_dir.mkdir(exist_ok=True)

review_index = int(st.number_input('Item Index to Review', value=0, min_value=0, max_value=len(pdf_files)-1))
chosen_file = pdf_files[review_index]
st.markdown(f'Reviewing {chosen_file.name}')
page_number = int(st.number_input('PDF page # to display', value=0, step=1))
left, right = st.columns((4,1))
display_pdf(pdf_files[review_index], location=left, page=page_number)
failed = False
dates = []
dates = get_dates(chosen_file)
# try:
#     dates = get_dates(chosen_file)
# except:
#     right.warning('Failed to get dates from file')
#     failed = True
if failed or len(dates) == 0:
    dates = [datetime.datetime.today()]

right.write(dates)
include_date = right.checkbox('Include date in name?', value=True)
pdf_date = right.date_input('PDF Date', value=dates[0].date())
label = right.text_input('Label').lower().replace(' ', '_')
if include_date:
    new_filename = f'{pdf_date.strftime("%Y%m%d")}_{label}.pdf'
else:
    new_filename = f'{label}.pdf'
right.markdown(f'New filename: {new_filename}')

if right.button('Relabel'):
    desination = output_dir / new_filename
    if desination.exists():
        right.error(f'{desination} already exists!')
    else:
        shutil.copy2(chosen_file, desination)
        chosen_file.unlink()
if right.button("Delete"):
    chosen_file.unlink()