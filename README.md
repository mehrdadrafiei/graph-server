# ZMQ Command Server

A client-server application that processes system commands and mathematical expressions using ZMQ.

## Requirements

- Python 3.13 or higher
- Virtual environment (recommended)

# Docker Usage

## Running the Server
```bash
# Build and start the server
docker compose up server

# Or in detached mode
docker compose up -d server
```

## Running Tests
```bash
# Run all tests
docker compose run --rm tests
```

## Development
The source code is mounted as a volume, so you can make changes and they'll be reflected immediately.

## Client Examples
```bash
# Run a command using the server container
docker compose exec server python -m src.client --type compute --expr "2 + 2"

# Or OS command
docker compose exec server python -m src.client --type os --cmd ls --params -l
```

## Installation

1. Create and activate a virtual environment:
```bash
# Linux/macOS
python3 -m venv .venv
source .venv/bin/activate

# Windows
python -m venv .venv
.venv\Scripts\activate
```

2. Install the package:
```bash
pip install -e .
```

## Running the Application

### Method 1: Using Command Line Tools

1. Start the server:
```bash
# Using the installed entry point
graph-server

# Or using the module directly
python -m server
```

2. In another terminal, use the client:
```bash
# For OS commands
python -m client --type os --cmd ls --params -l

# For compute commands
python -m client --type compute --expr "2 + 2"
```

### Method 2: Using Python Code

1. Start the server:
```python
from server import ZMQServer
import asyncio

server = ZMQServer()
asyncio.run(server.start())
```

2. In another Python script, use the client:
```python
from client import ZMQClient

client = ZMQClient()

# OS command example
response = client.send_command({
    "command_type": "os",
    "command_name": "ls",
    "parameters": ["-l"]
})
print(response)

# Compute example
response = client.send_command({
    "command_type": "compute",
    "expression": "(30 + 10) * 5 + 1"
})
print(response)
```

## Running Tests

```bash
# Run all tests
pytest

# Run tests with coverage
pytest --cov=graph_server

# Generate coverage report
pytest --cov=graph_server --cov-report=html
```

## Example Commands

1. List directory contents:
```bash
python -m client --type os --cmd ls --params -l
```

2. Calculate expression:
```bash
python -m client --type compute --expr "(30 + 10) * 5 + 1"
```

## Project Structure

```
graph_server/
├── src/
│   ├── __init__.py
│   ├── server.py         # Server implementation
│   ├── client.py         # Client implementation
│   ├── commands.py       # Command implementations
│   ├── command_factory.py # Command creation
│   ├── validators.py     # Request validation
│   └── exceptions.py     # Custom exceptions
└── tests/                # Test suite
```

## Development

1. Install development dependencies:
```bash
pip install -e ".[dev]"
```

2. Run linting:
```bash
flake8 src/
```

3. Run type checking:
```bash
mypy src/
```

## Troubleshooting

1. Port already in use:
```bash
# Change the port in the server initialization
graph-server --port 5556
```

2. Connection refused:
```bash
# Make sure the server is running and the port matches
python -m client --port 5556 --type os --cmd ls
```

## Common Issues

1. If you see "Address already in use":
   - The server is already running or the port is blocked
   - Kill the existing process or use a different port

2. If commands fail:
   - Check if the command is in the allowed list
   - Verify the command exists on your system
   - Check the parameters are correct

## Security Notes

- Only whitelisted OS commands are allowed
- Mathematical expressions are safely evaluated
- Input is validated before processing