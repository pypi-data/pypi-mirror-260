# SPDX-FileCopyrightText: 2021 Dalibo
#
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

from pathlib import Path
from typing import ClassVar

from attrs import frozen

from ...settings._patroni import Settings
from .. import impl


@frozen
class Service:
    """A Patroni service bound to a PostgreSQL instance."""

    __service_name__: ClassVar = "patroni"
    cluster: str
    node: str
    name: str
    settings: Settings

    def __str__(self) -> str:
        return f"{self.__service_name__}@{self.name}"

    def args(self) -> list[str]:
        configpath = impl._configpath(self.name, self.settings)
        return [str(self.settings.execpath), str(configpath)]

    def pidfile(self) -> Path:
        return Path(str(self.settings.pid_file).format(name=self.name))

    def env(self) -> None:
        return None
