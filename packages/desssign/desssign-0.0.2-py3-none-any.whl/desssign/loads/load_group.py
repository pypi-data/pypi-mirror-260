from __future__ import annotations

from itertools import combinations
from typing import TYPE_CHECKING

from desssign.loads.enums import LoadCaseRelation

if TYPE_CHECKING:
    from desssign.loads.load_case import DesignLoadCase


class LoadGroup:
    def __init__(
        self,
        load_cases: list[DesignLoadCase],
        load_case_relation: str | LoadCaseRelation = LoadCaseRelation.STANDARD,
    ) -> None:
        """
        Init the LoadGroup class.

        :param load_cases: List of :class:`DesignLoadCase` instances.
        :param load_case_relation: Relation between :class:`DesignLoadCase` instances.
                                   Possible values are ['together', 'standard', 'exclusive'].
        """
        self.load_cases = load_cases
        self.load_case_relation = LoadCaseRelation(load_case_relation)

    def __repr__(self) -> str:
        """Return a string representation of the LoadGroup object."""
        return (
            f"LoadGroup("
            f"load_cases={self.load_cases}, "
            f"load_case_relation={self.load_case_relation}"
            f")"
        )

    @property
    def number_of_load_cases(self) -> int:
        """Return the number of load cases."""
        return len(self.load_cases)

    @property
    def combinations(self) -> list[list[DesignLoadCase]]:
        """
        Generates a list of load case combinations based on the relation between load cases.

        :return: A list of lists, where each inner list represents a specific combination of `DesignLoadCase` instances.
        :raises AttributeError: If `load_case_relation` is not valid.
        """
        if self.load_case_relation == LoadCaseRelation.TOGETHER:
            return [self.load_cases]
        if self.load_case_relation == LoadCaseRelation.STANDARD:
            return [
                list(comb)
                for i in range(self.number_of_load_cases + 1)
                for comb in combinations(self.load_cases, i)
            ]
        if self.load_case_relation == LoadCaseRelation.EXCLUSIVE:
            comb = [[comb] for comb in self.load_cases]
            comb.insert(0, [])
            return comb
        else:
            raise AttributeError(
                f"Invalid load case relation: {self.load_case_relation}"
            )
