# Converts pdf documents to txt files
# v1 -> Batch processing

from lxml import etree
import codecs
import tqdm
import glob
import os

# Conversion from pdf to txt
def convert_xml_to_txt(path):
    text = ''
    tree = etree.parse(path, parser = parser)
    tags = [['P', 'H1', 'H2', 'H3',
             'H4', 'H5', 'H6']]
    
    for elem in tree.iter(tag = tags):
        if elem.text != None:
            text = text + elem.text.strip('\n').strip() + '\n\n'

    return(text)

input_dir = 'C:\\Users\\siban\\Dropbox\\CSAIL\\Projects\\01_Local\\10_Takeda\\02_papers_final\\02_clean\\01_xmls'
output_dir = 'C:\\Users\\siban\\Dropbox\\CSAIL\\Projects\\01_Local\\10_Takeda\\02_papers_final\\02_clean\\02_txts'

parser = etree.XMLParser(recover=True, encoding = 'utf-8')

for xml_file in tqdm.tqdm(glob.glob(os.path.join(input_dir, '*.xml')), desc = 'Parsing xmls'):
    text = convert_xml_to_txt(xml_file)
    output_file = os.path.basename(xml_file).split('.')[0] + '.txt'
    output_path = os.path.join(output_dir, output_file)

    with codecs.open(output_path, 'w', 'utf-8') as fw:
        fw.write(text)
