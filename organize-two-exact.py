#!/usr/bin/env python3
from platform import machine
from typing import TextIO
from collections import OrderedDict

import os
import json
import argparse

import pandas as pd

from dual.constants import JobNames
from dual.constants import CustomerNames
from dual.constants import MachineNames
from dual.constants import ConfigurationKeys
from dual.constants import TableFields
from dual.constants import TableNames
from dual.tables import ConfigurationTables
from dual.tables import form_result_table
from dual.tables import form_job_proba_table
from dual.tables import form_tier_proba_table
from dual.tables import form_common_table
from dual.tables import form_main_table
from dual.tables import form_configuration_tables


def parse_arguments() -> argparse.Namespace:
    parser: argparse.ArgumentParser = argparse.ArgumentParser(
            description="Form tables from C++ export json.")
    parser.add_argument("--result-json-path", type=str, required=True,
                        help="Path to the input JSON file with results.")
    parser.add_argument("--configuration-json-path", type=str, required=True,
                        help="Path to the input JSON file with configuration.")
    parser.add_argument("--export-dir", type=str, required=True,
                        help="Directory to save the prepared tables.")
    return parser.parse_args()


if __name__ == '__main__':
    args: argparse.Namespace = parse_arguments()
    result_table: pd.DataFrame = form_result_table(args.result_json_path)
    os.makedirs(args.export_dir, exist_ok=True)
    result_table.to_excel(
        os.path.join(args.export_dir, TableNames.RESULTS_EXCEL),
        float_format="%.2f", header=True, index=False)
    result_table.to_latex(
        os.path.join(args.export_dir, TableNames.RESULTS_LATEX),
        float_format="%.2f", header=True, index=False)

    configuration_frames: ConfigurationTables = form_configuration_tables(
        args.configuration_json_path)
    configuration_frames.common_table.to_excel(
        os.path.join(args.export_dir, TableNames.COMMON_CONFIG_EXCEL) ,
        float_format="%.2f", header=True, index=False)
    configuration_frames.main_table.to_excel(
        os.path.join(args.export_dir, TableNames.MAIN_CONFIG_EXCEL) ,
        float_format="%.2f", header=True, index=False)
    configuration_frames.job_proba_table.to_excel(
        os.path.join(args.export_dir, TableNames.PROBA_JOB_TYPE_CONFIG_EXCEL) ,
        float_format="%.2f", header=True, index=False)
    configuration_frames.tier_proba_table.to_excel(
        os.path.join(args.export_dir, TableNames.TIER_JOB_TYPE_CONFIG_EXCEL) ,
        float_format="%.2f", header=True, index=False)

    configuration_frames.common_table.to_latex(
        os.path.join(args.export_dir, TableNames.COMMON_CONFIG_LATEX) ,
        float_format="%.2f", header=True, index=False)
    configuration_frames.main_table.to_latex(
        os.path.join(args.export_dir, TableNames.MAIN_CONFIG_LATEX) ,
        float_format="%.2f", header=True, index=False)
    configuration_frames.job_proba_table.to_latex(
        os.path.join(args.export_dir, TableNames.PROBA_JOB_TYPE_CONFIG_LATEX) ,
        float_format="%.2f", header=True, index=False)
    configuration_frames.tier_proba_table.to_latex(
        os.path.join(args.export_dir, TableNames.TIER_JOB_TYPE_CONFIG_LATEX) ,
        float_format="%.2f", header=True, index=False)


