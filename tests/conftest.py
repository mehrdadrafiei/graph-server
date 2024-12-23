from unittest.mock import AsyncMock

import pytest

from src.graph_server.server import ZMQServer


@pytest.fixture
def server():
    """Create a server instance for testing."""
    return ZMQServer(log_level="ERROR")

@pytest.fixture
def mock_socket():
    socket = AsyncMock()
    socket.send_multipart = AsyncMock()
    return socket
