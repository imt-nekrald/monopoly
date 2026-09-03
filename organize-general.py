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


def build_order_table(directory_root: str) -> pd.DataFrame:
    raise NotImplementedError("Needs implementation.")




if __name__ == '__main__':
    args: argparse.Namespace = parse_arguments()
    directory_path: str = os.path.abspath(args.directory_root)
    profit_df: pd.DataFrame = build_profit_table(directory_path)
    time_df: pd.DataFrame = build_time_table(directory_path)
    gap_df: pd.DataFrame = build_gap_table(directory_path)
    parameter_df: pd.DataFrame = build_parameter_table(directory_path)

    

