from typing import TextIO
from typing import Any
import json
import os
import pandas as pd
from collections import OrderedDict

from general.common import ConfigurationNames
from general.common import NameComponents
from general.common import CallNames
from general.common import PolicyNames


class TemporalFields:
    DURATION: str = 'duration'
    GENETIC_DURATION: str = 'genetic-duration'


class TimeTableColumns:
    SETTING: str = 'Setting'
    STATIC: str = 'Static'
    ROLLOUT: str = 'Rollout'
    NESTED: str = 'Nested'
    GUROBI: str = 'Gurobi'
 

def build_time_table(directory_root: str) -> pd.DataFrame:
    build_dict: dict[str, list[str]] = OrderedDict()
    build_dict[TimeTableColumns.SETTING] = list()
    build_dict[TimeTableColumns.STATIC] = list()
    build_dict[TimeTableColumns.ROLLOUT] = list()
    build_dict[TimeTableColumns.NESTED] = list()
    build_dict[TimeTableColumns.GUROBI] = list()
    configuration: str
    for configuration in ConfigurationNames.OPTIONS:
        evaluation_json_path: str = os.path.join(
            directory_root, NameComponents.EVALUATION_TPL.format(configuration))
        if os.path.isfile(evaluation_json_path):        
            dict_evaluation: dict[str, Any] = dict()
            in_json: TextIO
            with open(evaluation_json_path, "r") as in_json:
                dict_evaluation = json.load(in_json)
                build_dict[TimeTableColumns.SETTING].append(configuration.capitalize())
                genetic_time: float = dict_evaluation[configuration][
                    CallNames.GENETIC][TemporalFields.GENETIC_DURATION]
                static_duration: float =  dict_evaluation[configuration][
                    CallNames.GENETIC][PolicyNames.STATIC][TemporalFields.DURATION] + genetic_time
                rollout_duration: float = dict_evaluation[configuration][
                    CallNames.GENETIC][PolicyNames.ROLLOUT][TemporalFields.DURATION] + genetic_time
                nested_duration: float = dict_evaluation[configuration][
                    CallNames.GENETIC][PolicyNames.NESTED][TemporalFields.DURATION] + genetic_time
                gurobi_duration: float = dict_evaluation[configuration][
                    CallNames.GUROBI][PolicyNames.ESTIMATOR][TemporalFields.DURATION]
                build_dict[TimeTableColumns.STATIC].append(static_duration)
                build_dict[TimeTableColumns.ROLLOUT].append(rollout_duration)
                build_dict[TimeTableColumns.NESTED].append(nested_duration)
                build_dict[TimeTableColumns.GUROBI].append(gurobi_duration)
    return pd.DataFrame.from_dict(build_dict)

