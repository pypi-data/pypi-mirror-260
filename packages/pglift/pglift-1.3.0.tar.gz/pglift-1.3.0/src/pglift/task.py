# SPDX-FileCopyrightText: 2021 Dalibo
#
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

import collections
import contextlib
import functools
import inspect
import logging
from collections.abc import AsyncIterator, Iterator
from dataclasses import dataclass
from typing import Any, Callable, ClassVar, Deque, Generic, Protocol, TypeVar, overload

import pydantic

from . import __name__ as pkgname
from . import exceptions
from ._compat import ParamSpec

P = ParamSpec("P")
T = TypeVar("T")

Call = tuple["Task[Any, Any]", tuple[Any, ...], dict[str, Any]]

logger = logging.getLogger(pkgname)


class Displayer(Protocol):
    def handle(self, msg: str) -> None: ...


@dataclass
class RevertAction(Generic[P]):
    signature: inspect.Signature
    call: Callable[P, Any]


class Task(Generic[P, T]):
    _calls: ClassVar[Deque[Call] | None] = None
    displayer: ClassVar[Displayer | None] = None

    def __init__(self, title: str | None, action: Callable[P, T]) -> None:
        self.title = title
        self.action = action
        self.signature = inspect.signature(action)
        self.revert_action: RevertAction[P] | None = None
        functools.update_wrapper(self, action)

    def __repr__(self) -> str:
        return f"<Task {self.action.__name__!r} at 0x{id(self)}>"

    def __call__(self, *args: P.args, **kwargs: P.kwargs) -> T:
        if self._calls is not None:
            self._calls.append((self, args, kwargs))
        b = self.signature.bind(*args, **kwargs)
        b.apply_defaults()
        if self.title:
            self.display(self.title.format(**b.arguments))
        return self.action(*args, **kwargs)

    def display(self, title: str) -> None:
        if self.displayer is not None:
            self.displayer.handle(title)

    @overload
    def revert(self, __func: Callable[P, Any]) -> Callable[P, Any]: ...

    @overload
    def revert(
        self, *, title: str | None = None
    ) -> Callable[[Callable[P, Any]], Callable[P, Any]]: ...

    def revert(
        self, __func: Callable[P, Any] | None = None, *, title: str | None = None
    ) -> Callable[P, Any] | Callable[[Callable[P, Any]], Callable[P, Any]]:
        """Decorator to register a 'revert' callback function.

        The revert function must accept the same arguments than its respective
        action.
        """
        action_iscoroutinefunction = inspect.iscoroutinefunction(self.action)

        def decorator(revertfn: Callable[P, Any]) -> Callable[P, Any]:
            if action_iscoroutinefunction and not inspect.iscoroutinefunction(revertfn):
                raise TypeError(
                    f"revert function '{revertfn.__module__}.{revertfn.__name__}' must be a coroutine function"
                )
            s = inspect.signature(revertfn)
            assert s.parameters == self.signature.parameters, (
                f"Parameters of function {self.action.__module__}.{self.action.__name__}({self.signature}) "
                f"differ from related revert function {revertfn.__module__}.{revertfn.__name__}({s})"
            )

            @functools.wraps(revertfn)
            def wrapper(*args: P.args, **kwargs: P.kwargs) -> Any:
                b = s.bind(*args, **kwargs)
                b.apply_defaults()
                if title is not None:
                    self.display(title.format(**b.arguments))
                return revertfn(*args, **kwargs)

            self.revert_action = RevertAction(s, wrapper)
            return wrapper

        if __func is not None:
            return decorator(__func)
        return decorator

    def rollback(self, *args: P.args, **kwargs: P.kwargs) -> Any:
        if self.revert_action is None:
            return
        if self.title:
            b = self.revert_action.signature.bind(*args, **kwargs)
            b.apply_defaults()
            logger.warning("reverting: %s", self.title.format(**b.arguments))
        return self.revert_action.call(*args, **kwargs)


@overload
def task(__func: Callable[P, T]) -> Task[P, T]: ...


@overload
def task(*, title: str | None) -> Callable[[Callable[P, T]], Task[P, T]]: ...


def task(
    __func: Callable[P, T] | None = None, *, title: str | None = None
) -> Task[P, T] | Callable[[Callable[P, T]], Task[P, T]]:
    def mktask(fn: Callable[P, T]) -> Task[P, T]:
        return functools.wraps(fn)(Task(title, fn))

    if __func is not None:
        return mktask(__func)
    return mktask


@contextlib.contextmanager
def displayer_installed(displayer: Displayer | None) -> Iterator[None]:
    if displayer is None:
        yield
        return
    assert Task.displayer is None
    Task.displayer = displayer
    try:
        yield
    finally:
        Task.displayer = None


@contextlib.contextmanager
def transaction(revert_on_error: bool = True) -> Iterator[None]:
    """Context manager handling revert of run tasks, in case of failure."""
    if Task._calls is not None:
        raise RuntimeError("inconsistent task state")
    Task._calls = collections.deque()
    try:
        yield
    except BaseException as exc:
        # Only log internal errors, i.e. those not coming from user
        # cancellation or invalid input data.
        if isinstance(exc, KeyboardInterrupt):
            if Task._calls:
                logger.warning("%s interrupted", Task._calls[-1][0])
        elif not isinstance(
            exc,
            (
                exceptions.ValidationError,
                pydantic.ValidationError,
                exceptions.Cancelled,
            ),
        ):
            logger.warning(str(exc))
        assert Task._calls is not None
        while True:
            try:
                t, args, kwargs = Task._calls.pop()
            except IndexError:
                break
            if revert_on_error:
                r = t.rollback(*args, **kwargs)
                assert not inspect.isawaitable(r)
        raise exc
    finally:
        Task._calls = None


@contextlib.asynccontextmanager
async def async_transaction(revert_on_error: bool = True) -> AsyncIterator[None]:
    """Context manager handling revert of run tasks, in case of failure."""
    if Task._calls is not None:
        raise RuntimeError("inconsistent task state")
    Task._calls = collections.deque()
    try:
        yield
    except BaseException as exc:
        # Only log internal errors, i.e. those not coming from user
        # cancellation or invalid input data.
        if isinstance(exc, KeyboardInterrupt):
            if Task._calls:
                logger.warning("%s interrupted", Task._calls[-1][0])
        elif not isinstance(
            exc,
            (
                exceptions.ValidationError,
                pydantic.ValidationError,
                exceptions.Cancelled,
            ),
        ):
            logger.warning(str(exc))
        assert Task._calls is not None
        while True:
            try:
                t, args, kwargs = Task._calls.pop()
            except IndexError:
                break
            if revert_on_error:
                r = t.rollback(*args, **kwargs)
                if inspect.isawaitable(r):
                    await r
        raise exc
    finally:
        Task._calls = None
