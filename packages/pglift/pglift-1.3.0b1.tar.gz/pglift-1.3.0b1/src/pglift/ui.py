# SPDX-FileCopyrightText: 2023 Dalibo
#
# SPDX-License-Identifier: GPL-3.0-or-later
from __future__ import annotations

import contextvars

from typing_extensions import TypeAlias

from . import abc


def confirm(message: str, default: bool) -> bool:
    ui = _UI.get()
    return ui.confirm(message, default)


def prompt(message: str, hide_input: bool = False) -> str | None:
    ui = _UI.get()
    return ui.prompt(message, hide_input=hide_input)


class UserInterface:
    """Default, non-interactive, UI."""

    def confirm(self, message: str, default: bool) -> bool:
        return default

    def prompt(self, message: str, hide_input: bool = False) -> str | None:
        return None


_UI = contextvars.ContextVar[abc.UserInterface]("UI", default=UserInterface())
Token: TypeAlias = contextvars.Token[abc.UserInterface]
get = _UI.get
set = _UI.set
reset = _UI.reset
