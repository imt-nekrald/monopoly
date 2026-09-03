from typing import Any
from typing import TextIO
import os
import json
import pandas as pd
from collections import OrderedDict

from general.common import ConfigurationNames
from general.common import NameComponents
from general.common import float_list_to_str
from general.common import int_list_to_str


class OrderInputFields:
    INPUT_ORDER_TYPES: str = 'order-types'
    INPUT_COMPATIBLE_MACHINES: str = 'compatible-machines'
    INPUT_ORDER_SIZE: str = 'count'
    INPUT_RELEASE_TERM: str = 'release-term'
    INPUT_DUE_TERM: str = 'due-term'
    INPUT_TARINESS_FEE: str = 'tardiness-penalty'
    INPUT_DECLINE_PENALTY = 'decline-penalty'
    INPUT_LINEAR_SENSITIVITY = 'linear-sensitivity'
    INPUT_PROCESSING_TERM: str = 'duration-per-machine'
    INPUT_DELIVERY_TERM: str = 'delivery-per-machine'
    INPUT_NAME: str = 'type-name'
    INPUT_INDEX: str = 'idx-type'
    INPUT_PRICE_RANGES: str = 'price-ranges'
    INPUT_PROBABILITIES: str = 'period-order-probability'



class OrderTableRows:
    ROW_ORDER_SIZE: str = 'Order size'
    ROW_RELEASE_TERM: str = 'Due term'
    ROW_DUE_TERM: str = 'Due term'
    ROW_COMPATIBLE_MACHINES: str = 'Compatible machines'
    ROW_DELIVERY_PER_MACHINE: str = 'Delivery per machine'
    ROW_PROCESSING_PER_MACHINE: str = 'Processing per machine'
    ROW_TARDINESS_FEE: str = 'Tardiness fee'
    ROW_DECLINE_PENALTY: str = 'Decline penalty'
    ROW_SENSITIVITY: str = 'Linear WTP sensitivity'
    ROW_PRICES: str = 'Prices'
    ROW_PROBABILITIES: str = 'Probability'


class OrderTableColumns:
    COLUMN_PARAMETERS: str = 'Parameter'


def build_order_table(directory_root: str) -> pd.DataFrame:
    build_dict: dict[str, list[str]] = OrderedDict()
    build_dict[OrderTableColumns.COLUMN_PARAMETERS] = [
        OrderTableRows.ROW_ORDER_SIZE,
        OrderTableRows.ROW_RELEASE_TERM, 
        OrderTableRows.ROW_DUE_TERM,
        OrderTableRows.ROW_COMPATIBLE_MACHINES, 
        OrderTableRows.ROW_PROCESSING_PER_MACHINE, 
        OrderTableRows.ROW_DELIVERY_PER_MACHINE,
        OrderTableRows.ROW_TARDINESS_FEE,
        OrderTableRows.ROW_DECLINE_PENALTY, 
        OrderTableRows.ROW_SENSITIVITY,
        OrderTableRows.ROW_PRICES, 
        OrderTableRows.ROW_PROBABILITIES,
    ]
    configuration: str
    for configuration in ConfigurationNames.OPTIONS:
        setting_json_path: str = os.path.join(directory_root, 
            NameComponents.CONFIGURATION_TPL.format(configuration))
        if os.path.isfile(setting_json_path):        
            in_json: TextIO
            with open(setting_json_path, "r") as in_json:
                dict_setting: dict[str, Any] = json.load(in_json)
                order_dict: dict[str, Any]; idx: int
                for idx, order_dict in enumerate(
                        dict_setting[OrderInputFields.INPUT_ORDER_TYPES]):
                    order_name: str = order_dict[OrderInputFields.INPUT_NAME]
                    order_size: int = order_dict[OrderInputFields.INPUT_ORDER_SIZE]
                    release_term: float = order_dict[OrderInputFields.INPUT_RELEASE_TERM]
                    due_term: float = order_dict[OrderInputFields.INPUT_DUE_TERM]
                    compatible_machines: list[int] = order_dict[OrderInputFields.INPUT_COMPATIBLE_MACHINES]
                    delivery: list[float] = order_dict[OrderInputFields.INPUT_DELIVERY_TERM]
                    processing: list[float] = order_dict[OrderInputFields.INPUT_PROCESSING_TERM]
                    tardiness_fee: float = order_dict[OrderInputFields.INPUT_TARINESS_FEE]
                    decline_penalty: float = order_dict[OrderInputFields.INPUT_DECLINE_PENALTY]
                    sensitivity: float = order_dict[OrderInputFields.INPUT_LINEAR_SENSITIVITY]
                    prices: list[float] = dict_setting[OrderInputFields.INPUT_PRICE_RANGES][0][idx]
                    probability: float= dict_setting[OrderInputFields.INPUT_PRICE_RANGES][0][idx]
                    order_column: list[str] = [
                        str(order_size), f"{release_term :.2f}", f"{due_term :.2f}",
                        int_list_to_str(compatible_machines), float_list_to_str(processing), 
                        float_list_to_str(delivery), f"{tardiness_fee :.2f}", 
                        f"{decline_penalty :.2f}", f"{sensitivity :.2f}",
                        float_list_to_str(prices), f"{probability :.2f}"
                    ] 
                    build_dict[order_name] = order_column

    return pd.DataFrame.from_dict(build_dict)
                    
