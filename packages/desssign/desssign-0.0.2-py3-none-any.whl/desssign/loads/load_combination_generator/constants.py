from desssign.loads.enums import LoadBehavior
from desssign.loads.enums import LoadType
from desssign.loads.enums import VariableCategory

PSI_FACTORS = {
    VariableCategory.CATEGORY_A: {
        "psi_0": 0.7,
        "psi_1": 0.5,
        "psi_2": 0.3,
    },
    VariableCategory.CATEGORY_B: {
        "psi_0": 0.7,
        "psi_1": 0.5,
        "psi_2": 0.3,
    },
    VariableCategory.CATEGORY_C: {
        "psi_0": 0.7,
        "psi_1": 0.7,
        "psi_2": 0.6,
    },
    VariableCategory.CATEGORY_D: {
        "psi_0": 0.7,
        "psi_1": 0.7,
        "psi_2": 0.6,
    },
    VariableCategory.CATEGORY_E: {
        "psi_0": 1.0,
        "psi_1": 0.9,
        "psi_2": 0.8,
    },
    VariableCategory.CATEGORY_F: {
        "psi_0": 0.7,
        "psi_1": 0.7,
        "psi_2": 0.6,
    },
    VariableCategory.CATEGORY_G: {
        "psi_0": 0.7,
        "psi_1": 0.5,
        "psi_2": 0.3,
    },
    VariableCategory.CATEGORY_H: {
        "psi_0": 0.0,
        "psi_1": 0.0,
        "psi_2": 0.0,
    },
    VariableCategory.SNOW_ABOVE_1000_M: {
        "psi_0": 0.7,
        "psi_1": 0.5,
        "psi_2": 0.2,
    },
    VariableCategory.SNOW_BELLOW_1000_M: {
        "psi_0": 0.5,
        "psi_1": 0.2,
        "psi_2": 0.0,
    },
    VariableCategory.WIND: {
        "psi_0": 0.6,
        "psi_1": 0.2,
        "psi_2": 0.0,
    },
    VariableCategory.TEMPERATURE: {
        "psi_0": 0.6,
        "psi_1": 0.5,
        "psi_2": 0.0,
    },
}


GAMMA_VALUES = {
    "Set B": {
        LoadType.PERMANENT: {
            LoadBehavior.FAVOURABLE: 1.0,
            LoadBehavior.UNFAVOURABLE: 1.35,
        },
        LoadType.VARIABLE: {
            LoadBehavior.FAVOURABLE: 0.0,
            LoadBehavior.UNFAVOURABLE: 1.5,
        },
    },
    "Set C": {
        LoadType.PERMANENT: {
            LoadBehavior.FAVOURABLE: 1.0,
            LoadBehavior.UNFAVOURABLE: 1.0,
        },
        LoadType.VARIABLE: {
            LoadBehavior.FAVOURABLE: 0.0,
            LoadBehavior.UNFAVOURABLE: 1.3,
        },
    },
}

XI = 0.85
