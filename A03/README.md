git clone git@github.com:prochazg/ci2.git
cd ci2
mkdir A03
mv ~/Downloads/PubChem_compound_benzidine.xml A03/
cd A03
python3 -m venv venv
source venv/bin/activate
pip install beautifulsoup4 lxml
python3 pubchem_parser.py PubChem_compound_benzidine.xml
