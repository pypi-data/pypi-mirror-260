# SPDX-FileCopyrightText: 2021 Dalibo
#
# SPDX-License-Identifier: GPL-3.0-or-later

import os
import shutil
from pathlib import Path
from typing import Annotated, Any, ClassVar

from pydantic import AfterValidator, Field, ValidationInfo, model_validator

from .. import util
from .base import BaseModel


def default_systemd_unit_path(uid: int) -> Path:
    """Return the default systemd unit path for 'uid'.

    >>> default_systemd_unit_path(0)
    PosixPath('/etc/systemd/system')
    >>> default_systemd_unit_path(42)  # doctest: +ELLIPSIS
    PosixPath('/.../.local/share/systemd/user')
    """
    if uid == 0:
        return Path("/etc/systemd/system")
    return util.xdg_data_home() / "systemd" / "user"


def check_sudo_and_user(value: bool, info: ValidationInfo) -> bool:
    if value and info.data.get("user"):
        raise ValueError("cannot be used with 'user' mode")
    return value


class Settings(BaseModel):
    """Systemd settings."""

    systemctl: ClassVar[Path]

    @model_validator(mode="before")
    @classmethod
    def __systemctl_(cls, values: dict[str, Any]) -> dict[str, Any]:
        if not hasattr(cls, "systemctl"):
            systemctl = shutil.which("systemctl")
            if systemctl is None:
                raise ValueError("systemctl command not found")
            cls.systemctl = Path(systemctl)
        return values

    unit_path: Annotated[
        Path, Field(description="Base path where systemd units will be installed.")
    ] = default_systemd_unit_path(os.getuid())

    user: Annotated[
        bool,
        Field(
            description="Use the system manager of the calling user, by passing --user to systemctl calls."
        ),
    ] = True

    sudo: Annotated[
        bool,
        Field(
            description="Run systemctl command with sudo; only applicable when 'user' is unset."
        ),
        AfterValidator(check_sudo_and_user),
    ] = False
