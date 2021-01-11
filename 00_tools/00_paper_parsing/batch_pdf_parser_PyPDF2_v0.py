# Converts pdf documents to txt files
# v1 -> Batch processing

from PyPDF2 import PdfFileReader

import tqdm
import glob
import os

# Function definitions
# Conversion from pdf to txt
def convert_pdf_to_txt(path):
    with open(path, 'rb') as f:
        pdf = PdfFileReader(f)
        # get the first page
        page = pdf.getPage(3)
        print(page)
        print('Page type: {}'.format(str(type(page))))
        text = page.extractText()
        return(text)

input_dir = 'C:\\Users\\siban\\Dropbox\\CSAIL\\Projects\\01_Local\\10_Takeda\\Papers\\01_unchanged_pdfs\\'
output_dir = 'C:\\Users\\siban\\Dropbox\\CSAIL\\Projects\\01_Local\\10_Takeda\\Papers\\01_unchanged_pdfs\\parsed_txts\\'

for txt_file in tqdm.tqdm(glob.glob(os.path.join(input_dir, '*.pdf')), desc = 'Parsing pdfs'):
    try:
        text = convert_pdf_to_txt(txt_file)
        output_file = os.path.basename(txt_file).split('.')[0] + '.txt'
        output_path = os.path.join(output_dir, output_file)

        with open(output_path, 'w') as fw:
            fw.write(text)

    except Exception:
        pass
