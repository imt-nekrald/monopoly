from typing import TextIO
from collections import OrderedDict

import os
import json

import pandas as pd

from dual.constants import JobNames
from dual.constants import CustomerNames
from dual.constants import MachineNames
from dual.constants import ConfigurationKeys
from dual.constants import TableFields
from dual.constants import TableNames


class ConfigurationTables:
    def __init__(self) -> None:
        self.main_table: pd.DataFrame | None = None
        self.common_table: pd.DataFrame | None = None
        self.job_proba_table: pd.DataFrame | None = None
        self.tier_proba_table: pd.DataFrame | None = None


def form_result_table(json_path: str) -> pd.DataFrame:
    data: list[dict[str, float]] = list()
    file_json: TextIO
    with open(json_path, 'r') as file_json:
        data = json.load(file_json)

    lenth_column: list[int] = list()
    dynamic_column: list[float] = list()
    static_column: list[float] = list()
    constant_column: list[float] = list()

    MIN_HORIZON_LENGTH: int = 3
    entry: dict[str, any]
    for entry in data:
        horizon_length: int = int(entry["horizon-length"])
        if horizon_length < MIN_HORIZON_LENGTH:
            continue
        lenth_column.append(str(horizon_length))
        dynamic_revenue: float = float(entry["dynamic-revenue"])
        dynamic_column.append(f"{dynamic_revenue:.1f}")
        if "static-revenue" in entry:
            static_revenue: float = float(entry["static-revenue"])
            static_column.append(f"{static_revenue:.1f}")
        else:
            static_column.append("N.A.")
        constant_revenue: float = float(entry["constant-revenue"])
        constant_column.append(constant_revenue)

    table: pd.DataFrame = pd.DataFrame.from_dict(
        OrderedDict({
            "Horizon": lenth_column,
            "Dynamic": dynamic_column,
            "Static": static_column,
            "Constant": constant_column
        }))
    return table.transpose()


def form_job_proba_table(list_data: list[list[float]]) -> pd.DataFrame:   
    table_dict: dict[str, list[any]] = OrderedDict()
    period_column: list[int] = list()
    simple_column: list[str] = list()
    complex_column: list[str] = list()

    idx_simple: int = JobNames.NAME_2_IDX[JobNames.SIMPLE]
    idx_complex: int = JobNames.NAME_2_IDX[JobNames.COMPLEX]
    for idx_period in range(len(list_data)):
        period_column.append(idx_period + 1)
        simple_column.append(f"{list_data[idx_period][idx_simple] :.1f}")
        complex_column.append(f"{list_data[idx_period][idx_complex] :.1f}")

    table_dict[TableFields.COLUMN_PERIOD] = period_column
    table_dict[JobNames.SIMPLE.capitalize()] = simple_column
    table_dict[JobNames.COMPLEX.capitalize()] = complex_column
    return pd.DataFrame.from_dict(table_dict)


def form_tier_proba_table(list_data: list[list[float]]) -> pd.DataFrame:   
    table_dict: dict[str, list[any]] = OrderedDict()
    period_column: list[int] = list()
    regular_column: list[str] = list()
    wealthy_column: list[str] = list()

    idx_regular: int = CustomerNames.NAME_2_IDX[CustomerNames.REGULAR]
    idx_wealthy: int = CustomerNames.NAME_2_IDX[CustomerNames.WEALTHY]
    for idx_period in range(len(list_data)):
        period_column.append(idx_period + 1)
        regular_column.append(f"{list_data[idx_period][idx_regular] :.1f}")
        wealthy_column.append(f"{list_data[idx_period][idx_wealthy] :.1f}")

    table_dict[TableFields.COLUMN_PERIOD] = period_column
    table_dict[CustomerNames.REGULAR.capitalize()] = regular_column
    table_dict[CustomerNames.WEALTHY.capitalize()] = wealthy_column
    return pd.DataFrame.from_dict(table_dict)


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
    simple_column.append(f"{MachineNames.FAST} : {simple_fast_duration}, " 
                         + f"{MachineNames.STANDARD} : {simple_std_duration} ")
    complex_durations: list[int] = json_data[ConfigurationKeys.JOB_DURATIONS
                                             ][JobNames.NAME_2_IDX[JobNames.COMPLEX]]
    complex_fast_duration: int = complex_durations[MachineNames.NAME_2_IDX[MachineNames.FAST]]
    complex_std_duration: int = complex_durations[MachineNames.NAME_2_IDX[MachineNames.FAST]]
    complex_column.append(f"{MachineNames.FAST} : {complex_fast_duration}, "  
                          + f"{MachineNames.STANDARD} : {complex_std_duration} ")
    
    parameter_column.append(TableFields.FIELD_DELIVERY_DURATIONS)
    simple_delivery: list[int] = json_data[
        ConfigurationKeys.DELIVERY_DURATIONS][JobNames.NAME_2_IDX[JobNames.SIMPLE]]
    simple_fast_delivery: int = simple_delivery[MachineNames.NAME_2_IDX[MachineNames.FAST]]
    simple_std_delivery: int = simple_delivery[MachineNames.NAME_2_IDX[MachineNames.FAST]]
    simple_column.append(f"{MachineNames.FAST} : {simple_fast_delivery}, " 
                         + f"{MachineNames.STANDARD} : {simple_std_delivery} ")
    complex_delivery: list[int] = json_data[ConfigurationKeys.DELIVERY_DURATIONS
                                             ][JobNames.NAME_2_IDX[JobNames.COMPLEX]]
    complex_fast_delivery: int = complex_delivery[MachineNames.NAME_2_IDX[MachineNames.FAST]]
    complex_std_delivery: int = complex_delivery[MachineNames.NAME_2_IDX[MachineNames.FAST]]
    complex_column.append(f"{MachineNames.FAST} : {complex_fast_delivery}, "  
                          + f"{MachineNames.STANDARD} : {complex_std_delivery} ")
    
    parameter_column.append(TableFields.FIELD_RELEASE_DURATIONS)
    release_durations: list[int] = json_data[ConfigurationKeys.RELEASE_DURATIONS]
    simple_column.append(str(release_durations[JobNames.NAME_2_IDX[JobNames.SIMPLE]]))
    complex_column.append(str(release_durations[JobNames.NAME_2_IDX[JobNames.COMPLEX]]))
    parameter_column.append(TableFields.FIELD_DUE_DURATIONS)
    due_durations: list[int] = json_data[ConfigurationKeys.DUE_DURATIONS]
    simple_column.append(str(due_durations[JobNames.NAME_2_IDX[JobNames.SIMPLE]]))
    complex_column.append(str(due_durations[JobNames.NAME_2_IDX[JobNames.COMPLEX]]))
 
    parameter_column.append(TableFields.FIELD_WTP)
    simple_wtp: list[float] = json_data[ConfigurationKeys.WILLINGNESS_TO_PAY
                                      ][JobNames.NAME_2_IDX[JobNames.SIMPLE]]
    simple_regular_wtp: float = simple_wtp[CustomerNames.NAME_2_IDX[CustomerNames.REGULAR]]
    simple_wealthy_wtp: float = simple_wtp[CustomerNames.NAME_2_IDX[CustomerNames.WEALTHY]]
    simple_column.append(f"{CustomerNames.REGULAR}: {simple_regular_wtp :.1f}, " 
                         + f"{CustomerNames.WEALTHY}: {simple_wealthy_wtp :.1f} ")
    complex_wtp: list[float] = json_data[ConfigurationKeys.WILLINGNESS_TO_PAY
                                       ][JobNames.NAME_2_IDX[JobNames.COMPLEX]]
    complex_regular_wtp: float = complex_wtp[CustomerNames.NAME_2_IDX[CustomerNames.REGULAR]]
    complex_wealthy_wtp: float = complex_wtp[CustomerNames.NAME_2_IDX[CustomerNames.WEALTHY]]
    complex_column.append(f"{CustomerNames.REGULAR}: {complex_regular_wtp :.1f}, " 
                         + f"{CustomerNames.WEALTHY}: {complex_wealthy_wtp :.1f} ")


    parameter_column.append(TableFields.FIELD_DUE_PENALTY)
    tardiness_fees: list[float] = json_data[ConfigurationKeys.DUE_PENALTIES]
    simple_column.append(f"{tardiness_fees[JobNames.NAME_2_IDX[JobNames.SIMPLE]] :.1f}")
    complex_column.append(f"{tardiness_fees[JobNames.NAME_2_IDX[JobNames.COMPLEX]] :.1f}")

    parameter_column.append(TableFields.FIELD_DECLINE_COST)
    decline_penalty: list[float] = json_data[ConfigurationKeys.DECLINE_COSTS]
    simple_column.append(f"{decline_penalty[JobNames.NAME_2_IDX[JobNames.SIMPLE]] :.1f}")
    complex_column.append(f"{decline_penalty[JobNames.NAME_2_IDX[JobNames.COMPLEX]] :.1f}")
 
 
    building_dict[TableFields.COLUMN_PARAMETER] = parameter_column
    building_dict[JobNames.SIMPLE.capitalize()] = simple_column
    building_dict[JobNames.COMPLEX.capitalize()] = complex_column
    return pd.DataFrame.from_dict(building_dict)
 

def form_configuration_tables(json_path: str) -> ConfigurationTables:
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


