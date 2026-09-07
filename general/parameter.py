from inspect import Parameter
from typing import Any
from typing import TextIO
import os
import json
from collections import OrderedDict

import pandas as pd

from general.common import ConfigurationNames
from general.common import NameComponents


class ParameterInputFields:
    N_EVALUATION_SAMPLES: str = "n-evaluation-samples"
    N_ROLLOUT_TRAJECTORIES: str = "n-rollout-trajectories"
    GENETIC: str = "genetic"
    N_GENETIC_ITERATIONS: str = "n-genetic-iterations"
    N_EVALUATION_TRAJECTORIES: str = "n-evaluation-trajectories"
    N_FAST_TRAJECTORIES: str = "n-fast-trajectories"
    N_MUTATION_PLACES: str = "n-mutation-places"
    RECOMBINATION_PROBA: str = "recombination-proba"
    SELECTION_SIZE: str = "selection-size"
    ESTIMATOR_TIME_LIMIT: str = "estimator-time-limit"


class ParameterTableColumnNames:
    PARAMETER: str = 'Parameter'


class ParameterTableRowNames:
    ROW_EVALUATION_SIZE: str = "Number of trajectories at evaluation"
    ROW_ROLLOUT_SIZE: str = "Number of trajectories for rollout estimation"
    ROW_N_GENETIC_ITERATIONS: str = "Number of genetic iterations"
    ROW_N_EVALUATION_TRAJECTORIES: str = "Number of trajectories for final genetic estimation"
    ROW_N_FAST_TRAJECTORIES: str = "Number of trajectories for intermediate genetic estimation"
    ROW_N_MUTATION_PLACES: str = "Number of mutation places in genetic"
    ROW_RECOMBINATION_PROBA: str = "Probability at recombination in genetic"
    ROW_SELECTION_SIZE: str = "Number of policies after selection in genetic"
    ROW_ESTIMATOR_TL: str = "Gurobi MIP Time Limit (sec.)"


def build_parameter_table(directory_root: str) -> pd.DataFrame:
    build_dict: dict[str, list[str]] = OrderedDict()
    build_dict[ParameterTableColumnNames.PARAMETER] = [
        ParameterTableRowNames.ROW_EVALUATION_SIZE,
        ParameterTableRowNames.ROW_ROLLOUT_SIZE,
        ParameterTableRowNames.ROW_N_GENETIC_ITERATIONS,
        ParameterTableRowNames.ROW_N_EVALUATION_TRAJECTORIES,
        ParameterTableRowNames.ROW_N_FAST_TRAJECTORIES,
        ParameterTableRowNames.ROW_N_MUTATION_PLACES,
        ParameterTableRowNames.ROW_RECOMBINATION_PROBA,
        ParameterTableRowNames.ROW_SELECTION_SIZE,
        ParameterTableRowNames.ROW_ESTIMATOR_TL,
    ]
    configuration: str
    for configuration in ConfigurationNames.OPTIONS:
        parameters_json_path: str = os.path.join(directory_root, 
            NameComponents.PARAMETERS_TPL.format(configuration))
        if os.path.isfile(parameters_json_path):        
            dict_parameters: dict[str, Any] = dict()
            in_json: TextIO
            with open(parameters_json_path, "r") as in_json:
                dict_parameters = json.load(in_json)
                evaluation_size: int = dict_parameters[ParameterInputFields.N_EVALUATION_SAMPLES]
                rollout_size: int = dict_parameters[ParameterInputFields.N_ROLLOUT_TRAJECTORIES]
                genetic_parameters: dict[str, Any] = dict_parameters[ParameterInputFields.GENETIC]
                genetic_iterations: int = genetic_parameters[ParameterInputFields.N_GENETIC_ITERATIONS]
                genetic_eval_size: int = genetic_parameters[ParameterInputFields.N_EVALUATION_TRAJECTORIES]
                genetic_fast_size: int = genetic_parameters[ParameterInputFields.N_FAST_TRAJECTORIES]
                mutation_places: int = genetic_parameters[ParameterInputFields.N_MUTATION_PLACES]
                recombination_proba: float = genetic_parameters[ParameterInputFields.RECOMBINATION_PROBA]
                selection_size: int = genetic_parameters[ParameterInputFields.SELECTION_SIZE]
                estimator_tl: int = dict_parameters[ParameterInputFields.ESTIMATOR_TIME_LIMIT]
                build_dict[configuration.capitalize()] = [
                    str(evaluation_size), str(rollout_size), str(genetic_iterations), 
                    str(genetic_eval_size), str(genetic_fast_size), str(mutation_places), 
                    f"{recombination_proba :.2f}", str(selection_size), str(estimator_tl)
                ]
    return pd.DataFrame.from_dict(build_dict)

