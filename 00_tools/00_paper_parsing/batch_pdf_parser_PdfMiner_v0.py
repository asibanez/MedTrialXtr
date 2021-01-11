# Converts pdf documents to txt files
# v1 -> Batch processing


from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from io import StringIO
import tqdm
import glob
import nltk
import os
#nltk.download('punkt')

# Function definitions
# Conversion from pdf to txt
def convert_pdf_to_txt(input_path):
    rsrcmgr = PDFResourceManager()
    retstr = StringIO()
    codec = 'utf-8'
    laparams = LAParams()
    device = TextConverter(rsrcmgr, retstr, codec=codec, laparams=laparams)
    fp = open(input_path, 'rb')
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    password = ""
    maxpages = 0
    caching = True
    pagenos=set()

    for page in PDFPage.get_pages(fp, pagenos, maxpages=maxpages, password=password,
                                  caching=caching, check_extractable=True):
        interpreter.process_page(page)

    text = retstr.getvalue()
    fp.close()
    device.close()
    retstr.close()
    return text

input_dir = 'C:\\Users\\siban\\Dropbox\\CSAIL\\Projects\\01_Local\\10_Takeda\\OneDrive_2020-07-21\\TAEG018 MIT SLR'
output_dir = 'C:\\Users\\siban\\Dropbox\\CSAIL\\Projects\\01_Local\\10_Takeda\\OneDrive_2020-07-21\\TAEG018 MIT SLR\\parsed_to_text'

for txt_file in tqdm.tqdm(glob.glob(os.path.join(input_dir, '*.pdf')), desc = 'Parsing pdfs'):
    try:
        text = convert_pdf_to_txt(txt_file)
        output_file = os.path.basename(txt_file).split('.')[0] + '.txt'
        output_path = os.path.join(output_dir, output_file)

        with open(output_path, 'w') as fw:
            fw.write(text)

    except Exception:
        pass
