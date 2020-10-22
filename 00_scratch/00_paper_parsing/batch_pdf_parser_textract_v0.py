# Converts pdf documents to txt files
# v1 -> Batch processing

from tika import parser
import tqdm
import glob
import os

# Function definitions
# Conversion from pdf to txt
def convert_pdf_to_txt(path):
    raw = parser.from_file(path)
    text = (raw['content'])
    print(text)

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


file = 'C:\\Users\\siban\\Dropbox\\CSAIL\\Projects\\01_Local\\10_Takeda\\OneDrive_2020-07-21\\TAEG018 MIT SLR\\Avet-Loiseau 2010.pdf'
raw = parser.from_file(file)
