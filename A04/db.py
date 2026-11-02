import sys
import os
import sqlite3
import zipfile
import csv
import io


class WorldDatabase:
    def __init__(self, args):
        self.csv_files = args
        self.base_dir = os.path.dirname(os.path.abspath(__file__))
        self.db_name = os.path.join(self.base_dir, "db.sqlite")
        self.zip_name = os.path.join(self.base_dir, "world.zip")

        try:
            sys.stdout.reconfigure(encoding='utf-8')
        except Exception:
            pass

        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()

        self.nacti_csv_soubory()
        self.vyres_otazku()
        self.conn.close()

    def tabulka_existuje(self, table_name):
        """Zjistí, zda tabulka v databázi již existuje."""
        self.cursor.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name=?",
            (table_name,),
        )
        return self.cursor.fetchone() is not None

    def uprav_nazev_sloupce(self, nazev, index):
        """Vyčistí název sloupce a doplní náhradní jméno, pokud je prázdný."""
        upraveny = nazev.strip().strip('"').strip("'").strip()
        if upraveny:
            return upraveny
        return f"col_{index}"

    def nacti_csv_soubory(self):
        """Načte CSV soubory z archivu a vytvoří odpovídající tabulky v databázi."""
        if not self.csv_files:
            print("Žádné parametry nezadány. Pokračuji s existující databází.")
            return

        if not os.path.exists(self.zip_name):
            print(f"Chyba: Archiv '{os.path.basename(self.zip_name)}' nebyl nalezen ve složce.")
            return

        try:
            with zipfile.ZipFile(self.zip_name, 'r') as archiv:
                for csv_filename in self.csv_files:
                    table_name = os.path.splitext(os.path.basename(csv_filename))[0]

                    if self.tabulka_existuje(table_name):
                        print(f"Tabulka '{table_name}' již existuje. Přeskakuji vytváření.")
                        continue

                    if csv_filename not in archiv.namelist():
                        print(f"Soubor '{csv_filename}' nebyl v archivu nalezen.")
                        continue

                    with archiv.open(csv_filename) as soubor:
                        text_stream = io.TextIOWrapper(soubor, encoding='utf-8-sig', newline='')
                        reader = csv.reader(text_stream, delimiter=';')

                        headers = next(reader, None)
                        if headers is None:
                            print(f"Soubor '{csv_filename}' je prázdný.")
                            continue

                        sloupce = [self.uprav_nazev_sloupce(h, i) for i, h in enumerate(headers)]
                        nazvy = ", ".join(f'"{s}" TEXT' for s in sloupce)
                        self.cursor.execute(f'CREATE TABLE "{table_name}" ({nazvy});')

                        insert_sql = (
                            f'INSERT INTO "{table_name}" ({", ".join(f'"{s}"' for s in sloupce)}) '
                            f'VALUES ({", ".join("?" for _ in sloupce)})'
                        )

                        rows = []
                        for row in reader:
                            if not row:
                                continue
                            if len(row) < len(sloupce):
                                row.extend([''] * (len(sloupce) - len(row)))
                            elif len(row) > len(sloupce):
                                row = row[:len(sloupce)]
                            rows.append(row)

                        if rows:
                            self.cursor.executemany(insert_sql, rows)

                        self.conn.commit()
                        print(f"Tabulka '{table_name}' byla úspěšně vytvořena a naplněna.")

        except Exception as e:
            print(f"Chyba při práci s archívem '{os.path.basename(self.zip_name)}': {e}")

    def vyres_otazku(self):
        """Vyhledá odpověď na otázku č. 9 a vytiskne ji."""
        otazka = "How many countries use Arabic as an official language?"
        dotaz = """
            SELECT COUNT(DISTINCT CountryCode)
            FROM countrylanguage
            WHERE LOWER(Language) = 'arabic'
              AND (LOWER(IsOfficial) = 't' OR LOWER(IsOfficial) = 'true' OR IsOfficial = '1');
        """

        try:
            vysledek = self.cursor.execute(dotaz).fetchone()[0]
        except Exception as e:
            vysledek = f"Chyba při provádění dotazu: {e}"

        print("-" * 50)
        print(f"Question: {otazka}")
        print(f"Answer: {vysledek}")
        print("-" * 50)


if __name__ == "__main__":
    app = WorldDatabase(sys.argv[1:])
