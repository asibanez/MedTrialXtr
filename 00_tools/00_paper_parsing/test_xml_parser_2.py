import xml.etree.ElementTree as ETree

parser = ETree.XMLParser(encoding = 'utf-8')

mytree = ETree.parse('C:\\Users\\siban\\Dropbox\\CSAIL\\Projects\\01_Local\\10_Takeda\\Papers\\01_unchanged_pdfs\\chang_2007_new.xml', parser = parser)


from lxml import etree
parser = etree.XMLParser(recover=True)
etree.fromstring(xmlstring, parser=parser)



fr = open('C:\\Users\\siban\\Dropbox\\CSAIL\\Projects\\01_Local\\10_Takeda\\Papers\\01_unchanged_pdfs\\chang_2007.xml', 'rb')
string = fr.read()
string_new = string.replace(b'\x0c', b'')
fr.close()

fw = open('C:\\Users\\siban\\Dropbox\\CSAIL\\Projects\\01_Local\\10_Takeda\\Papers\\01_unchanged_pdfs\\chang_2007_new.xml', 'wb')
fw.write(string_new)
fw.close()


