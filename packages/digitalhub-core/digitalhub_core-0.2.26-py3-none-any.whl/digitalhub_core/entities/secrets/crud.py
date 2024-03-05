"""
Secret operations module.
"""
from __future__ import annotations

import typing

from digitalhub_core.context.builder import check_context, get_context
from digitalhub_core.entities.secrets.entity import secret_from_dict, secret_from_parameters
from digitalhub_core.utils.api import api_ctx_delete, api_ctx_read, api_ctx_update
from digitalhub_core.utils.io_utils import read_yaml

if typing.TYPE_CHECKING:
    from digitalhub_core.entities.secrets.entity import Secret


def create_secret(**kwargs) -> Secret:
    """
    Create a new Secret instance with the specified parameters.

    Parameters
    ----------
    **kwargs
        Keyword arguments.

    Returns
    -------
    Secret
        An instance of the created secret.
    """
    return secret_from_parameters(**kwargs)


def create_secret_from_dict(obj: dict) -> Secret:
    """
    Create a new Secret instance from a dictionary.

    Parameters
    ----------
    obj : dict
        Dictionary to create the Secret from.

    Returns
    -------
    Secret
        Secret object.
    """
    check_context(obj.get("project"))
    return secret_from_dict(obj)


def new_secret(
    project: str,
    name: str,
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
    uuid : str
        UUID.
    description : str
        A description of the secret.
    source : str
        Remote git source for object.
    labels : list[str]
        List of labels.
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
    obj = create_secret(
        project=project,
        name=name,
        kind="secret",
        uuid=uuid,
        description=description,
        source=source,
        labels=labels,
        path=path,
        provider=provider,
        embedded=embedded,
        **kwargs,
    )
    obj.save()
    return obj


def get_secret(project: str, name: str, uuid: str | None = None) -> Secret:
    """
    Retrieves secret details from the backend.

    Parameters
    ----------

    project : str
        Name of the project.
    name : str
        The name of the secret.
    uuid : str
        UUID.

    Returns
    -------
    Secret
        Object instance.
    """
    api = api_ctx_read(project, "secrets", name, uuid=uuid)
    obj = get_context(project).read_object(api)
    return create_secret_from_dict(obj)


def import_secret(file: str) -> Secret:
    """
    Import an Secret object from a file using the specified file path.

    Parameters
    ----------
    file : str
        Path to the file.

    Returns
    -------
    Secret
        Object instance.
    """
    obj: dict = read_yaml(file)
    return create_secret_from_dict(obj)


def delete_secret(project: str, name: str, uuid: str | None = None) -> dict:
    """
    Delete secret from the backend. If the uuid is not specified, delete all versions.

    Parameters
    ----------
    project : str
        Name of the project.
    name : str
        The name of the secret.
    uuid : str
        UUID.

    Returns
    -------
    dict
        Response from backend.
    """
    api = api_ctx_delete(project, "secrets", name, uuid=uuid)
    return get_context(project).delete_object(api)


def update_secret(secret: Secret) -> dict:
    """
    Update a secret.

    Parameters
    ----------
    secret : Secret
        The secret to update.

    Returns
    -------
    dict
        Response from backend.
    """
    api = api_ctx_update(secret.project, "secrets", secret.name, uuid=secret.id)
    return get_context(secret.project).update_object(secret.to_dict(), api)
