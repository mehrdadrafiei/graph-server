from abc import ABC, abstractmethod
import asyncio
from typing import Dict, Any, List
import ast
import operator
from src.exceptions import CommandExecutionError

class Command(ABC):
    """Abstract base class for commands (Command Pattern)."""
    
    @abstractmethod
    async def execute(self) -> Dict[str, str]:
        """Execute the command and return the result."""
        pass

class OSCommand(Command):
    """Handles system command execution."""
    
    SAFE_COMMANDS = {'ls', 'dir', 'cp', 'copy', 'sleep'}
    
    def __init__(self, command_name: str, parameters: List[str]):
        self._validate_command(command_name)
        self.command_name = command_name
        self.parameters = parameters
    
    def _validate_command(self, command_name: str) -> None:
        if command_name not in self.SAFE_COMMANDS:
            raise CommandExecutionError(
                f"Command '{command_name}' not allowed",
                command_name
            )
    
    async def execute(self) -> Dict[str, str]:
        command = [self.command_name] + self.parameters
        command_str = " ".join(command)
        
        try:
            process = await asyncio.create_subprocess_exec(
                *command,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            
            stdout, stderr = await process.communicate()
            
            if process.returncode != 0:
                raise CommandExecutionError(
                    f"Command failed: {stderr.decode().strip()}",
                    command_str
                )
            
            return {
                "given_os_command": command_str,
                "result": stdout.decode().strip()
            }
            
        except FileNotFoundError:
            raise CommandExecutionError(
                f"Command not found: {self.command_name}",
                command_str
            )

class ComputeCommand(Command):
    """Handles mathematical expression evaluation."""
    
    OPERATORS = {
        ast.Add: operator.add,
        ast.Sub: operator.sub,
        ast.Mult: operator.mul,
        ast.Div: operator.truediv,
        ast.Pow: operator.pow,
    }
    
    def __init__(self, expression: str):
        self.expression = expression
    
    async def execute(self) -> Dict[str, str]:
        try:
            parsed = ast.parse(self.expression, mode='eval')
            result = self._eval_expr(parsed.body)
            
            return {
                "given_math_expression": self.expression,
                "result": str(result)
            }
            
        except Exception as e:
            raise CommandExecutionError(
                f"Expression evaluation failed: {str(e)}",
                self.expression
            )
    
    def _eval_expr(self, node: ast.AST) -> float:
        if isinstance(node, ast.Constant):
            if isinstance(node.value, (int, float)):
                return node.value
            else:
                raise CommandExecutionError(
                    f"Unsupported constant type: {type(node.value).__name__}",
                    self.expression
                )
        elif isinstance(node, ast.BinOp):
            if type(node.op) not in self.OPERATORS:
                raise CommandExecutionError(
                    f"Unsupported operator: {type(node.op).__name__}",
                    self.expression
                )
            
            left = self._eval_expr(node.left)
            right = self._eval_expr(node.right)
            return self.OPERATORS[type(node.op)](left, right)
        else:
            raise CommandExecutionError(
                f"Unsupported expression type: {type(node).__name__}",
                self.expression
            )