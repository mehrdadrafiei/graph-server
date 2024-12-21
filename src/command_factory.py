from typing import Dict, Any
from src.commands import Command, OSCommand, ComputeCommand

class CommandFactory:
    """Factory for creating command instances."""
    
    @staticmethod
    def create_command(request: Dict[str, Any]) -> Command:
        """Create appropriate command instance based on request type."""
        command_type = request["command_type"]
        
        if command_type == "os":
            return OSCommand(request["command_name"], request.get("parameters", []))
        elif command_type == "compute":
            return ComputeCommand(request["expression"])
        else:
            raise ValueError(f"Unknown command type: {command_type}")
        