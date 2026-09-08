#!/usr/bin/env python3
from typing import Optional
from typing import Any
from typing import TextIO
from collections import OrderedDict

import os
import json
import argparse

import pandas as pd


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


def form_result_table(json_path: str) -> pd.DataFrame:
    data: list[dict[str, float]] = list()
    file_json: TextIO
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


class ConfigurationTables:
    def __init__(self) -> None:
        self.main_table: Optional[pd.DataFrame] = None
        self.job_proba_table: Optional[pd.DataFrame] = None
        self.tier_proba_table: Optional[pd.DataFrame] = None
    

class JobNames:
    SIMPLE: str = 'simple'
    COMPLEX: str = 'complex'


class ConfigurationKeys:
    MAX_HORIZON_DP: str = "max-horizon-dp"
    DECLINE_COSTS: str = "decline-costs"
    DELIVERY_DURATIONS: str = "delivery-durations"
    DUE_DURATIONS: str = "due-durations"
    DUE_PENALTIES: str = "due-penalties"
    JOB_DURATIONS: str = "job-durations"
    JOB_TYPE_PROBA: str = "job-type-proba"
    MAX_HORIZON_STATIC: str = "max-horizon-static"
    N_MACHINES: str ="n-machines"
    RELEASE_DURATIONS: str = "release-durations"
    TIER_PROBA: str = "tier-proba"
    UPPER_WTP: str = "upper-wtp"
    WILLINGNESS_TO_PAY: str = "willingness-to-pay"


def form_job_proba_table(list_data: list[list[float]]) -> pd.DataFrame:   
    raise NotImplementedError("Needs implementation.")


def form_tier_proba_table(list_data: list[list[float]]) -> pd.DataFrame:   
    raise NotImplementedError("Needs implementation.")



def form_configuration_tables(json_path: str) -> ConfigurationTables:
    raise NotImplementedError("Needs implementation.")
    json_data: dict[str, Any]
    file_json: TextIO
    with open(json_path, 'r') as file_json:
        json_data = json.load(file_json)
    response: ConfigurationTables = ConfigurationTables()
    response.job_proba_table = form_job_proba_table(json_data[ConfigurationKeys.JOB_TYPE_PROBA])
    response.tier_proba_table = form_tier_proba_table(json_data[ConfigurationKeys.TIER_PROBA])
    
    name_column: list[str] = list()
    value_column: list[str] = list()

    raise NotImplementedError("Needs implementation.")
    return response


if __name__ == '__main__':
    args: argparse.Namespace = parse_arguments()
    result_table: pd.DataFrame = form_result_table(args.result_json_path)
    os.makedirs(args.export_dir, exist_ok=True)
    result_table.to_excel(
        os.path.join(args.export_dir, "result-table.xlsx"),
        float_format="%.2f", header=False, index=True)
    result_table.to_latex(
        os.path.join(args.export_dir, "result-table.tex"),
        float_format="%.2f", header=False, index=True)


