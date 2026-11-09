"""Convert CDXML files to one SDF file and report the closest pair."""

import argparse
import glob
import importlib
from pathlib import Path


def load_chemistry_tools():
    try:
        chem = importlib.import_module("rdkit.Chem")
    except ModuleNotFoundError as error:
        if error.name not in {"rdkit", "rdkit.Chem"}:
            raise
        raise RuntimeError(
            "RDKit is required to read CDXML files. "
            "Install it with: python -m pip install rdkit"
        ) from error

    try:
        pybel = importlib.import_module("openbabel.pybel")
    except ModuleNotFoundError as error:
        if error.name not in {"openbabel", "openbabel.pybel"}:
            raise

        try:
            pybel = importlib.import_module("pybel")
        except ModuleNotFoundError as pybel_error:
            if pybel_error.name != "pybel":
                raise
            raise RuntimeError(
                "Open Babel and its Python bindings are required. "
                "Install them with: python -m pip install openbabel-wheel"
            ) from pybel_error

    return chem, pybel


def main():
    parser = argparse.ArgumentParser(
        description="Convert CDXML files to SDF and find their most similar pair."
    )
    parser.add_argument(
        "files",
        nargs="+",
        metavar="FILE_OR_PATTERN",
        help="CDXML filename/pattern, and optionally a new .sdf output filename",
    )
    arguments = parser.parse_args()

    patterns = []
    output = None
    for argument in arguments.files:
        if argument.lower().endswith(".sdf"):
            if output is None and not Path(argument).exists():
                output = argument
        else:
            patterns.append(argument)

    if not patterns:
        parser.error("Provide at least one CDXML file or wildcard pattern.")

    input_files = []
    for pattern in patterns:
        matches = sorted(
            filename
            for filename in glob.glob(pattern)
            if Path(filename).is_file()
            and Path(filename).suffix.lower() == ".cdxml"
        )
        if not matches:
            parser.error(f"No CDXML files matched: {pattern}")
        for filename in matches:
            if filename not in input_files:
                input_files.append(filename)

    try:
        chem, pybel = load_chemistry_tools()
    except RuntimeError as error:
        parser.error(str(error))

    sdf_records = []
    fingerprints = []
    for filename in input_files:
        cdxml = Path(filename).read_text(encoding="utf-8")
        rdkit_molecules = chem.MolsFromCDXML(cdxml, sanitize=False)
        if not rdkit_molecules:
            parser.error(f"No molecule could be read from {filename}")

        for rdkit_molecule in rdkit_molecules:
            mol_block = chem.MolToMolBlock(rdkit_molecule)
            molecule = pybel.readstring("mol", mol_block)
            molecule.title = Path(filename).name
            record = molecule.write("sdf").rstrip()
            if not record:
                parser.error(f"Could not convert {filename} to SDF")
            if not record.endswith("$$$$"):
                record += "\n$$$$"
            sdf_records.append(record + "\n")
            fingerprints.append((filename, molecule.calcfp("fp2")))

    output = output or "cdxml2sdf.sdf"
    Path(output).write_text("".join(sdf_records), encoding="utf-8")

    if len(fingerprints) < 2:
        print(f"Wrote {len(fingerprints)} molecule(s) to {output}")
        print("At least two molecules are needed to find a similar pair.")
        return

    best_pair = None
    for first in range(len(fingerprints) - 1):
        for second in range(first + 1, len(fingerprints)):
            similarity = fingerprints[first][1] | fingerprints[second][1]
            if best_pair is None or similarity > best_pair[0]:
                best_pair = (
                    similarity,
                    fingerprints[first][0],
                    fingerprints[second][0],
                )

    similarity, first_file, second_file = best_pair
    print(f"Wrote {len(fingerprints)} molecule(s) to {output}")
    print(
        f"Most similar: {first_file} and {second_file} "
        f"(Tanimoto similarity: {similarity:.3f})"
    )


if __name__ == "__main__":
    main()
