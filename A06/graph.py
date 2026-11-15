import csv
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np


OUTPUT_DIR = Path(__file__).resolve().parent
CSV_PATH = OUTPUT_DIR / "graph.csv"
PNG_PATH = OUTPUT_DIR / "graph.png"


def generate_csv() -> None:
    x_values = np.linspace(0, 10, 201)

    with CSV_PATH.open("w", newline="", encoding="utf-8") as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(["x", "y"])
        writer.writerows((f"{x:.2f}", f"{np.sqrt(x):.4f}") for x in x_values)


def create_graph() -> None:
    data = np.genfromtxt(CSV_PATH, delimiter=",", names=True)

    plt.figure(figsize=(8, 5))
    plt.plot(data["x"], data["y"], label="y = √x")
    plt.title("Odmocninová závislost")
    plt.xlabel("x")
    plt.ylabel("y")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.savefig(PNG_PATH, dpi=150)
    plt.close()


def main() -> None:
    generate_csv()
    create_graph()
    print(f"Data byla uložena do {CSV_PATH}")
    print(f"Graf byl uložen do {PNG_PATH}")


if __name__ == "__main__":
    main()
