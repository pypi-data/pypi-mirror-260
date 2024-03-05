"""
RunResults module.
"""
from __future__ import annotations

import typing

if typing.TYPE_CHECKING:
    from digitalhub_core.entities._base.entity import Entity
    from digitalhub_core.entities.artifacts.entity import Artifact


class RunResults:
    """
    A class representing a run results.
    """

    def __init__(
        self,
        artifacts: list[Artifact] | None = None,
    ) -> None:
        """
        Constructor.

        Parameters
        ----------
        artifacts : list[Artifact]
            The artifacts.
        """
        self.artifacts = artifacts

    def get_artifacts(self) -> list[Artifact]:
        """
        Get artifacts.

        Returns
        -------
        list[Artifact]
            List of artifacts.
        """
        return self.artifacts if self.artifacts is not None else []

    def get_artifact_by_key(self, key: str) -> Artifact | None:
        """
        Get artifact by key.

        Parameters
        ----------
        key : str
            Key.

        Returns
        -------
        Artifact
            Artifact.
        """
        for artifact in self.get_artifacts():
            if artifact.name == key:
                return artifact
        return None

    def __repr__(self) -> str:
        return str(self.__dict__)


def get_entity_info(entity: Entity, entity_type: str) -> dict:
    """
    Get the information of an entity.

    Parameters
    ----------
    entity : entity
        The entity object.
    entity_type : str
        The type of the entity.

    Returns
    -------
    dict
        The information of the entity.
    """
    return {
        "id": f"store://{entity.project}/{entity_type}/{entity.kind}/{entity.name}:{entity.id}",
        "name": entity.name,
    }
