#!/usr/bin/env python3

from typing import TextIO
from typing import Any

import argparse
import json
import os
import sys
import math
from collections import OrderedDict

import pandas as pd
import numpy as np

from general.common import NameComponents
from general.profit import build_profit_table
from general.temporal import build_time_table
from general.gap import build_gap_table
from general.parameter import build_parameter_table
from general.order import build_order_table
from general.setting import build_setting_table


def parse_arguments() -> argparse.Namespace:
    parser: argparse.ArgumentParser = argparse.ArgumentParser(
            description="Read information from JSONs and organize in LaTeX-compatible form.")
    parser.add_argument("--directory-root", type=str, required=True,
            help="Path to root output directory.")
    return parser.parse_args()


def build_setting_table(directory_root: str) -> pd.DataFrame:
    configuration_json_path: str = os.path.join(
        directory_root, NameComponents.CONFIGURATION_TPL.format(setting_name))
    in_json: TextIO
    with open(configuration_json_path, "r") as in_json:
        dict_configuration = json.load(in_json)

    raise NotImplementedError("Needs implementation.")


class ExportNames:
    PROFIT_TEX: str = "profits.tex"
    PROFIT_XLSX: str = "profits.xlsx"
    TIME_TEX: str = "time.tex"
    TIME_XLSX: str = "time.xlsx"
    GAP_TEX: str = "gap.tex"
    GAP_XLSX: str = "gap.xlsx"
    PARAMETER_TEX: str = "parameter.tex"
    PARAMETER_XLSX: str = "parameter.xlsx"
    ORDER_TEX: str = "order.tex"
    ORDER_XLSX: str = "order.xlsx"
    SETTING_TEX: str = "setting.tex"
    SETTING_XLSX: str = "setting.xlsx"


if __name__ == '__main__':
    args: argparse.Namespace = parse_arguments()
    directory_path: str = os.path.abspath(args.directory_root)
    profit_df: pd.DataFrame = build_profit_table(directory_path)
    time_df: pd.DataFrame = build_time_table(directory_path)
    gap_df: pd.DataFrame = build_gap_table(directory_path)
    parameter_df: pd.DataFrame = build_parameter_table(directory_path)
    order_df: pd.DataFrame = build_order_table(directory_path)
    setting_df: pd.DataFrame = build_setting_table(directory_path)

    profit_df.to_latex(os.path.join(directory_path, ExportNames.PROFIT_TEX), index=False)
    time_df.to_latex(os.path.join(directory_path, ExportNames.TIME_TEX), index=False)
    gap_df.to_latex(os.path.join(directory_path, ExportNames.GAP_TEX), index=False)
    parameter_df.to_latex(os.path.join(directory_path, ExportNames.PARAMETER_TEX), index=False)
    order_df.to_latex(os.path.join(directory_path, ExportNames.ORDER_TEX), index=False)
    setting_df.to_latex(os.path.join(directory_path, ExportNames.SETTING_TEX), index=False)

    profit_df.to_excel(os.path.join(directory_path, ExportNames.PROFIT_XLSX), index=False)
    time_df.to_excel(os.path.join(directory_path, ExportNames.TIME_XLSX), index=False)
    gap_df.to_excel(os.path.join(directory_path, ExportNames.GAP_XLSX), index=False)
    parameter_df.to_excel(os.path.join(directory_path, ExportNames.PARAMETER_XLSX), index=False)
    order_df.to_excel(os.path.join(directory_path, ExportNames.ORDER_XLSX), index=False)
    setting_df.to_excel(os.path.join(directory_path, ExportNames.SETTING_XLSX), index=False)


    
