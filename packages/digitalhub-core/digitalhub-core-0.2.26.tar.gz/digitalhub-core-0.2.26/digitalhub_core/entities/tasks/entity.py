"""
Task module.
"""
from __future__ import annotations

import typing
from pathlib import Path

from digitalhub_core.context.builder import get_context
from digitalhub_core.entities._base.entity import Entity
from digitalhub_core.entities._builders.metadata import build_metadata
from digitalhub_core.entities._builders.spec import build_spec
from digitalhub_core.entities._builders.status import build_status
from digitalhub_core.entities.runs.crud import delete_run, get_run, new_run, run_from_parameters
from digitalhub_core.entities.tasks.metadata import TaskMetadata
from digitalhub_core.entities.tasks.status import TaskStatus
from digitalhub_core.utils.api import api_ctx_create, api_ctx_update_name_only
from digitalhub_core.utils.generic_utils import build_uuid, get_timestamp
from digitalhub_core.utils.io_utils import write_yaml

if typing.TYPE_CHECKING:
    from digitalhub_core.context.context import Context
    from digitalhub_core.entities.runs.entity import Run
    from digitalhub_core.entities.tasks.spec import TaskSpec


class Task(Entity):
    """
    A class representing a task.
    """

    def __init__(
        self,
        project: str,
        uuid: str,
        kind: str,
        metadata: TaskMetadata,
        spec: TaskSpec,
        status: TaskStatus,
    ) -> None:
        """
        Constructor.

        Parameters
        ----------
        project : str
            Name of the project.
        uuid : str
            UUID.
        kind : str
            Kind of the object.
        metadata : TaskMetadata
            Metadata of the object.
        spec : TaskSpec
            Specification of the object.
        status : TaskStatus
            Status of the object.
        """
        super().__init__()
        self.project = project
        self.id = uuid
        self.kind = kind
        self.metadata = metadata
        self.spec = spec
        self.status = status

        # Add attributes to be used in the to_dict method
        self._obj_attr.extend(["project", "id"])

    #############################
    #  Save / Export
    #############################

    def save(self, update: bool = False) -> dict:
        """
        Save task into backend.

        Parameters
        ----------
        update : bool
            Flag to indicate update.

        Returns
        -------
        dict
            Mapping representation of Task from backend.
        """
        obj = self.to_dict()

        if not update:
            api = api_ctx_create(self.project, "tasks")
            return self._context().create_object(obj, api)

        self.metadata.updated = obj["metadata"]["updated"] = get_timestamp()
        api = api_ctx_update_name_only(self.project, "tasks", self.id)
        return self._context().update_object(obj, api)

    def export(self, filename: str | None = None) -> None:
        """
        Export object as a YAML file.

        Parameters
        ----------
        filename : str
            Name of the export YAML file. If not specified, the default value is used.

        Returns
        -------
        None
        """
        obj = self.to_dict()
        if filename is None:
            filename = f"{self.kind}_{self.name}_{self.id}.yml"
        pth = Path(self._context().project_dir) / filename
        pth.parent.mkdir(parents=True, exist_ok=True)
        write_yaml(pth, obj)

    #############################
    #  Context
    #############################

    def _context(self) -> Context:
        """
        Get context.

        Returns
        -------
        Context
            Context.
        """
        return get_context(self.project)

    #############################
    #  Task methods
    #############################

    def run(
        self,
        inputs: dict | None,
        outputs: dict | None = None,
        parameters: dict | None = None,
        local_execution: bool = False,
    ) -> Run:
        """
        Run task.

        Parameters
        ----------
        inputs : dict
            The inputs of the run.
        outputs : dict
            The outputs of the run.
        parameters : dict
            The parameters of the run.
        local_execution : bool
            Flag to indicate if the run will be executed locally.

        Returns
        -------
        Run
            Run object.
        """
        return self.new_run(
            project=self.project,
            task=self._get_task_string(),
            task_id=self.id,
            kind=f"{self.kind.split('+')[0]}+run",
            inputs=inputs,
            outputs=outputs,
            parameters=parameters,
            local_execution=local_execution,
        )

    def _get_task_string(self) -> str:
        """
        Get task string.

        Returns
        -------
        str
            Task string.
        """
        splitted = self.spec.function.split("://")
        return f"{self.kind}://{splitted[1]}"

    #############################
    # CRUD Methods for Run
    #############################

    def new_run(self, **kwargs) -> Run:
        """
        Create a new run.

        Parameters
        ----------
        **kwargs
            Keyword arguments.

        Returns
        -------
        Run
            Run object.
        """
        if kwargs["local_execution"]:
            return run_from_parameters(**kwargs)
        return new_run(**kwargs)

    def get_run(self, uuid: str) -> Run:
        """
        Get run.

        Parameters
        ----------
        update : bool
            Flag to indicate update.

        Returns
        -------
        Run
            Run object.
        """
        return get_run(self.project, uuid)

    def delete_run(self, uuid: str) -> None:
        """
        Delete run.

        Parameters
        ----------
        update : bool
            Flag to indicate update.

        Returns
        -------
        None
        """
        delete_run(self.project, uuid)

    #############################
    #  Static interface methods
    #############################

    @staticmethod
    def _parse_dict(
        obj: dict,
        validate: bool = True,
    ) -> dict:
        """
        Get dictionary and parse it to a valid entity dictionary.

        Parameters
        ----------
        entity : str
            Entity type.
        obj : dict
            Dictionary to parse.

        Returns
        -------
        dict
            A dictionary containing the attributes of the entity instance.
        """
        project = obj.get("project")
        kind = obj.get("kind")

        uuid = build_uuid(obj.get("id"))
        metadata = build_metadata(TaskMetadata, **obj.get("metadata", {}))
        spec = build_spec(
            kind,
            validate=validate,
            framework_runtime=kind.split("+")[0],
            **obj.get("spec", {}),
        )
        status = build_status(kind, framework_runtime=kind.split("+")[0], **obj.get("status", {}))
        return {
            "project": project,
            "uuid": uuid,
            "kind": kind,
            "metadata": metadata,
            "spec": spec,
            "status": status,
        }


def task_from_parameters(
    project: str,
    kind: str,
    uuid: str | None = None,
    source: str | None = None,
    labels: list[str] | None = None,
    function: str | None = "",
    node_selector: list[dict] | None = None,
    volumes: list[dict] | None = None,
    resources: list[dict] | None = None,
    affinity: dict | None = None,
    tolerations: list[dict] | None = None,
    k8s_labels: list[dict] | None = None,
    env: list[dict] | None = None,
    secrets: list[str] | None = None,
    **kwargs,
) -> Task:
    """
    Create a new object instance.

    Parameters
    ----------
    project : str
        Name of the project.
    kind : str
        The type of the task.
    uuid : str
        UUID.
    source : str
        Remote git source for object.
    labels : list[str]
        List of labels.
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
    k8s_labels : list[Label]
        The labels of the task.
    env : list[Env]
        The env variables of the task.
    secrets : list[str]
        The secrets of the task.
    **kwargs
        Spec keyword arguments.

    Returns
    -------
    Task
       Object instance.
    """
    uuid = build_uuid(uuid)
    metadata = build_metadata(
        TaskMetadata,
        project=project,
        name=uuid,
        source=source,
        labels=labels,
    )
    spec = build_spec(
        kind,
        framework_runtime=function.split("://")[0],
        function=function,
        node_selector=node_selector,
        volumes=volumes,
        resources=resources,
        affinity=affinity,
        tolerations=tolerations,
        k8s_labels=k8s_labels,
        env=env,
        secrets=secrets,
        **kwargs,
    )
    status = build_status(
        kind,
        framework_runtime=function.split("://")[0],
    )
    return Task(
        project=project,
        uuid=uuid,
        kind=kind,
        metadata=metadata,
        spec=spec,
        status=status,
    )


def task_from_dict(obj: dict) -> Task:
    """
    Create Task object from dictionary.

    Parameters
    ----------
    obj : dict
        Dictionary representation of Task.

    Returns
    -------
    Task
        Task object.
    """
    return Task.from_dict(obj, validate=False)
