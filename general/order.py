from typing import Any
from typing import TextIO
import os
import json
import pandas as pd


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



class OrderTableColumns:
    COLUMN_DESCRIPTION: str=  'Description'
    COLUMN_ORDER_SIZE: str = 'Order size'
    COLUMN_RELEASE_TERM: str = 'Due term'
    COLUMN_DUE_TERM: str = 'Due term'
    COLUMN_COMPATIBLE_MACHINES: str = 'Compatible machines'
    COLUMN_DELIVERY_PER_MACHINE: str = 'Delivery per machine'
    COLUMN_PROCESSING_PER_MACHINE: str = 'Processing per machine'
    COLUMN_SENSITIVITY: str = 'Linear WTP sensitivity'
    COLUMN_TARDINESS_FEE: str = 'Tardiness fee'
    COLUMN_DECLINE_PENALTY: str = 'Decline penalty'
    COLUMN_PRICES: str = 'Prices'
    COLUMN_PROBABILITIES: str = 'Probabilities'





def build_order_table(directory_root: str) -> pd.DataFrame:
    raise NotImplementedError("Needs implementation.")


