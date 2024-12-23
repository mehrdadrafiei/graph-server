import json

import pytest


@pytest.mark.asyncio
class TestZMQServer:
    async def test_handle_valid_os_request(self, server, mock_socket):
        client_id = b'test_client'
        request = {
            "command_type": "os",
            "command_name": "ls",
            "parameters": ["-l"]
        }
        
        await server.handle_request(client_id, json.dumps(request), mock_socket)

        mock_socket.send_multipart.assert_called_once()
        call_args = mock_socket.send_multipart.call_args[0][0]
        assert call_args[0] == client_id
        response_dict = json.loads(call_args[1].decode())
        assert "given_os_command" in response_dict
        assert "result" in response_dict

    async def test_handle_valid_compute_request(self, server, mock_socket):
        client_id = b'test_client'
        request = {
            "command_type": "compute",
            "expression": "2 + 2"
        }

        await server.handle_request(client_id, json.dumps(request), mock_socket)

        mock_socket.send_multipart.assert_called_once()
        call_args = mock_socket.send_multipart.call_args[0][0]
        assert call_args[0] == client_id
        response_dict = json.loads(call_args[1].decode())
        assert response_dict["result"] == "4"

    async def test_handle_invalid_json(self, server, mock_socket):
        client_id = b'test_client'
        request = "invalid json"
        
        await server.handle_request(client_id, request, mock_socket)

        mock_socket.send_multipart.assert_called_once()
        call_args = mock_socket.send_multipart.call_args[0][0]
        assert call_args[0] == client_id
        response_dict = json.loads(call_args[1].decode())
        assert "error" in response_dict
        assert "Invalid JSON format" in response_dict["error"]

    async def test_handle_invalid_command_type(self, server, mock_socket):
        client_id = b'test_client'
        request = {
            "command_type": "invalid"
        }
        
        await server.handle_request(client_id, json.dumps(request), mock_socket)

        mock_socket.send_multipart.assert_called_once()
        call_args = mock_socket.send_multipart.call_args[0][0]
        assert call_args[0] == client_id
        response_dict = json.loads(call_args[1].decode())
        assert "error" in response_dict
