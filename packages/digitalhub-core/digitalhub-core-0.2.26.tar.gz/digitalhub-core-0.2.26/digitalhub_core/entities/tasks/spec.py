"""
Task specification module.
"""
from __future__ import annotations

from digitalhub_core.entities._base.spec import Spec, SpecParams
from digitalhub_core.entities.tasks.models import Affinity, Env, Label, NodeSelector, Resource, Toleration, Volume


class TaskSpec(Spec):
    """Task specification."""

    def __init__(
        self,
        function: str,
        node_selector: list[NodeSelector] | None = None,
        volumes: list[Volume] | None = None,
        resources: list[Resource] | None = None,
        labels: list[Label] | None = None,
        affinity: Affinity | None = None,
        tolerations: list[Toleration] | None = None,
        env: list[Env] | None = None,
        secrets: list[str] | None = None,
        **kwargs,
    ) -> None:
        """
        Constructor.

        Parameters
        ----------
        function : str
            The function string of the task.
        node_selector : list[NodeSelector]
            The node selector of the task.
        volumes : list[Volume]
            The volumes of the task.
        resources : list[Resource]
            Kubernetes resources for the task.
        affinity : Affinity
            The affinity of the task.
        tolerations : list[Toleration]
            The tolerations of the task.
        labels : list[Label]
            The labels of the task.
        env : list[Env]
            The env variables of the task.
        secrets : list[str]
            The secrets of the task.
        """
        self.function = function
        self.node_selector = node_selector
        self.volumes = volumes
        self.resources = resources
        self.labels = labels
        self.affinity = affinity
        self.tolerations = tolerations
        self.env = env
        self.secrets = secrets

        self._any_setter(**kwargs)


class TaskParams(SpecParams):
    """
    Base task model.
    """

    function: str
    """Function string."""

    node_selector: list[NodeSelector] = None
    """Node selector."""

    volumes: list[Volume] = None
    """List of volumes."""

    resources: list[Resource] = None
    """Resources restrictions."""

    affinity: Affinity = None
    """Affinity."""

    tolerations: list[Toleration] = None
    """Tolerations."""

    labels: list[Label] = None
    """List of labels."""

    env: list[Env] = None
    """Env variables."""

    secrets: list[str] = None
    """List of secret names."""
