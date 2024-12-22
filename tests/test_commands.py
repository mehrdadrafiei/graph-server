import pytest
from graph_server.commands import ComputeCommand, OSCommand
from graph_server.exceptions import CommandExecutionError

@pytest.mark.asyncio(loop_scope="module")
class TestOSCommand:
    async def test_valid_ls_command(self):
        command = OSCommand("ls", ["-l"])
        result = await command.execute()
        assert "given_os_command" in result
        assert "result" in result

    async def test_invalid_command(self):
        with pytest.raises(CommandExecutionError):
            command = OSCommand("rm", ["-rf", "/"])
            await command.execute()

    async def test_command_not_found(self):
        with pytest.raises(CommandExecutionError, match="Command 'nonexistent' not allowed"):
            command = OSCommand("nonexistent", [])
            await command.execute()

@pytest.mark.asyncio(loop_scope="module")
class TestComputeCommand:
    async def test_valid_expression(self):
        command = ComputeCommand("2 + 2")
        result = await command.execute()
        assert result["result"] == "4"

    async def test_complex_expression(self):
        command = ComputeCommand("(30 + 10) * 5 + 1")
        result = await command.execute()
        assert result["result"] == "201"

    async def test_invalid_expression(self):
        with pytest.raises(CommandExecutionError, match="Expression evaluation failed"):
            command = ComputeCommand("2 + ")
            await command.execute()

    async def test_unsafe_expression(self):
        with pytest.raises(CommandExecutionError):
            command = ComputeCommand("__import__('os').system('ls')")
            await command.execute()