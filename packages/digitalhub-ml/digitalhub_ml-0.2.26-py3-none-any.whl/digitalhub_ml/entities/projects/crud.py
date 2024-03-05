"""
Project operations module.
"""
from __future__ import annotations

import typing

from digitalhub_core.client.builder import build_client, get_client
from digitalhub_core.entities.projects.crud import _setup_project
from digitalhub_core.utils.api import api_base_read
from digitalhub_core.utils.exceptions import BackendError, EntityError
from digitalhub_core.utils.io_utils import read_yaml
from digitalhub_data.entities.projects.entity import project_from_dict, project_from_parameters

if typing.TYPE_CHECKING:
    from digitalhub_ml.entities.projects.entity import ProjectMl as Project


def create_project(**kwargs) -> Project:
    """
    Create a new project.

    Parameters
    ----------
    **kwargs
        Keyword arguments.

    Returns
    -------
    Project
        A Project instance.
    """
    return project_from_parameters(**kwargs)


def create_project_from_dict(obj: dict) -> Project:
    """
    Create a new Project instance from a dictionary.

    Parameters
    ----------
    obj : dict
        Dictionary to create the Project from.

    Returns
    -------
    Project
        Project object.
    """
    return project_from_dict(obj)


def load_project(
    name: str | None = None,
    filename: str | None = None,
    local: bool = False,
    config: dict | None = None,
    setup_kwargs: dict | None = None,
) -> Project:
    """
    Load project and context from backend or file.

    Parameters
    ----------
    name : str
        Name of the project.
    filename : str
        Path to file where to load project from.
    local : bool
        Flag to determine if backend is local.
    config : dict
        DHCore env configuration.

    Returns
    -------
    Project
        A Project instance with setted context.
    """
    if name is not None:
        return get_project(name=name, local=local, config=config, setup_kwargs=setup_kwargs)
    if filename is not None:
        return import_project(filename, local=local, config=config, setup_kwargs=setup_kwargs)
    raise EntityError("Either name or filename must be provided.")


def get_or_create_project(
    name: str,
    local: bool = False,
    config: dict | None = None,
    setup_kwargs: dict | None = None,
    **kwargs,
) -> Project:
    """
    Get or create a project.

    Parameters
    ----------
    name : str
        Name of the project.
    local : bool
        Flag to determine if backend is local.
    config : dict
        DHCore env configuration.
    **kwargs
        Keyword arguments.

    Returns
    -------
    Project
        A Project instance.
    """
    try:
        return get_project(name, local, config=config, setup_kwargs=setup_kwargs)
    except BackendError:
        return new_project(name, local=local, config=config, setup_kwargs=setup_kwargs, **kwargs)


def new_project(
    name: str,
    description: str | None = None,
    source: str | None = None,
    labels: list[str] | None = None,
    local: bool = False,
    config: dict | None = None,
    context: str | None = None,
    setup_kwargs: dict | None = None,
    **kwargs,
) -> Project:
    """
    Create project.

    Parameters
    ----------
    name : str
        Identifier of the project.
    kind : str
        The type of the project.
    uuid : str
        UUID.
    description : str
        Description of the project.
    source : str
        Remote git source for object.
    labels : list[str]
        List of labels.
    local : bool
        Flag to determine if object will be exported to backend.
    config : dict
        DHCore env configuration.
    context : str
        The context of the project.
    setup_kwargs : dict
        Setup keyword arguments.
    **kwargs
        Keyword arguments.

    Returns
    -------
    Project
        Project object.
    """
    build_client(local, config)
    obj = create_project(
        name=name,
        kind="project",
        description=description,
        source=source,
        labels=labels,
        local=local,
        context=context,
        **kwargs,
    )
    obj.save()
    return _setup_project(obj, setup_kwargs)


def get_project(
    name: str,
    local: bool = False,
    config: dict | None = None,
    setup_kwargs: dict | None = None,
) -> Project:
    """
    Retrieves project details from the backend.

    Parameters
    ----------
    name : str
        The name or UUID.
    local : bool
        Flag to determine if backend is local.
    config : dict
        DHCore env configuration.

    Returns
    -------
    Project
        Object instance.
    """
    build_client(local, config)
    api = api_base_read("projects", name)
    client = get_client(local)
    obj = client.read_object(api)
    obj["local"] = local
    project = create_project_from_dict(obj)
    return _setup_project(project, setup_kwargs)


def import_project(
    file: str,
    local: bool = False,
    config: dict | None = None,
    setup_kwargs: dict | None = None,
) -> Project:
    """
    Import an Project object from a file using the specified file path.

    Parameters
    ----------
    file : str
        Path to the file.
    local : bool
        Flag to determine if backend is local.
    config : dict
        DHCore env configuration.

    Returns
    -------
    Project
        Object instance.
    """
    build_client(local, config)
    obj: dict = read_yaml(file)
    obj["local"] = local
    project = create_project_from_dict(obj)
    return _setup_project(project, setup_kwargs)
