import pytest
import asyncio
from src.server import ZMQServer


@pytest.fixture
def server():
    """Create a server instance for testing."""
    return ZMQServer("tcp://127.0.0.1:5555")