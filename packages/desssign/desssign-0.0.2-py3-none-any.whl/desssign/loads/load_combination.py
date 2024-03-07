from __future__ import annotations

from typing import TYPE_CHECKING

from framesss.pre.cases import LoadCombination

if TYPE_CHECKING:
    from desssign.loads.load_case import DesignLoadCase


class DesignLoadCombination(LoadCombination):
    def __init__(
        self,
        label: str,
        load_cases: dict[DesignLoadCase, float],
        combination_key: str,
    ) -> None:
        super().__init__(label, load_cases)  # type: ignore[arg-type]
        self.combination_key = combination_key
