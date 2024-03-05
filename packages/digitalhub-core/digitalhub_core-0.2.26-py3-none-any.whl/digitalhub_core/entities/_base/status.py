"""
Status class module.
"""
from __future__ import annotations

from enum import Enum

from digitalhub_core.entities._base.base import ModelObj


class State(Enum):
    """
    State enumeration.
    """

    BUILT = "BUILT"
    COMPLETED = "COMPLETED"
    CREATED = "CREATED"
    ERROR = "ERROR"
    IDLE = "IDLE"
    PENDING = "PENDING"
    READY = "READY"
    RUNNING = "RUNNING"
    STOP = "STOP"


class Status(ModelObj):
    """
    Base Status class.
    The status class contains information about the state of an entity,
    for example, the state of a RUNNING run, and eventual error message.
    """

    def __init__(self, state: str, message: str | None = None) -> None:
        """
        Constructor.

        Parameters
        ----------
        state : str
            The state of the entity.
        message : str
            Error message.
        """
        self.state = state
        self.message = message

    @classmethod
    def from_dict(cls, obj: dict) -> "Status":
        """
        Return entity statusification object from dictionary.

        Parameters
        ----------
        obj : dict
            A dictionary containing the attributes of the entity statusification.

        Returns
        -------
        EntityStatus
            An entity statusification object.
        """
        return cls(**obj)


class StatusRegistry(dict):
    """
    A class representing the registry of entity statusifications.
    """

    def register(self, kind: str, module: str, status_class: str) -> None:
        """
        Register an entity statusification.

        Parameters
        ----------
        kind : str
            The kind of the entity.
        module : str
            The module name of the entity statusification.
        status_class : str
            The class name of the entity statusification.

        Returns
        -------
        None
        """
        self[kind] = {"module": module, "status_class": status_class}
