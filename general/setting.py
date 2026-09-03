from typing import Any
from typing import TextIO
import os
import json
import pandas as pd
from collections import OrderedDict

from general.common import ConfigurationNames
from general.common import NameComponents
from general.common import float_list_to_str


class InputSettingFields:
    INPUT_N_MACHINES: str = "n-machines"
    INPUT_N_ORDER_TYPES: str = "n-order-types"
    INPUT_N_PERIODS: str = "n-periods"
    INPUT_PERIOD_DURATIONS: str = "period-duration"


class SettingTableRows:
    ROW_N_MACHINES: str = "Number of machines"
    ROW_N_ORDER_TYPES: str = "Number of order types"
    ROW_N_PERIODS: str = "Number of periods"
    ROW_PERIOD_DURATONS: str = "Period Durations"


class SettingTableColumns:
    COLUMN_PARAMETER: str = 'Parameter'


def build_setting_table(directory_root: str) -> pd.DataFrame:
    build_dict: dict[str, list[str]] = OrderedDict()
    build_dict[SettingTableColumns.COLUMN_PARAMETER] = [
        SettingTableRows.ROW_N_MACHINES, SettingTableRows.ROW_N_ORDER_TYPES,
        SettingTableRows.ROW_N_PERIODS, SettingTableRows.ROW_PERIOD_DURATIONS,
    ]
    configuration: str
    for configuration in ConfigurationNames.OPTIONS:
        setting_json_path: str = os.path.join(directory_root, 
            NameComponents.CONFIGURATION_TPL.format(configuration))
        if os.path.isfile(setting_json_path):        
            in_json: TextIO
            with open(setting_json_path, "r") as in_json:
                dict_setting: dict[str, Any] = json.load(in_json)
                n_machines: int = dict_setting[InputSettingFields.INPUT_N_MACHINES]
                n_order_types: int = dict_setting[InputSettingFields.INPUT_N_ORDER_TYPES]
                n_periods: int = dict_setting[InputSettingFields.INPUT_N_PERIODS]
                period_durations: list[float] = dict_setting[InputSettingFields.INPUT_PERIOD_DURATIONS]
                build_dict[configuration.capitalize()] = [ 
                    str(n_machines), str(n_order_types), 
                    str(n_periods), float_list_to_str(period_durations) ]
    return pd.DataFrame.from_dict(build_dict)
                
