class JobNames:
    COMPLEX: str = 'complex'
    SIMPLE: str = 'simple'

    IDX_2_NAME: list[str] = [COMPLEX, SIMPLE]
    NAME_2_IDX: dict[str, int] = {COMPLEX: 0, SIMPLE: 1}


class CustomerNames:
    REGULAR: str = 'regular'
    WEALTHY: str=  'wealthy'

    IDX_2_NAME: list[str] = [REGULAR, WEALTHY]
    NAME_2_IDX: dict[str, int]  = {REGULAR: 0, WEALTHY: 1}


class MachineNames:
    FAST: str = 'fast'
    STANDARD: str = 'standard'
    
    IDX_2_NAME: list[str] = [FAST, STANDARD]
    NAME_2_IDX: dict[str, int] = {FAST: 0, STANDARD: 1}


class ConfigurationKeys:
    N_MACHINES: str = "n-machines"
    MAX_HORIZON_DP: str = "max-horizon-dp"
    MAX_HORIZON_STATIC: str = "max-horizon-static"
    UPPER_WTP: str = "upper-wtp"

    JOB_DURATIONS: str = "job-durations"
    DELIVERY_DURATIONS: str = "delivery-durations"
    RELEASE_DURATIONS: str = "release-durations"
    DUE_DURATIONS: str = "due-durations"
    WILLINGNESS_TO_PAY: str = "willingness-to-pay"
    DUE_PENALTIES: str = "due-penalties"
    DECLINE_COSTS: str = "decline-costs"
    JOB_TYPE_PROBA: str = "job-type-proba"
    TIER_PROBA: str = "tier-proba"


class TableFields:
    COLUMN_PARAMETER: str = 'Parameter'
    COLUMN_VALUE: str = 'Value'
    COLUMN_PERIOD: str = 'Period'

    FIELD_N_MACHINES: str = 'Number of machines'
    FIELD_MAX_HORIZON_DYNAMIC: str = 'Maximal horizon for profile dynamic'
    FIELD_MAX_HORIZON_STATIC: str = 'Maximal horizon for static search'
    FIELD_UPPER_WTP: str = "Upper bound on WTP"

    FIELD_JOB_DURATIONS: str = 'Processing terms per machine'
    FIELD_DELIVERY_DURATIONS: str = 'Delivery durations per machine'
    FIELD_RELEASE_DURATIONS: str = 'Release terms'
    FIELD_DUE_DURATIONS:  str = 'Due terms'
    FIELD_WTP: str = 'Willingness to pay'
    FIELD_DUE_PENALTY: str = 'Tardiness fee'
    FIELD_DECLINE_COST: str = 'Decline penalty'


class TableNames:
    RESULTS_EXCEL: str = 'result-table.xlsx'
    MAIN_CONFIG_EXCEL: str = 'main-config-table.xlsx'
    COMMON_CONFIG_EXCEL: str = 'common-config-table.xlsx'
    PROBA_JOB_TYPE_CONFIG_EXCEL: str = 'job-type-proba-config.xlsx'
    PROBA_TIER_TYPE_CONFIG_EXCEL: str = 'tier-type-proba-config.xlsx'

    RESULTS_LATEX: str = 'result-table.tex'
    MAIN_CONFIG_LATEX: str = 'main-config-table.tex'
    COMMON_CONFIG_LATEX: str = 'common-config-table.tex'
    PROBA_JOB_TYPE_CONFIG_LATEX: str = 'job-type-proba-config.tex'
    PROBA_TIER_TYPE_CONFIG_LATEX: str = 'tier-type-proba-config.tex'



