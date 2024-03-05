"""
Run base specification module.
"""
from __future__ import annotations

from digitalhub_core.entities._base.spec import Spec, SpecParams


class RunSpec(Spec):
    """Run specification."""

    def __init__(
        self,
        task: str,
        task_id: str,
        inputs: dict | None = None,
        outputs: dict | None = None,
        parameters: dict | None = None,
        local_execution: bool = False,
        **kwargs,
    ) -> None:
        """
        Constructor.

        Parameters
        ----------
        task : str
            The task associated with the run.
        task_id : str
            The task id associated with the run.
        inputs : dict
            The inputs of the run.
        outputs : dict
            The outputs of the run.
        parameters : dict
            The parameters of the run.
        local_execution : bool
            Flag to indicate if the run will be executed locally
        **kwargs
            Keywords arguments.
        """
        self.task = task
        self.task_id = task_id
        self.inputs = inputs if inputs is not None else {}
        self.outputs = outputs if outputs is not None else {}
        self.parameters = parameters if parameters is not None else {}
        self.local_execution = local_execution

        self._any_setter(**kwargs)


class RunParams(SpecParams):
    """
    Run parameters.
    """

    task: str = None
    """The task string associated with the run."""

    task_id: str = None
    """The task id associated with the run."""

    inputs: dict = None
    """List of input dataitems and artifacts names."""

    outputs: dict = None
    """List of output dataitems and artifacts names."""

    parameters: dict = None
    """Parameters to be used in the run."""

    local_execution: bool = False
    """Flag to indicate if the run will be executed locally."""
