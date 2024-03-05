"""
RunStatus class module.
"""
from __future__ import annotations

from digitalhub_core.entities._base.status import Status


class RunStatus(Status):
    """
    Status class for run entities.
    """

    def get_results(self) -> list[object]:
        """
        Get run objects results. If no results are available.
        """
        return []
