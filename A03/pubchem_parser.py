import sys
from bs4 import BeautifulSoup

if len(sys.argv) < 2:
    print("Použití: python pubchem_parser.py <soubor.xml>")
    sys.exit(1)

filename = sys.argv[1]

with open(filename, encoding='utf-8') as f:
    soup = BeautifulSoup(f, 'xml')

for urn in soup.find_all('PC-Urn'):
    label = urn.find('PC-Urn_label')
    if label and label.text == 'IUPAC Name':
        infodata = urn.find_parent('PC-InfoData')
        if infodata:
            sval = infodata.find('PC-InfoData_value_sval')
            if sval:
                print(sval.text)
