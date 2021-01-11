from lxml import etree

path = 'C:\\Users\\siban\\Dropbox\\CSAIL\\Projects\\01_Local\\10_Takeda\\Papers\\01_unchanged_pdfs\\xmls\\chang_2007.xml'
parser = etree.XMLParser(recover=True, encoding = 'utf-8')
tree = etree.parse(path, parser = parser)

text = etree.tostring(tree).decode('utf-8').split('\n')
root = tree.getroot()

#%%
for elem in root:
    print(elem.text)
    
#%%
tags = [['P', 'H1', 'H2', 'H3',
         'H4', 'H5', 'H6']]
for elem in tree.iter(tag = tags):
    print(elem.text, '\n')
#%%