import sys
from bs4 import BeautifulSoup

def parse_pubchem_iupac(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            # Načtení XML pomocí BeautifulSoup
            soup = BeautifulSoup(f, 'xml')
    except FileNotFoundError:
        print(f"Chyba: Soubor '{file_path}' nebyl nalezen.")
        return

    # Hledání IUPAC názvů v XML struktuře
    iupac_elements = soup.find_all(lambda tag: 'iupac' in tag.name.lower())

    found_names = set()
    for element in iupac_elements:
        text = element.text.strip()
        if text and text not in found_names:
            found_names.add(text)
            print(text)

if __name__ == "__main__":
    # Kontrola, zda uživatel zadal název souboru jako argument příkazové řádky
    if len(sys.argv) < 2:
        print("Použití: python pubchem_parser.py <cesta_k_xml_souboru>")
        sys.exit(1)
    
    # První argument za názvem skriptu je cesta k souboru
    file_path = sys.argv[1]
    parse_pubchem_iupac(file_path)
