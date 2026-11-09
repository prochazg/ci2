git clone git@github.com:prochazg/ci2.git
cd ci2\A05
python -m venv .venv
.venv\Scripts\python.exe -m pip install rdkit openbabel-wheel
.venv\Scripts\python.exe .\cdxml2sdf.py "*.cdxml"
