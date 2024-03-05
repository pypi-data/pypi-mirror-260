"""
This module contains pipable operators that are used to handle errors in aiostream pipelines.
"""

import logging
import sys
from typing import Any, AsyncIterable, AsyncIterator, Callable

from ._extra import IS_AIOSTREAM_INSTALLED
from .decorator import decorator
from .types import ERRORED, AsyncFunctionType, FunctionType, SecuredAsyncFunctionType, SecuredFunctionType, is_secured

if IS_AIOSTREAM_INSTALLED:
    import aiostream
    from aiostream.stream.combine import T, U

    # pylint: disable=too-many-arguments, redefined-builtin
    @aiostream.pipable_operator
    def map(
        source: AsyncIterable[T],
        func: (
            FunctionType[[T], U]
            | AsyncFunctionType[[T], U]
            | SecuredFunctionType[[T], U]
            | SecuredAsyncFunctionType[[T], U]
        ),
        *more_sources: AsyncIterable[T],
        ordered: bool = True,
        task_limit: int | None = None,
        on_success: Callable[[U, T], Any] | None = None,
        on_error: Callable[[Exception, T], Any] | None = None,
        on_finalize: Callable[[T], Any] | None = None,
        wrap_secured_function: bool = False,
        suppress_recalling_on_error: bool = True,
        logger: logging.Logger = logging.getLogger(__name__),
    ) -> AsyncIterator[U]:
        """
        This operator does mostly the same as stream.map of aiostream.
        Additionally, it catches all errors, calls the corresponding callbacks and filters out errored results.
        If suppress_recalling_on_error is True, the on_error callable will not be called if the error were already
        caught by a previous catcher.
        """
        if not wrap_secured_function and is_secured(func):
            if func.__catcher__.on_error_return_always is not ERRORED:
                raise ValueError(
                    "The given function is already secured but does not return ERRORED in error case. "
                    "If the secured function re-raises errors you can set wrap_secured_function=True"
                )
            if (
                on_success is not None
                or on_error is not None
                or on_finalize is not None
                or not suppress_recalling_on_error
            ):
                raise ValueError(
                    "The given function is already secured. "
                    "Please do not set on_success, on_error, on_finalize as they would be ignored. "
                    "You can set wrap_secured_function=True to wrap the secured function with another catcher."
                )
            logger.debug(
                f"The given function {func.__original_callable__.__name__} is already secured. Using it as is."
            )
            secured_func = func
        else:
            secured_func = decorator(  # type: ignore[assignment]
                on_success=on_success,
                on_error=on_error,
                on_finalize=on_finalize,
                on_error_return_always=ERRORED,
                suppress_recalling_on_error=suppress_recalling_on_error,
            )(
                func  # type: ignore[arg-type]
            )
            # Ignore that T | ErroredType is not compatible with T. All ErroredType results are filtered out
            # in a subsequent step.
        next_source: AsyncIterator[U] = aiostream.stream.map.raw(
            source, secured_func, *more_sources, ordered=ordered, task_limit=task_limit  # type: ignore[arg-type]
        )
        next_source = aiostream.stream.filter.raw(next_source, lambda result: result is not ERRORED)
        return next_source

else:
    from ._extra import _NotInstalled

    sys.modules[__name__] = _NotInstalled()  # type: ignore[assignment]
