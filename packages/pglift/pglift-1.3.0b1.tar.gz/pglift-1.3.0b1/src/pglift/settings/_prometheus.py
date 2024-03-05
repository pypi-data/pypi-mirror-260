# SPDX-FileCopyrightText: 2021 Dalibo
#
# SPDX-License-Identifier: GPL-3.0-or-later

import warnings
from pathlib import Path
from typing import Annotated, Any, Optional

from pydantic import AfterValidator, Field, FilePath, ValidationInfo

from .base import BaseModel, ConfigPath, RunPath, TemplatedPath


def _queriespath_is_deprecated(value: Any, info: ValidationInfo) -> Any:
    if value is not None:
        warnings.warn(
            f"{info.field_name!r} setting is deprecated; make sure the postgres_exporter in use supports this",
            FutureWarning,
            stacklevel=2,
        )
    return value


class Settings(BaseModel):
    """Settings for Prometheus postgres_exporter"""

    execpath: Annotated[
        FilePath, Field(description="Path to the postgres_exporter executable.")
    ]

    role: Annotated[
        str,
        Field(
            description="Name of the PostgreSQL role for Prometheus postgres_exporter."
        ),
    ] = "prometheus"

    configpath: Annotated[
        Path,
        AfterValidator(TemplatedPath("name")),
        ConfigPath,
        Field(description="Path to the config file.", validate_default=True),
    ] = Path("prometheus/postgres_exporter-{name}.conf")

    queriespath: Annotated[
        Optional[Path],
        ConfigPath,
        Field(description="Path to the queries file (DEPRECATED)."),
        AfterValidator(_queriespath_is_deprecated),
    ] = None

    pid_file: Annotated[
        Path,
        AfterValidator(TemplatedPath("name")),
        RunPath,
        Field(
            description="Path to which postgres_exporter process PID will be written.",
            validate_default=True,
        ),
    ] = Path("prometheus/{name}.pid")
