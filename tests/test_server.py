import pytest
import json
from src.server import ZMQServer

@pytest.mark.asyncio
class TestZMQServer:
    async def test_handle_valid_os_request(self, server):
        request = json.dumps({
            "command_type": "os",
            "command_name": "ls",
            "parameters": ["-l"]
        })
        response = await server.handle_request(request)
        response_dict = json.loads(response)
        assert "given_os_command" in response_dict
        assert "result" in response_dict

    async def test_handle_valid_compute_request(self, server):
        request = json.dumps({
            "command_type": "compute",
            "expression": "2 + 2"
        })
        response = await server.handle_request(request)
        response_dict = json.loads(response)
        assert response_dict["result"] == "4"

    async def test_handle_invalid_json(self, server):
        request = "invalid json"
        response = await server.handle_request(request)
        response_dict = json.loads(response)
        assert "error" in response_dict
        assert "Invalid JSON format" in response_dict["error"]

    async def test_handle_invalid_command_type(self, server):
        request = json.dumps({
            "command_type": "invalid"
        })
        response = await server.handle_request(request)
        response_dict = json.loads(response)
        assert "error" in response_dict