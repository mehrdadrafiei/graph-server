
# ZMQ Command Server

A client-server application using ZMQ to process system commands and mathematical expressions.

## Requirements

- Python 3.12+
- Virtual environment (recommended)

## Quick Start

### Docker

#### Start Server
```bash
docker compose up server
```

#### Run Tests
```bash
docker compose run --rm tests
```

#### Use the Client
1. OS Command:
   ```bash
   docker compose exec server python -m graph_server.client --type os --cmd ls --params -l
   ```
2. Compute Expression:
   ```bash
   docker compose exec server python -m graph_server.client --type compute --expr "2 + 2"
   ```

### Manual Installation

1. Set up a virtual environment:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate  # Linux/macOS
   .venv\Scripts\activate     # Windows
   ```

2. Install dependencies:
   ```bash
   pip install -e .
   ```

3. Start the server:
   ```bash
   graph-server
   ```

4. Use the client:
   ```bash
   python -m client --type os --cmd ls --params -l
   python -m client --type compute --expr "2 + 2"
   ```

## Testing

```bash
pytest  # Run tests
pytest --cov=graph_server --cov-report=html  # Coverage report
```

## Security

- Only whitelisted OS commands are allowed.
- Mathematical expressions are safely evaluated.
