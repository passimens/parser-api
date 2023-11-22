class ParserError(Exception):
    """Base class for exceptions in this module."""
    pass


class NoDataError(ParserError):
    """Raised when no-data condition is treated as error by parser."""
    pass


class InputError(ParserError):
    """Raised when data is corrupt and cannot be parsed."""
    pass


class FormatError(InputError):
    """Raised when data format is not as expected by parser."""
    pass


class IncompleteDataError(InputError):
    """Raised when data is incomplete and cannot be parsed."""
    pass
