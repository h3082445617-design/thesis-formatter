"""Custom exception classes for formatting errors."""


class FormattingError(Exception):
    """Base exception for formatting errors."""
    pass


class InvalidFileFormatError(FormattingError):
    """Raised when file is not .docx format."""
    pass


class FileTooLargeError(FormattingError):
    """Raised when file exceeds 50MB limit."""
    pass


class FileCorruptedError(FormattingError):
    """Raised when file cannot be opened or is corrupted."""
    pass


class ProcessingTimeoutError(FormattingError):
    """Raised when processing takes too long."""
    pass


class TitleDetectionError(FormattingError):
    """Raised when title hierarchy cannot be determined."""
    pass
