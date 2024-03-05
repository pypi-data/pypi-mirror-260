# SPDX-FileCopyrightText: 2021 Dalibo
#
# SPDX-License-Identifier: GPL-3.0-or-later

import string
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Final, Optional, Union

import pydantic
from pydantic import ConfigDict

from .. import types


def string_format_variables(fmt: str) -> set[str]:
    return {v for _, v, _, _ in string.Formatter().parse(fmt) if v is not None}


class BaseModel(pydantic.BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")


class TemplatedPath:
    """Validate that a Path field contains expected template variables."""

    def __init__(self, *args: str) -> None:
        self.variables = set(args)

    def __call__(self, value: Path) -> Path:
        if string_format_variables(str(value)) != self.variables:
            raise ValueError(
                "value contains unknown or missing template variable(s); "
                f"expecting: {', '.join(sorted(self.variables)) or 'none'}"
            )
        return value


@dataclass(frozen=True)
class PrefixedPath:
    basedir: Path = Path("")
    key: str = "prefix"

    def prefix(self, value: Path, prefix: Union[str, Path]) -> Path:
        """Return the path prefixed if is not yet absolute.

        >>> PrefixedPath(basedir=Path("alice")).prefix(Path("documents"), "/home")
        PosixPath('/home/alice/documents')
        >>> PrefixedPath(basedir=Path("/uh")).prefix(Path("/root"), Path("/whatever"))
        PosixPath('/root')
        """
        if value.is_absolute():
            return value
        assert Path(prefix).is_absolute(), (
            f"expecting an absolute prefix (got {prefix!r})",
        )
        return prefix / self.basedir / value


ConfigPath: Final = PrefixedPath(Path("etc"))
DataPath: Final = PrefixedPath(Path("srv"))
LogPath: Final = PrefixedPath(Path("log"))
RunPath: Final = PrefixedPath(Path(""), key="run_prefix")


def prefix_values(m: pydantic.BaseModel, prefixes: dict[str, Path]) -> dict[str, Any]:
    values = {}
    for key, field in m.model_fields.items():
        value = getattr(m, key)
        if isinstance(value, Path):
            if p := types.field_annotation(field, PrefixedPath):
                value = p.prefix(value, prefixes[p.key])
        elif isinstance(value, pydantic.BaseModel):
            value = prefix_values(value, prefixes)
        values[key] = value
    return values


class ServerCert(BaseModel):
    """TLS certificate files for a server."""

    ca_cert: Optional[pydantic.FilePath] = pydantic.Field(
        description="Certificate Authority certificate to verify client requests.",
        default=None,
    )
    cert: pydantic.FilePath = pydantic.Field(
        description="Certificate file for TLS encryption."
    )
    key: pydantic.FilePath = pydantic.Field(
        description="Private key for the certificate."
    )
