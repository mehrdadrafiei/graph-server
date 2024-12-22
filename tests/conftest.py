import pytest
from src.graph_server.server import ZMQServer


@pytest.fixture
def server():
    """Create a server instance for testing."""
    return ZMQServer()