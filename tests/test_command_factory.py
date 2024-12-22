import pytest
from graph_server.command_factory import CommandFactory
from graph_server.commands import OSCommand, ComputeCommand

class TestCommandFactory:
    def test_create_os_command(self):
        request = {
            "command_type": "os",
            "command_name": "ls",
            "parameters": ["-l"]
        }
        command = CommandFactory.create_command(request)
        assert isinstance(command, OSCommand)
        assert command.command_name == "ls"
        assert command.parameters == ["-l"]

    def test_create_compute_command(self):
        request = {
            "command_type": "compute",
            "expression": "2 + 2"
        }
        command = CommandFactory.create_command(request)
        assert isinstance(command, ComputeCommand)
        assert command.expression == "2 + 2"

    def test_invalid_command_type(self):
        request = {
            "command_type": "invalid"
        }
        with pytest.raises(ValueError, match="Unknown command type"):
            CommandFactory.create_command(request)