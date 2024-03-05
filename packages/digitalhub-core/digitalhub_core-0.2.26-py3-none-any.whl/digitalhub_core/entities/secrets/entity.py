"""
Secret module.
"""
from __future__ import annotations

import typing
from pathlib import Path

from digitalhub_core.context.builder import get_context
from digitalhub_core.entities._base.entity import Entity
from digitalhub_core.entities._builders.metadata import build_metadata
from digitalhub_core.entities._builders.spec import build_spec
from digitalhub_core.entities._builders.status import build_status
from digitalhub_core.entities.secrets.metadata import SecretMetadata
from digitalhub_core.entities.secrets.status import SecretStatus
from digitalhub_core.utils.api import api_base_read, api_base_update, api_ctx_create, api_ctx_update
from digitalhub_core.utils.generic_utils import build_uuid, get_timestamp
from digitalhub_core.utils.io_utils import write_yaml

if typing.TYPE_CHECKING:
    from digitalhub_core.context.context import Context
    from digitalhub_core.entities.secrets.spec import SecretSpec


class Secret(Entity):
    """
    A class representing a secret.
    """

    def __init__(
        self,
        project: str,
        name: str,
        uuid: str,
        kind: str,
        metadata: SecretMetadata,
        spec: SecretSpec,
        status: SecretStatus,
    ) -> None:
        """
        Constructor.

        Parameters
        ----------
        project : str
            Name of the project.
        name : str
            Name of the object.
        uuid : str
            Version of the object.
        kind : str
            Kind of the object.
        metadata : SecretMetadata
            Metadata of the object.
        spec : SecretSpec
            Specification of the object.
        status : SecretStatus
            Status of the object.
        """
        super().__init__()
        self.project = project
        self.name = name
        self.id = uuid
        self.kind = kind
        self.metadata = metadata
        self.spec = spec
        self.status = status

        # Add attributes to be used in the to_dict method
        self._obj_attr.extend(["project", "name", "id"])

    #############################
    #  Save / Export
    #############################

    def save(self, update: bool = False) -> dict:
        """
        Save secret into backend.

        Parameters
        ----------
        update : bool
            Flag to indicate update.

        Returns
        -------
        dict
            Mapping representation of Secret from backend.
        """
        obj = self.to_dict()

        if not update:
            api = api_ctx_create(self.project, "secrets")
            return self._context().create_object(obj, api)

        self.metadata.updated = obj["metadata"]["updated"] = get_timestamp()
        api = api_ctx_update(self.project, "secrets", self.name, self.id)
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
    #  Secret methods
    #############################

    def set_secret(self, key: str, value: str) -> dict:
        """
        Set a secret.

        Parameters
        ----------
        key : str
            Key of the secret.
        value : str
            Value of the secret.

        Returns
        -------
        dict
            Response from backend.
        """
        if self._context().local:
            raise NotImplementedError("set_secret() is not implemented for local projects.")

        obj = {key: value}
        api = api_base_update("projects", self.project) + "/secrets/data"
        return self._context().update_object(obj, api)

    def read_secret(self, key: str) -> dict:
        """
        Read a secret from the backend.

        Parameters
        ----------
        key : str
            Key of the secret.

        Returns
        -------
        str
            Value of the secret.
        """
        if self._context().local:
            raise NotImplementedError("read_secret() is not implemented for local projects.")
        api = api_base_read("projects", self.project) + f"/secrets/data?keys={key}"
        return self._context().read_object(api)

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
        obj : dict
            Dictionary to parse.

        Returns
        -------
        dict
            A dictionary containing the attributes of the entity instance.
        """
        project = obj.get("project")
        name = obj.get("name")
        kind = obj.get("kind")
        uuid = build_uuid(obj.get("id"))
        metadata = build_metadata(SecretMetadata, **obj.get("metadata", {}))
        spec = build_spec(
            kind,
            layer_digitalhub="digitalhub_core",
            validate=validate,
            **obj.get("spec", {}),
        )
        status = build_status(kind, layer_digitalhub="digitalhub_core", **obj.get("status", {}))
        return {
            "project": project,
            "name": name,
            "uuid": uuid,
            "kind": kind,
            "metadata": metadata,
            "spec": spec,
            "status": status,
        }


def secret_from_parameters(
    project: str,
    name: str,
    kind: str,
    uuid: str | None = None,
    description: str | None = None,
    source: str | None = None,
    labels: list[str] | None = None,
    embedded: bool = True,
    path: str | None = None,
    provider: str | None = None,
    **kwargs,
) -> Secret:
    """
    Create a new Secret instance with the specified parameters.

    Parameters
    ----------
    project : str
        A string representing the project associated with this secret.
    name : str
        The name of the secret.
    kind : str
        Kind of the object.
    uuid : str
        UUID.
    source : str
        Remote git source for object.
    labels : list[str]
        List of labels.
    description : str
        A description of the secret.
    embedded : bool
        Flag to determine if object must be embedded in project.
    path : str
        Path to the secret file.
    provider : str
        Provider of the secret.
    **kwargs
        Spec keyword arguments.

    Returns
    -------
    Secret
        An instance of the created secret.
    """
    uuid = build_uuid(uuid)
    metadata = build_metadata(
        SecretMetadata,
        project=project,
        name=name,
        version=uuid,
        description=description,
        source=source,
        labels=labels,
        embedded=embedded,
    )
    spec = build_spec(
        kind,
        path=path,
        provider=provider,
        layer_digitalhub="digitalhub_core",
        **kwargs,
    )
    status = build_status(kind, layer_digitalhub="digitalhub_core")
    return Secret(
        project=project,
        name=name,
        uuid=uuid,
        kind=kind,
        metadata=metadata,
        spec=spec,
        status=status,
    )


def secret_from_dict(obj: dict) -> Secret:
    """
    Create Secret instance from a dictionary.

    Parameters
    ----------
    obj : dict
        Dictionary to create Secret from.

    Returns
    -------
    Secret
        Secret instance.
    """
    return Secret.from_dict(obj, validate=False)
