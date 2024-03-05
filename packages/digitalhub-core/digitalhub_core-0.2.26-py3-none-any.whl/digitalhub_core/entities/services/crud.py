"""
Service operations module.
"""
from __future__ import annotations

import typing

from digitalhub_core.context.builder import check_context, get_context
from digitalhub_core.entities.services.entity import service_from_dict, service_from_parameters
from digitalhub_core.utils.api import api_ctx_delete, api_ctx_read, api_ctx_update
from digitalhub_core.utils.io_utils import read_yaml

if typing.TYPE_CHECKING:
    from digitalhub_core.entities.services.entity import Service


def create_service(**kwargs) -> Service:
    """
    Create a new Service instance with the specified parameters.

    Parameters
    ----------
    **kwargs
        Keyword arguments.

    Returns
    -------
    Service
        An instance of the created service.
    """
    return service_from_parameters(**kwargs)


def create_service_from_dict(obj: dict) -> Service:
    """
    Create a new Service instance from a dictionary.

    Parameters
    ----------
    obj : dict
        Dictionary to create the Service from.

    Returns
    -------
    Service
        Service object.
    """
    check_context(obj.get("project"))
    return service_from_dict(obj)


def new_service(
    project: str,
    name: str,
    kind: str,
    uuid: str | None = None,
    description: str | None = None,
    source: str | None = None,
    labels: list[str] | None = None,
    embedded: bool = True,
    **kwargs,
) -> Service:
    """
    Create a new Service instance with the specified parameters.

    Parameters
    ----------
    project : str
        A string representing the project associated with this service.
    name : str
        The name of the service.
    kind : str
        Kind of the object.
    uuid : str
        UUID.
    description : str
        A description of the service.
    source : str
        Remote git source for object.
    labels : list[str]
        List of labels.
    embedded : bool
        Flag to determine if object must be embedded in project.
    **kwargs
        Spec keyword arguments.

    Returns
    -------
    Service
        An instance of the created service.
    """
    obj = create_service(
        project=project,
        name=name,
        kind=kind,
        uuid=uuid,
        description=description,
        source=source,
        labels=labels,
        embedded=embedded,
        **kwargs,
    )
    obj.save()
    return obj


def get_service(project: str, name: str, uuid: str | None = None) -> Service:
    """
    Retrieves service details from the backend.

    Parameters
    ----------

    project : str
        Name of the project.
    name : str
        The name of the service.
    uuid : str
        UUID.

    Returns
    -------
    Service
        Object instance.
    """
    api = api_ctx_read(project, "services", name, uuid=uuid)
    obj = get_context(project).read_object(api)
    return create_service_from_dict(obj)


def import_service(file: str) -> Service:
    """
    Import an Service object from a file using the specified file path.

    Parameters
    ----------
    file : str
        Path to the file.

    Returns
    -------
    Service
        Object instance.
    """
    obj: dict = read_yaml(file)
    return create_service_from_dict(obj)


def delete_service(project: str, name: str, uuid: str | None = None) -> dict:
    """
    Delete service from the backend. If the uuid is not specified, delete all versions.

    Parameters
    ----------
    project : str
        Name of the project.
    name : str
        The name of the service.
    uuid : str
        UUID.

    Returns
    -------
    dict
        Response from backend.
    """
    api = api_ctx_delete(project, "services", name, uuid=uuid)
    return get_context(project).delete_object(api)


def update_service(service: Service) -> dict:
    """
    Update a service.

    Parameters
    ----------
    service : Service
        The service to update.

    Returns
    -------
    dict
        Response from backend.
    """
    api = api_ctx_update(service.project, "services", service.name, uuid=service.id)
    return get_context(service.project).update_object(service.to_dict(), api)
