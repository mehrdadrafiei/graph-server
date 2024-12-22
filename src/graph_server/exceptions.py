from typing import Optional

class CommandError(Exception):
    """Base exception for command-related errors."""
    pass

class ValidationError(CommandError):
    """Raised when request validation fails."""
    pass

class CommandExecutionError(CommandError):
    """Raised when command execution fails."""
    def __init__(self, message: str, command: Optional[str] = None):
        self.command = command
        super().__init__(message)