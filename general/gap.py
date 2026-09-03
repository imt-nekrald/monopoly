from typing import Any
from typing import TextIO
import math
import os
import json
from collections import OrderedDict
import pandas as pd
import numpy as np

from general.common import str_for_interval
from general.common import ConfigurationNames
from general.common import NameComponents
from general.common import PolicyNames
from general.common import EstimatorFields
from general.common import CallNames
from general.common import ConceptFields


class GapTableRows:
    STATIC_ROLLOUT_GAP: str = 'Static-Rollout Gap'
    ROLLOUT_NESTED_GAP: str = 'Rollout-Nested Gap'
    NESTED_BOUND_GAP: str = 'Nested-Gurobi Bound Gap'
    GUROBI_MIP_GAP: str = 'Gurobi MIP-Bound Gap'


class GapTableColumns:
    SETTING: str = 'Setting'
    GAP_TYPE: str = 'Gap Type'
    GAP_VALUE: str = 'Gap Value'


def form_str_gap(lhs_values: list[float], rhs_values: list[float]) -> str:
    gap_values: list[float] = list()
    lhs_item: float; rhs_item: float
    epsilon: float = 1e-5
    for lhs_item, rhs_item in zip(lhs_values, rhs_values):
        gap_values.append((rhs_item - lhs_item) / (abs(lhs_item) + epsilon))
    assert len(lhs_values) == len(rhs_values)
    size: int = len(lhs_values)
    average: float = np.mean(gap_values)
    std: float = np.std(gap_values)
    return str_for_interval(
        average - std * 1.96 / math.sqrt(size), 
        average + std * 1.96 / math.sqrt(size))


def build_gap_table(directory_root: str) -> pd.DataFrame:
    build_dict: dict[str, list[str]] = OrderedDict()
    build_dict[GapTableColumns.SETTING] = list()
    build_dict[GapTableColumns.GAP_TYPE] = list()
    build_dict[GapTableColumns.GAP_VALUE] = list()
    configuration: str
    for configuration in ConfigurationNames.OPTIONS:
        evaluation_json_path: str = os.path.join(
            directory_root, NameComponents.EVALUATION_TPL.format(configuration))
        if os.path.isfile(evaluation_json_path):        
            dict_evaluation: dict[str, Any] = dict()
            in_json: TextIO
            with open(evaluation_json_path, "r") as in_json:
                dict_evaluation = json.load(in_json)
                static_observations: list[float] = dict_evaluation[configuration][CallNames.GENETIC][
                    PolicyNames.STATIC][EstimatorFields.OBSERVATIONS_TPL.format(ConceptFields.PROFIT)]
                rollout_observations: list[float] = dict_evaluation[configuration][CallNames.GENETIC][
                    PolicyNames.ROLLOUT][EstimatorFields.OBSERVATIONS_TPL.format(ConceptFields.PROFIT)]
                nested_observations: list[float] = dict_evaluation[configuration][CallNames.GENETIC][
                    PolicyNames.NESTED][EstimatorFields.OBSERVATIONS_TPL.format(ConceptFields.PROFIT)]
                mip_gurobi_observations: list[float] = dict_evaluation[configuration][CallNames.GUROBI][
                    PolicyNames.ESTIMATOR][EstimatorFields.OBSERVATIONS_TPL.format(ConceptFields.PROFIT)]
                gurobi_bound_observations: list[float] = dict_evaluation[configuration][CallNames.GUROBI][
                    PolicyNames.ESTIMATOR][EstimatorFields.OBSERVATIONS_TPL.format(ConceptFields.BOUND)]
                build_dict[GapTableColumns.SETTING].append(configuration.capitalize())
                build_dict[GapTableColumns.GAP_TYPE].append(GapTableRows.STATIC_ROLLOUT_GAP)
                build_dict[GapTableColumns.GAP_VALUE].append(form_str_gap(static_observations, rollout_observations))
                build_dict[GapTableColumns.SETTING].append(configuration.capitalize())
                build_dict[GapTableColumns.GAP_TYPE].append(GapTableRows.ROLLOUT_NESTED_GAP)
                build_dict[GapTableColumns.GAP_VALUE].append(form_str_gap(rollout_observations, nested_observations))
                build_dict[GapTableColumns.SETTING].append(configuration.capitalize())
                build_dict[GapTableColumns.GAP_TYPE].append(GapTableRows.NESTED_BOUND_GAP)
                build_dict[GapTableColumns.GAP_VALUE].append(form_str_gap(nested_observations, gurobi_bound_observations))
                build_dict[GapTableColumns.SETTING].append(configuration.capitalize())
                build_dict[GapTableColumns.GAP_TYPE].append(GapTableRows.GUROBI_MIP_GAP)
                build_dict[GapTableColumns.GAP_VALUE].append(form_str_gap(mip_gurobi_observations, gurobi_bound_observations))
    return pd.DataFrame.from_dict(build_dict)


