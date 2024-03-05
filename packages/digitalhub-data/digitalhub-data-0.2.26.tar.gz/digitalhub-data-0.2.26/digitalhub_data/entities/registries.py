from __future__ import annotations

from digitalhub_core.entities._base.spec import SpecRegistry
from digitalhub_core.entities._base.status import StatusRegistry

status_registry = StatusRegistry()
status_registry.register(
    "dataitem",
    "digitalhub_data.entities.dataitems.status",
    "DataitemStatus",
)
status_registry.register(
    "table",
    "digitalhub_data.entities.dataitems.status",
    "DataitemStatusTable",
)
status_registry.register(
    "iceberg",
    "digitalhub_data.entities.dataitems.status",
    "DataitemStatusIceberg",
)

spec_registry = SpecRegistry()
spec_registry.register(
    "dataitem",
    "digitalhub_data.entities.dataitems.spec",
    "DataitemSpec",
    "DataitemParams",
)
spec_registry.register(
    "table",
    "digitalhub_data.entities.dataitems.spec",
    "DataitemSpecTable",
    "DataitemParamsTable",
)
spec_registry.register(
    "iceberg",
    "digitalhub_data.entities.dataitems.spec",
    "DataitemSpecIceberg",
    "DataitemParamsIceberg",
)
spec_registry.register(
    "project",
    "digitalhub_data.entities.projects.spec",
    "ProjectSpecData",
    "ProjectParamsData",
)
