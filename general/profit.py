from typing import Any
from typing import TextIO

import os
import json
from collections import OrderedDict
import pandas as pd

from general.common import ConfigurationNames
from general.common import PolicyNames
from general.common import ConceptFields
from general.common import EstimatorFields
from general.common import CallNames
from general.common import NameComponents
from general.common import str_for_interval


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

