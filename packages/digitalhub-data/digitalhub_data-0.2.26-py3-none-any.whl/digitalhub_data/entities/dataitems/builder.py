"""
Dataitem module.
"""
from __future__ import annotations

import typing

from digitalhub_core.entities._builders.metadata import build_metadata
from digitalhub_core.entities._builders.spec import build_spec
from digitalhub_core.entities._builders.status import build_status
from digitalhub_core.utils.exceptions import EntityError
from digitalhub_core.utils.generic_utils import build_uuid
from digitalhub_data.entities.dataitems.metadata import DataitemMetadata

if typing.TYPE_CHECKING:
    from digitalhub_data.entities.dataitems.entity._base import Dataitem

# Manage class mapper
cls_mapper = {}
try:
    from digitalhub_data.entities.dataitems.entity.table import DataitemTable

    cls_mapper["table"] = DataitemTable
except ImportError:
    ...
try:
    from digitalhub_data.entities.dataitems.entity.iceberg import DataitemIceberg

    cls_mapper["iceberg"] = DataitemIceberg
except ImportError:
    pass


def _choose_dataitem_type(kind: str) -> type[Dataitem]:
    """
    Choose class based on kind.

    Parameters
    ----------
    kind : str
        Kind of the dataitem.

    Returns
    -------
    type[Dataitem]
        Class of the dataitem.
    """
    try:
        return cls_mapper[kind]
    except KeyError:
        raise EntityError(f"Unknown dataitem kind: {kind}")


def dataitem_from_parameters(
    project: str,
    name: str,
    kind: str,
    uuid: str | None = None,
    description: str | None = None,
    source: str | None = None,
    labels: list[str] | None = None,
    embedded: bool = True,
    key: str | None = None,
    path: str | None = None,
    **kwargs,
) -> Dataitem:
    """
    Create a new object instance.

    Parameters
    ----------
    project : str
        Name of the project.
    name : str
        Identifier of the dataitem.
    kind : str
        The type of the dataitem.
    uuid : str
        UUID.
    description : str
        Description of the dataitem.
    source : str
        Remote git source for object.
    labels : list[str]
        List of labels.
    embedded : bool
        Flag to determine if object must be embedded in project.
    key : str
        Representation of the dataitem, e.g. store://etc.
    path : str
        Path to the dataitem on local file system or remote storage.
    **kwargs
        Spec keyword arguments.

    Returns
    -------
    Dataitem
       Object instance.
    """
    uuid = build_uuid(uuid)
    key = key if key is not None else f"store://{project}/dataitems/{kind}/{name}:{uuid}"
    metadata = build_metadata(
        DataitemMetadata,
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
        layer_digitalhub="digitalhub_data",
        key=key,
        path=path,
        **kwargs,
    )
    status = build_status(kind, layer_digitalhub="digitalhub_data")
    cls = _choose_dataitem_type(kind)
    return cls(
        project=project,
        name=name,
        uuid=uuid,
        kind=kind,
        metadata=metadata,
        spec=spec,
        status=status,
    )


def dataitem_from_dict(obj: dict) -> Dataitem:
    """
    Create dataitem from dictionary.

    Parameters
    ----------
    obj : dict
        Dictionary to create dataitem from.

    Returns
    -------
    Dataitem
        Dataitem object.
    """
    kind = obj.get("kind")
    cls = _choose_dataitem_type(kind)
    return cls.from_dict(obj, validate=False)
