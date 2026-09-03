import os


def str_for_interval(lhs: float, rhs: float) -> str:
    return f"[{lhs :.2f}, {rhs :.2f}]"


def float_list_to_str(input_list: list[float]) -> str:
    components: list[str] = list()
    element: float
    for element in input_list:
        components.append(f"{element :.2f}")
    return ", ".join(components)

def int_list_to_str(input_list: list[int]) -> str:
    components: list[str] = list()
    element: int
    for element in input_list:
        components.append(str(element))
    return ", ".join(components)


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

