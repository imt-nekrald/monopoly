#!/usr/bin/env python3

from collections import OrderedDict

import os
import json
import argparse

import pandas as pd


def parse_arguments() -> argparse.Namespace:
    parser: argparse.ArgumentParser = argparse.ArgumentParser(
            description="Form tables from C++ export json.")
    parser.add_argument("--json-path", type=str, required=True,
                        help="Path to the input JSON file.")
    parser.add_argument("--export-dir", type=str, required=True,
                        help="Directory to save the prepared tables.")
    return parser.parse_args()


def form_table(json_path: str) -> pd.DataFrame:
    data: list[dict[str, float]] = list()
    with open(json_path, 'r') as file_json:
        data = json.load(file_json)

    lenth_column: list[int] = list()
    dynamic_column: list[float] = list()
    static_column: list[float] = list()
    constant_column: list[float] = list()

    for entry in data:
        lenth_column.append(entry["horizon-length"])
        dynamic_column.append(entry["dynamic-revenue"])
        if "static-revenue" in entry:
            static_revenue: float = float(entry["static-revenue"])
            static_column.append(f"{static_revenue :.2f}")
        else:
            static_column.append("N/A")
        constant_column.append(entry["constant-revenue"])

    table: pd.DataFrame = pd.DataFrame.from_dict(
        OrderedDict({
            "Horizon": lenth_column,
            "Dynamic": dynamic_column,
            "Static": static_column,
            "Constant": constant_column
        }))
    return table.transpose()


if __name__ == '__main__':
    args: argparse.Namespace = parse_arguments()
    table: pd.DataFrame = form_table(args.json_path)
    os.makedirs(args.export_dir, exist_ok=True)
    table.to_excel(
        os.path.join(args.export_dir, "table.xlsx"),
        float_format="%.2f",
        header=False,
        index=True
    )
    table.to_latex(
        os.path.join(args.export_dir, "table.tex"),
        float_format="%.2f",
        header=False,
        index=True
    )


