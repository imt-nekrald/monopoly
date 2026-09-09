#!/usr/bin/env python3
from platform import machine
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
            static_column.append("N.A.")
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
        self.main_table: pd.DataFrame | None = None
        self.common_table: pd.DataFrame | None = None
        self.job_proba_table: pd.DataFrame | None = None
        self.tier_proba_table: pd.DataFrame | None = None


class JobNames:
    COMPLEX: str = 'complex'
    SIMPLE: str = 'simple'

    IDX_2_NAME: list[str] = [COMPLEX, SIMPLE]
    NAME_2_IDX: dict[str, int] = {COMPLEX: 0, SIMPLE: 1}


class CustomerNames:
    REGULAR: str = 'regular'
    WEALTHY: str=  'wealthy'

    IDX_2_NAME: list[str] = [REGULAR, WEALTHY]
    NAME_2_IDX: dict[str, int]  = {REGULAR: 0, WEALTHY: 1}


class MachineNames:
    FAST: str = 'fast'
    STANDARD: str = 'standard'
    
    IDX_2_NAME: list[str] = [FAST, STANDARD]
    NAME_2_IDX: dict[str, int] = {FAST: 0, STANDARD: 1}


class ConfigurationKeys:
    N_MACHINES: str = "n-machines"
    MAX_HORIZON_DP: str = "max-horizon-dp"
    MAX_HORIZON_STATIC: str = "max-horizon-static"
    UPPER_WTP: str = "upper-wtp"

    JOB_DURATIONS: str = "job-durations"
    DELIVERY_DURATIONS: str = "delivery-durations"
    RELEASE_DURATIONS: str = "release-durations"
    DUE_DURATIONS: str = "due-durations"
    WILLINGNESS_TO_PAY: str = "willingness-to-pay"
    DUE_PENALTIES: str = "due-penalties"
    DECLINE_COSTS: str = "decline-costs"
    JOB_TYPE_PROBA: str = "job-type-proba"
    TIER_PROBA: str = "tier-proba"


class TableFields:
    COLUMN_PARAMETER: str = 'Parameter'
    COLUMN_VALUE: str = 'Value'

    FIELD_N_MACHINES: str = 'Number of machines'
    FIELD_MAX_HORIZON_DYNAMIC: str = 'Maximal horizon for profile dynamic'
    FIELD_MAX_HORIZON_STATIC: str = 'Maximal horizon for static search'
    FIELD_UPPER_WTP: str = "Upper bound on WTP"

    FIELD_JOB_DURATIONS: str = 'Processing terms per machine'
    FIELD_DELIVERY_DURATIONS: str = 'Delivery durations per machine'
    FIELD_RELEASE_DURATIONS: str = 'Release terms'
    FIELD_DUE_DURATIONS:  str = 'Due terms'
    FIELD_WTP: str = 'Willingness to pay'
    FIELD_DUE_PENALTY: str = 'Tardiness fee'
    FIELD_DECLINE_COST: str = 'Decline penalty'


def form_job_proba_table(list_data: list[list[float]]) -> pd.DataFrame:   
    raise NotImplementedError("Needs implementation.")


def form_tier_proba_table(list_data: list[list[float]]) -> pd.DataFrame:   
    raise NotImplementedError("Needs implementation.")


def form_common_table(json_data: dict[str, any]) -> pd.DataFrame:
    # Common Table
    common_dict: dict[str, list[str]] = OrderedDict()
    name_column: list[str] = [ 
        TableFields.FIELD_N_MACHINES, 
        TableFields.FIELD_MAX_HORIZON_DYNAMIC, 
        TableFields.FIELD_MAX_HORIZON_STATIC, 
        TableFields.FIELD_UPPER_WTP]
    value_column: list[str] = [
        str(json_data[ConfigurationKeys.N_MACHINES]), 
        str(json_data[ConfigurationKeys.MAX_HORIZON_DP]),
        str(json_data[ConfigurationKeys.MAX_HORIZON_STATIC]),
        str(json_data[ConfigurationKeys.UPPER_WTP])]
    common_dict[TableFields.COLUMN_PARAMETER] = name_column
    common_dict[TableFields.COLUMN_VALUE] = value_column
    return pd.DataFrame.from_dict(common_dict)


def form_main_table(json_data: dict[str, any]) -> pd.DataFrame:
    # Main Table
    building_dict: dict[str, list[str]] =  OrderedDict()
    parameter_column: list[str] = list()
    simple_column: list[str] = list()
    complex_column: list[str] = list()

    parameter_column.append(TableFields.FIELD_JOB_DURATIONS)
    simple_durations: list[int] = json_data[
        ConfigurationKeys.JOB_DURATIONS][JobNames.NAME_2_IDX[JobNames.SIMPLE]]
    simple_fast_duration: int = simple_durations[MachineNames.NAME_2_IDX[MachineNames.FAST]]
    simple_std_duration: int = simple_durations[MachineNames.NAME_2_IDX[MachineNames.FAST]]
    simple_column.append(f"{MachineNames.FAST}: {simple_fast_duration}," 
                         + f"{MachineNames.STANDARD}: {simple_std_duration} ")
    complex_durations: list[int] = json_data[ConfigurationKeys.JOB_DURATIONS
                                             ][JobNames.NAME_2_IDX[JobNames.COMPLEX]]
    complex_fast_duration: int = complex_durations[MachineNames.NAME_2_IDX[MachineNames.FAST]]
    complex_std_duration: int = complex_durations[MachineNames.NAME_2_IDX[MachineNames.FAST]]
    complex_column.append(f"{MachineNames.FAST}: {complex_fast_duration}," 
                          + f"{MachineNames.STANDARD}: {complex_std_duration} ")
    
    parameter_column.append(TableFields.FIELD_DELIVERY_DURATIONS)
    simple_delivery: list[int] = json_data[
        ConfigurationKeys.DELIVERY_DURATIONS][JobNames.NAME_2_IDX[JobNames.SIMPLE]]
    simple_fast_delivery: int = simple_delivery[MachineNames.NAME_2_IDX[MachineNames.FAST]]
    simple_std_delivery: int = simple_delivery[MachineNames.NAME_2_IDX[MachineNames.FAST]]
    simple_column.append(f"{MachineNames.FAST}: {simple_fast_delivery}," 
                         + f"{MachineNames.STANDARD}: {simple_std_delivery} ")
    complex_delivery: list[int] = json_data[ConfigurationKeys.DELIVERY_DURATIONS
                                             ][JobNames.NAME_2_IDX[JobNames.COMPLEX]]
    complex_fast_delivery: int = complex_delivery[MachineNames.NAME_2_IDX[MachineNames.FAST]]
    complex_std_delivery: int = complex_delivery[MachineNames.NAME_2_IDX[MachineNames.FAST]]
    complex_column.append(f"{MachineNames.FAST}: {complex_fast_delivery}," 
                          + f"{MachineNames.STANDARD}: {complex_std_delivery} ")
    
    parameter_column.append(TableFields.FIELD_RELEASE_DURATIONS)
    release_durations: list[int] = json_data[ConfigurationKeys.RELEASE_DURATIONS]
    simple_column.append(str(release_durations[JobNames.NAME_2_IDX[JobNames.SIMPLE]]))
    complex_column.append(str(release_durations[JobNames.NAME_2_IDX[JobNames.COMPLEX]]))
    parameter_column.append(TalbeFields.FIELD_DUE_DURATIONS)
    due_durations: list[int] = json_data[ConfigurationKeys.DUE_DURATIONS]
    simple_column.append(str(due_durations[JobNames.NAME_2_IDX[JobNames.SIMPLE]]))
    complex_column.append(str(due_durations[JobNames.NAME_2_IDX[JobNames.COMPLEX]]))
 
    parameter_column.append(TableFields.FIELD_WTP)
    simple_wtp: list[float] = json_data[ConfigurationKeys.WILLINGNESS_TO_PAY
                                      ][JobNames.NAME_2_IDX[JobNames.SIMPLE]]
    simple_regular_wtp: float = simple_wtp[CustomerNames.NAME_2_IDX[CustomerNames.REGULAR]]
    simple_wealthy_wtp: float = simple_wtp[CustomerNames.NAME_2_IDX[CustomerNames.WEALTHY]]
    simple_column.append(f"{CustomerNames.REGULAR}: {simple_regular_wtp :.2f}," 
                         + f"{CustomerNames.WEALTHY}: {simple_wealthy_wtp :.2f} ")
    complex_wtp: list[float] = json_data[ConfigurationKeys.WILLINGNESS_TO_PAY
                                       ][JobNames.NAME_2_IDX[JobNames.COMPLEX]]
    complex_regular_wtp: float = complex_wtp[CustomerNames.NAME_2_IDX[CustomerNames.REGULAR]]
    complex_wealthy_wtp: float = complex_wtp[CustomerNames.NAME_2_IDX[CustomerNames.WEALTHY]]
    complex_column.append(f"{CustomerNames.REGULAR}: {complex_regular_wtp :.2f}," 
                         + f"{CustomerNames.WEALTHY}: {complex_wealthy_wtp :.2f} ")


    parameter_column.append(TableFields.FIELD_DUE_PENALTY)
    tardiness_fees: list[float] = json_data[ConfigurationKeys.DUE_PENALTIES]
    simple_column.append(f"{tardiness_fees[JobNames.NAME_2_IDX[JobNames.SIMPLE]] :.2f}")
    complex_column.append(f"{tardiness_fees[JobNames.NAME_2_IDX[JobNames.COMPLEX]] :.2f}")

    parameter_column.append(TableFields.FIELD_DECLINE_COST)
    decline_penalty: list[float] = json_data[ConfigurationKeys.DECLINE_COSTS]
    simple_column.append(f"{decline_penalty[JobNames.NAME_2_IDX[JobNames.SIMPLE]] :.2f}")
    complex_column.append(f"{decline_penalty[JobNames.NAME_2_IDX[JobNames.COMPLEX]] :.2f}")
 
 
    building_dict[TableFields.COLUMN_PARAMETER] = parameter_column
    building_dict[JobNames.SIMPLE.capitalize()] = simple_column
    building_dict[JobNames.COMPLEX.capitalize()] = complex_column
    return pd.DataFrame.from_dict(building_dict)
 

def form_configuration_tables(json_path: str) -> ConfigurationTables:
    raise NotImplementedError("Needs implementation.")
    json_data: dict[str, any]
    file_json: TextIO
    with open(json_path, 'r') as file_json:
        json_data = json.load(file_json)
    response: ConfigurationTables = ConfigurationTables()
    response.job_proba_table = form_job_proba_table(
        json_data[ConfigurationKeys.JOB_TYPE_PROBA])
    response.tier_proba_table = form_tier_proba_table(
        json_data[ConfigurationKeys.TIER_PROBA])
    response.common_table = form_common_table(json_data)
    response.main_table = form_main_table(json_data) 
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


