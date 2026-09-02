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


def parse_arguments() -> argparse.Namespace:
    parser: argparse.ArgumentParser = argparse.ArgumentParser(
            description="Read information from JSONs and organize in LaTeX-compatible form.")
    parser.add_argument("--directory-root", type=str, required=True,
            help="Path to root output directory.")
    return parser.parse_args()


def str_for_interval(lhs: float, rhs: float) -> str:
    return f"[{lhs :.2f}, {rhs :.2f}]"


class NameComponents:
    PARAMETERS_TPL: str = '{}-parameters.json'
    CONFIGURATION_TPL: str = '{}-configuration.json'
    EVALUATION_TPL: str = 'evaluation-{}.json'
    JSON_EXTENSION: str = ".json"


class ConfigurationNames:
    MINIMAL: str = "minimal"
    SMALL: str = "small"
    MEDIUM: str = "medium"
    OPTIONS: list[str] = [MINIMAL, SMALL, MEDIUM]


class CallNames:
    GENETIC: str = "genetic"
    GUROBI: str = "gurobi"
    OPTIONS: list[str] = [GENETIC, GUROBI]


class PolicyNames:
    STATIC: str = 'static'
    ROLLOUT: str = 'rollout'
    NESTED: str = 'nested'
    ESTIMATOR: str = 'estimator'


class EstimatorFields:
    AVERAGE_TPL: str = 'average-{}'
    LOWER_TPL: str = 'lower-{}'
    UPPER_TPL: str = 'upper-{}'
    OBSERVATIONS_TPL: str = 'observations-'


class ConceptFields:
    GAP: str = 'gap'
    PROFIT: str = 'revenue'
    BOUND: str = 'mip-bound'


class ProfitTableColumns:
    SETTING: str = 'Setting'
    STATIC: str = 'Static'
    ROLLOUT: str = 'Rollout'
    NESTED: str = 'Nested'
    MIP_GUROBI: str = 'MIP Gurobi PI'
    UB_GUROBI: str = 'UB Gurobi PI'


def build_profit_table(directory_root: str) -> pd.DataFrame:
    build_dict: dict[str, list[str]] = OrderedDict()
    build_dict[ProfitTableColumns.SETTING] = list()
    build_dict[ProfitTableColumns.STATIC] = list()
    build_dict[ProfitTableColumns.ROLLOUT] = list()
    build_dict[ProfitTableColumns.NESTED] = list()
    build_dict[ProfitTableColumns.MIP_GUROBI] = list()
    build_dict[ProfitTableColumns.UB_GUROBI] = list()

    configuration: str
    for configuration in ConfigurationNames.OPTIONS:
        evaluation_json_path: str = os.path.join(
            directory_root, NameComponents.EVALUATION_TPL.format(configuration))
        if os.path.isfile(evaluation_json_path):        
            dict_evaluation: dict[str, Any] = dict()
            in_json: TextIO
            with open(evaluation_json_path, "r") as in_json:
                dict_evaluation = json.load(in_json)
                build_dict[ProfitTableColumns.SETTING].append(configuration.capitalize())
                lhs_static: float = dict_evaluation[configuration][CallNames.GENETIC][
                    PolicyNames.STATIC][EstimatorFields.LOWER_TPL.format(ConceptFields.PROFIT)]
                rhs_static: float = dict_evaluation[configuration][CallNames.GENETIC][
                    PolicyNames.STATIC][EstimatorFields.UPPER_TPL.format(ConceptFields.PROFIT)]
                build_dict[ProfitTableColumns.STATIC].append(
                    str_for_interval(lhs_static, rhs_static))

                lhs_rollout: float = dict_evaluation[configuration][CallNames.GENETIC][
                    PolicyNames.ROLLOUT][EstimatorFields.LOWER_TPL.format(ConceptFields.PROFIT)]
                rhs_rollout: float = dict_evaluation[configuration][CallNames.GENETIC][
                    PolicyNames.ROLLOUT][EstimatorFields.UPPER_TPL.format(ConceptFields.PROFIT)]
                build_dict[ProfitTableColumns.ROLLOUT].append(
                    str_for_interval(lhs_rollout, rhs_rollout))

                lhs_nested: float = dict_evaluation[configuration][CallNames.GENETIC][
                    PolicyNames.NESTED][EstimatorFields.LOWER_TPL.format(ConceptFields.PROFIT)]
                rhs_nested: float = dict_evaluation[configuration][CallNames.GENETIC][
                    PolicyNames.NESTED][EstimatorFields.UPPER_TPL.format(ConceptFields.PROFIT)]
                build_dict[ProfitTableColumns.NESTED].append(
                    str_for_interval(lhs_nested, rhs_nested))

                lhs_mip_gurobi: float =  dict_evaluation[configuration][CallNames.GUROBI][
                    PolicyNames.ESTIMATOR][EstimatorFields.LOWER_TPL.format(ConceptFields.PROFIT)]
                rhs_mip_gurobi: float = dict_evaluation[configuration][CallNames.GUROBI][
                    PolicyNames.ESTIMATOR][EstimatorFields.UPPER_TPL.format(ConceptFields.PROFIT)]
                build_dict[ProfitTableColumns.MIP_GUROBI].append(
                    str_for_interval(lhs_mip_gurobi, rhs_mip_gurobi))

                lhs_bound_gurobi: float = dict_evaluation[configuration][CallNames.GUROBI][
                    PolicyNames.ESTIMATOR][EstimatorFields.LOWER_TPL.format(ConceptFields.BOUND)]
                rhs_bound_gurobi: float = dict_evaluation[configuration][CallNames.GUROBI][
                    PolicyNames.ESTIMATOR][EstimatorFields.UPPER_TPL.format(ConceptFields.BOUND)]
                build_dict[ProfitTableColumns.UB_GUROBI].append(
                    str_for_interval(lhs_bound_gurobi, rhs_bound_gurobi))
    return pd.DataFrame.from_dict(build_dict)


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
    return str_for_interval(average - std * 1.96 / math.sqrt(size), average + std * 1.96 / math.sqrt(size) )


def build_gap_table(directory_root: str) -> pd.DataFrame:
    build_dict: dict[str, list[str]] = OrderedDict()
    build_dict[TimeTableColumns.SETTING] = list()
    build_dict[TimeTableColumns.GAP_TYPE] = list()
    build_dict[TimeTableColumns.GAP_VALUE] = list()
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


def build_parameter_table(directory_root: str) -> pd.DataFrame:
    raise NotImplementedError("Needs implementation.")


def build_setting_table(directory_root: str, setting_name: str) -> pd.DataFrame:
    configuration_json_path: str = os.path.join(
        directory_root, NameComponents.CONFIGURATION_TPL.format(setting_name))
    in_json: TextIO
    with open(configuration_json_path, "r") as in_json:
        dict_configuration = json.load(in_json)

    raise NotImplementedError("Needs implementation.")


if __name__ == '__main__':
    args: argparse.Namespace = parse_arguments()
    directory_path: str = os.path.abspath(args.directory_root)
    profit_df: pd.DataFrame = build_profit_table(directory_path)
    time_df: pd.DataFrame = build_time_table(directory_path)
    gap_df: pd.DataFrame = build_gap_table(directory_path)
    

