from framesss.enums import CaseInsensitiveStrEnum


class LoadBehavior(CaseInsensitiveStrEnum):
    UNFAVOURABLE = "unfavourable"
    FAVOURABLE = "favourable"


class LoadType(CaseInsensitiveStrEnum):
    """Enumeration of possible type of action."""

    PERMANENT = "permanent"
    VARIABLE = "variable"
    ACCIDENTAL = "accidental"


class LimitState(CaseInsensitiveStrEnum):
    """
    Enumeration of limit states.

    :cvar ULS: Ultimate limit state.
    :cvar SLS: Serviceability limit state.
    """

    ULS = "uls"
    SLS = "sls"


class UltimateLimitStates(CaseInsensitiveStrEnum):
    """Enumeration of ultimate limit states."""

    EQU = "equ"
    STR = "str"
    GEO = "geo"
    FAT = "fat"
    UPL = "upl"
    HYD = "hyd"


class ULSCombination(CaseInsensitiveStrEnum):
    """
    Enumeration of ultimate limit state combinations according to EN 1990.

    :cvar BASIC: Basic combination according to equation 6.10 of EN 1990.
    :cvar ALTERNATIVE: Alternative combinations according to equations 6.10a and 6.10b of EN 1990.
                       In this case, two variants of the combinations are considered in calculations,
                       one with reduced constant load cases and the other with reduced principal
                       variable load cases.
    :cvar ACCIDENTAL: Accidental combinations according to equations 6.11 of EN 1990.
    """

    BASIC = "basic"
    ALTERNATIVE = "alternative"
    ACCIDENTAL = "accidental"


class SLSCombination(CaseInsensitiveStrEnum):
    """
    Enumeration of serviceability limit state combinations according to EN 1990.

    :cvar CHARACTERISTIC: Combination according to equations 6.14 of EN 1990.
    :cvar FREQUENT: Combination according to equation 6.15 of EN 1990.
    :cvar QUASIPERMANENT: Combination according to equation 6.16 of EN 1990.
    """

    CHARACTERISTIC = "characteristic"
    FREQUENT = "frequent"
    QUASIPERMANENT = "quasipermanent"


class VariableCategory(CaseInsensitiveStrEnum):
    """Enumeration of possible variable loads."""

    CATEGORY_A = "category a"
    CATEGORY_B = "category b"
    CATEGORY_C = "category c"
    CATEGORY_D = "category d"
    CATEGORY_E = "category e"
    CATEGORY_F = "category f"
    CATEGORY_G = "category g"
    CATEGORY_H = "category h"
    SNOW_ABOVE_1000_M = "snow > 1000 m"
    SNOW_BELLOW_1000_M = "snow < 1000 m"
    WIND = "wind"
    TEMPERATURE = "temperature"


class LoadCaseRelation(CaseInsensitiveStrEnum):
    """
    Enumeration of possible relation of load cases.

    :cvar EXCLUSIVE: Load cases from the same load group will never act together.
    :cvar STANDARD: Load cases from the same load group may (or may not) act together.
    :cvar TOGETHER: Load cases from the same load group always act together.
    """

    EXCLUSIVE = "exclusive"
    STANDARD = "standard"
    TOGETHER = "together"
