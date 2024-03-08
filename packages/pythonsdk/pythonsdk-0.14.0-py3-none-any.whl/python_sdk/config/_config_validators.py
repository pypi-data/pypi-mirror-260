from __future__ import annotations

import typing

if typing.TYPE_CHECKING:
    from python_sdk.config import _config


class ConfigValidationError(Exception):
    ...


class ConfigValidator(typing.Protocol):
    name: str
    description: str

    def __call__(self, config: type[_config.Config]) -> None:
        """
        Raises:
            ConfigValidationError: Config does not pass validation.
        """
        ...
