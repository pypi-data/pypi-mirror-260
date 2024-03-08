import os
import pathlib
import re
import typing


class ConfigValueValidationError(Exception):
    """Config Value does not pass validation."""

    ...


class ConfigValueValidator(typing.Protocol):
    name: str
    description: str

    def __call__(self, value: typing.Any) -> None:
        """
        Raises:
            ConfigValueValidationError: Config value does not pass validation.
        """
        ...


class ValidateFileExists:
    name: str = "Validate File Exists"
    description: str = "Validates that the file at a given path exists."

    def __call__(self, value: pathlib.Path) -> None:
        """
        Raises:
            ConfigValueValidationError: Path does not exist or is not a directory.
        """
        if not value.exists():
            raise ConfigValueValidationError(f"File at {value} does not exist.")
        if not value.is_file():
            raise ConfigValueValidationError(f"{value} not a file.")


class ValidateDirectoryExists:
    name: str = "Validate Directory Exists"
    description: str = "Validates that the directory at a given path exists."

    def __call__(self, value: pathlib.Path) -> None:
        """
        Raises:
            ConfigValueValidationError: Path does not exist or is not a directory.
        """
        if not value.exists():
            raise ConfigValueValidationError(f"Directory at {value} does not exist.")
        if not value.is_dir():
            raise ConfigValueValidationError(f"{value} not a directory.")


class ValidatePathIsReadable:
    name: str = "Validate Path is Readable"
    description: str = "Validates that a given path is readable."

    def __call__(self, value: pathlib.Path) -> None:
        """
        Raises:
            ConfigValueValidationError: Path is not readable.
        """
        path_to_evaluate = value if value.exists() else value.parent
        if not os.access(path_to_evaluate, os.R_OK):
            raise ConfigValueValidationError(f"{value} is not readable.")


class ValidatePathIsWritable:
    name: str = "Validate Path is Writable"
    description: str = "Validates that a given path is writeable."

    def __call__(self, value: pathlib.Path) -> None:
        """
        Raises:
            ConfigValueValidationError: Path is not writeable.
        """
        path_to_evaluate = value if value.exists() else value.parent
        if not os.access(path_to_evaluate, os.W_OK):
            raise ConfigValueValidationError(f"{value} is not writeable")


class ValidatePathIsExecutable:
    name: str = "Validate Path is Executable"
    description: str = "Validates that a given path is executable."

    def __call__(self, value: pathlib.Path) -> None:
        """
        Raises:
            ConfigValueValidationError: Path is not executable.
        """
        path_to_evaluate = value if value.exists() else value.parent
        if not os.access(path_to_evaluate, os.EX_OK):
            raise ConfigValueValidationError(f"{value} is not executable")


class ValidateFileType:
    name: str = "Validate File Type"
    description: str = "Validates that the file at a given path is of set file type."

    file_type: str

    def __init__(self, file_type: str) -> None:
        self.file_type = file_type if file_type[0] == "." else f".{file_type}"

    def __call__(self, value: pathlib.Path) -> None:
        """
        Raises:
            ConfigValueValidationError: Path is not of correct file type.
        """
        if "".join(value.suffixes) != self.file_type:
            raise ConfigValueValidationError(f"{value} is not {self.file_type}")


class ValidateRegexMatch:
    name: str = "Validate Regex Match"
    description: str = """
    Validates that the passed value(s) match a regex pattern.
    This can be used with strings and lists of strings.
    """

    pattern: re.Pattern

    def __init__(self, pattern: str) -> None:
        self.pattern = re.compile(pattern=pattern)

    def __call__(self, value: str | list[str]) -> None:
        """
        Raises:
            ConfigValueValidationError: Value does not match regex pattern.
        """
        values_to_validate = value if isinstance(value, list) else [value]
        for value in values_to_validate:
            if not self.pattern.match(value):
                raise ConfigValueValidationError(f"Value does not match regex pattern {self.pattern.pattern}")


class ValidateDictKeysRegexMatch:
    name: str = "Validate Dict Keys Regex Match"
    description: str = """
    Validates that the passed dictionary keys match a regex pattern.
    """

    pattern: re.Pattern

    def __init__(self, pattern: str) -> None:
        self.pattern = re.compile(pattern=pattern)

    def __call__(self, value: dict[str, typing.Any]) -> None:
        """
        Raises:
            ConfigValueValidationError: Value does not match regex pattern.
        """
        for key in value:
            if not self.pattern.match(key):
                raise ConfigValueValidationError(f"Key {key} does not match regex pattern {self.pattern.pattern}")


class ValidateNumberRange:
    name: str = "Validate Number Range"
    description: str = """
    Validates that the passed value is within a number range.
    """

    min: float
    max: float

    def __init__(self, min: float, max: float) -> None:
        self.min = min
        self.max = max

    def __call__(self, value: int | float) -> None:
        """
        Raises:
            ConfigValueValidationError: Value does not match regex pattern.
        """
        if not self.min <= value <= self.max:
            raise ConfigValueValidationError(f"Value outside of {self.min} - {self.max} bounds.")
