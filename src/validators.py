from abc import ABC, abstractmethod
from typing import Dict, Any
from exceptions import ValidationError

class RequestValidator(ABC):
    """Abstract base class for request validators."""
    
    @abstractmethod
    def validate(self, request: Dict[str, Any]) -> None:
        """Validate the request format."""
        pass

class JSONRequestValidator(RequestValidator):
    """Validates JSON request format."""
    
    def validate(self, request: Dict[str, Any]) -> None:
        if not isinstance(request, dict):
            raise ValidationError("Request must be a JSON object")
            
        if "command_type" not in request:
            raise ValidationError("Missing 'command_type' in request")
            
        command_type = request["command_type"]
        
        if command_type == "os":
            self._validate_os_command(request)
        elif command_type == "compute":
            self._validate_compute_command(request)
        else:
            raise ValidationError(f"Invalid command_type: {command_type}")
    
    def _validate_os_command(self, request: Dict[str, Any]) -> None:
        if "command_name" not in request:
            raise ValidationError("Missing 'command_name' for OS command")
            
        if not isinstance(request.get("parameters", []), list):
            raise ValidationError("'parameters' must be a list")
    
    def _validate_compute_command(self, request: Dict[str, Any]) -> None:
        if "expression" not in request:
            raise ValidationError("Missing 'expression' for compute command")