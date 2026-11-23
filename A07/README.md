```bash
Generates an image of five alanine molecules placed at the vertices of a regular pentagon.

git clone git@github.com:prochazg/ci2.git
cd ci2\A07
python -m venv .venv
.venv\Scripts\python.exe -m pip install openbabel-wheel

$babel = Join-Path $PWD ".venv\Lib\site-packages\openbabel\bin"
$env:BABEL_DATADIR = Join-Path $babel "data"
& (Join-Path $babel "obabel.exe") .\ala.smi -O .\ala.pov --gen3D

Requires POV-Ray 3.7 with its bin folder on PATH:
pvengine64.exe /RENDER .\ala5.pov +FN +Oala5.png /EXIT
