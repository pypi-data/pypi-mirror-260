from __future__ import annotations

from digitalhub_core.entities._base.spec import SpecRegistry
from digitalhub_core.entities._base.status import StatusRegistry

status_registry = StatusRegistry()
status_registry.register(
    "model",
    "digitalhub_ml.entities.models.status",
    "ModelStatus",
)

spec_registry = SpecRegistry()
spec_registry.register(
    "model",
    "digitalhub_ml.entities.models.spec",
    "ModelSpec",
    "ModelParams",
)
spec_registry.register(
    "project",
    "digitalhub_ml.entities.projects.spec",
    "ProjectSpecMl",
    "ProjectParamsMl",
)
