import zmq.asyncio
import json
import logging
import asyncio
import os
from dotenv import load_dotenv
from contextlib import asynccontextmanager
from exceptions import CommandError
from validators import JSONRequestValidator
from command_factory import CommandFactory

load_dotenv()

class ZMQServer:
    """Main server class implementing the Facade pattern."""
    
    def __init__(self, log_level=logging.INFO):
        host = os.getenv('ZMQ_SERVER_HOST', '127.0.0.1')
        port = os.getenv('ZMQ_SERVER_PORT', '5555')
        self.bind_address = f"tcp://{host}:{port}"
        self.validator = JSONRequestValidator()
        self.command_factory = CommandFactory()
        self.is_running = False
        
        # Configure logging
        logging.basicConfig(
            level=log_level,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger(__name__)
    
    async def handle_request(self, request_json: str) -> str:
        """Process a single client request."""
        try:
            # Parse and validate request
            request = json.loads(request_json)
            self.validator.validate(request)
            
            # Create and execute command
            command = self.command_factory.create_command(request)
            response = await command.execute()
            
            return json.dumps(response)
            
        except json.JSONDecodeError:
            return json.dumps({"error": "Invalid JSON format"})
        except CommandError as e:
            return json.dumps({
                "error": str(e),
                "command": getattr(e, 'command', None)
            })
        except Exception as e:
            self.logger.error(f"Unexpected error: {str(e)}", exc_info=True)
            return json.dumps({"error": "Internal server error"})
    
    @asynccontextmanager
    async def server_context(self):
        """Context manager for server socket."""
        context = zmq.asyncio.Context()
        socket = context.socket(zmq.REP)
        socket.bind(self.bind_address)
        try:
            yield socket
        finally:
            socket.close()
            context.term()
    
    async def start(self) -> None:
        """Start the ZMQ server."""
        self.is_running = True
        self.logger.info(f"Server starting on {self.bind_address}")
        
        async with self.server_context() as socket:
            self.logger.info("Server started successfully")
            while self.is_running:
                try:
                    request_json = await socket.recv_string()
                    self.logger.info(f"Received request: {request_json}")
                    
                    response = await self.handle_request(request_json)
                    await socket.send_string(response)
                    
                except asyncio.CancelledError:
                    self.logger.info("Server shutdown initiated")
                    break
                except Exception as e:
                    self.logger.error(f"Error processing request: {str(e)}", exc_info=True)
                    await socket.send_string(
                        json.dumps({"error": "Internal server error"})
                    )
        
        self.logger.info("Server shut down")
    
    def stop(self) -> None:
        """Stop the server."""
        self.is_running = False
        self.logger.info("Server stop requested")


def main():
    server = ZMQServer()
    try:
        asyncio.run(server.start())
    except KeyboardInterrupt:
        print("Server stopped by user")


if __name__ == "__main__":
    main()
