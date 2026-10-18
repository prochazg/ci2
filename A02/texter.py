import re
import sys


class Texter:
    """Třída pro analýzu textového souboru."""

    def __init__(self, soubor):
        # Uložíme si cestu k souboru
        self.soubor = soubor

    def run(self):
        # Pokusíme se otevřít a přečíst soubor
        try:
            with open(self.soubor, "r", encoding="utf-8") as f:
                text = f.read()
        except FileNotFoundError:
            print(f"Chyba: Soubor '{self.soubor}' nebyl nalezen.")
            return

        # Rozdělíme text na slova podle mezer
        slova = text.split()
        cista_slova = []

        # Očistíme každé slovo od interpunkce (tečky, čárky atd.)
        # a převedeme na malá písmena
        for slovo in slova:
            ciste = re.sub(r"^[^\w]+|[^\w]+$", "", slovo)
            if ciste:
                cista_slova.append(ciste.lower())

        # a) Počet všech unikátních (různých) slov v souboru
        unikatni_slova = set(cista_slova)
        pocet_unikatnich = len(unikatni_slova)

        # b) Nejčastěji se opakující slovo a kolikrát se opakuje
        cetnost = {}
        for slovo in cista_slova:
            cetnost[slovo] = cetnost.get(slovo, 0) + 1

        if cetnost:
            nejcastejsi_slovo = max(cetnost, key=cetnost.get)
            pocet_opakovani = cetnost[nejcastejsi_slovo]
        else:
            nejcastejsi_slovo = "žádné"
            pocet_opakovani = 0

        # Výpis výsledků na obrazovku
        print(f"Počet unikátních slov: {pocet_unikatnich}")
        print(
            f"Nejčastější slovo: '{nejcastejsi_slovo}' "
            f"(vyskytuje se {pocet_opakovani}krát)"
        )


def zobraz_napovedu():
    """Funkce pro zobrazení nápovědy k použití skriptu."""
    print("Použití: python texter.py <nazev_souboru.txt>")


if __name__ == "__main__":
    # Kontrola, zda uživatel zadal argument (název souboru)
    if len(sys.argv) < 2:
        zobraz_napovedu()
        sys.exit(1)

    jmeno_souboru = sys.argv[1]
    analyzator = Texter(jmeno_souboru)
    analyzator.run()
