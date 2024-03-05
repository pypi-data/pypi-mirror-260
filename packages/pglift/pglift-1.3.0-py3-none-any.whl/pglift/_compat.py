# SPDX-FileCopyrightText: 2021 Dalibo
#
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

import builtins
import importlib.resources
import sys
from typing import Any, Union

if sys.version_info[:2] >= (3, 10):
    from types import NoneType, UnionType
    from typing import ParamSpec

    zip = builtins.zip
    UnionTypes = (UnionType, Union)
else:
    from typing_extensions import ParamSpec

    def zip(*iterables: Any, strict: bool = False) -> Any:
        return builtins.zip(*iterables)

    NoneType = type(None)
    UnionTypes = (Union,)


if sys.version_info[:2] >= (3, 11):
    from typing import Self, assert_never

    def read_resource(pkgname: str, name: str) -> str | None:
        resource = importlib.resources.files(pkgname).joinpath(name)
        if resource.is_file():
            return resource.read_text()
        return None

else:
    from typing_extensions import Self, assert_never

    def read_resource(pkgname: str, name: str) -> str | None:
        if importlib.resources.is_resource(pkgname, name):
            return importlib.resources.read_text(pkgname, name)
        return None


__all__ = [
    "NoneType",
    "ParamSpec",
    "Self",
    "UnionTypes",
    "assert_never",
    "read_resource",
    "zip",
]
