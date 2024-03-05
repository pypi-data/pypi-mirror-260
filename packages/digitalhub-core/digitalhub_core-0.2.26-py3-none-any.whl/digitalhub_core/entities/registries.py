from __future__ import annotations

from digitalhub_core.entities._base.spec import SpecRegistry
from digitalhub_core.entities._base.status import StatusRegistry

status_registry = StatusRegistry()
status_registry.register(
    "artifact",
    "digitalhub_core.entities.artifacts.status",
    "ArtifactStatus",
)
status_registry.register(
    "function",
    "digitalhub_core.entities.functions.status",
    "FunctionStatus",
)
status_registry.register(
    "project",
    "digitalhub_core.entities.projects.status",
    "ProjectStatus",
)
status_registry.register(
    "secret",
    "digitalhub_core.entities.secrets.status",
    "SecretStatus",
)
status_registry.register(
    "service",
    "digitalhub_core.entities.services.status",
    "ServiceStatus",
)
status_registry.register(
    "task",
    "digitalhub_core.entities.tasks.status",
    "TaskStatus",
)
status_registry.register(
    "workflow",
    "digitalhub_core.entities.workflows.status",
    "WorkflowStatus",
)


spec_registry = SpecRegistry()
spec_registry.register(
    "artifact",
    "digitalhub_core.entities.artifacts.spec",
    "ArtifactSpec",
    "ArtifactParams",
)
spec_registry.register(
    "project",
    "digitalhub_core.entities.projects.spec",
    "ProjectSpec",
    "ProjectParams",
)
spec_registry.register(
    "secret",
    "digitalhub_core.entities.secrets.spec",
    "SecretSpec",
    "SecretParams",
)
spec_registry.register(
    "service",
    "digitalhub_core.entities.services.spec",
    "ServiceSpec",
    "ServiceParams",
)
spec_registry.register(
    "workflow",
    "digitalhub_core.entities.workflows.spec",
    "WorkflowSpec",
    "WorkflowParams",
)
