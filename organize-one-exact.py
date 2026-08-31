#!/usr/bin/env python3


import argparse
import os
import sys

import pandas as pd
import numpy as np


def parse_arguments() -> argparse.Namespace:
    parser: argparse.ArgumentParser = argparse.ArgumentParser(
            description="Add Latex table version for all Excel tables.")
    parser.add_argument("--directory-root", type=str, required=True,
            help="Path to root output directory.")
    return parser.parse_args()


def walk_and_convert(export_root: str) -> None:
    assert os.path.isdir(export_root)
    root: str; dirs: list[str]; files: list[str]
    for root, dirs, files in os.walk(export_root):
        for name in files:
            if name.endswith(".xlsx"):
                excel_path: str = os.path.join(root, name)
                latex_path: str = os.path.join(root, name[:-5] + ".tex")
                df: pd.DataFrame = pd.read_excel(excel_path)
                df.to_latex(latex_path, index=False)


if __name__ == '__main__':
    args: argparse.Namespace = parse_arguments()
    walk_and_convert(args.directory_root)


