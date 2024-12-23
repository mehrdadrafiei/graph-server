import asyncio
import json
import logging
import os

import zmq.asyncio
from dotenv import load_dotenv

from graph_server.command_factory import CommandFactory
from graph_server.exceptions import CommandError
from graph_server.validators import JSONRequestValidator

load_dotenv()

class ZMQServer:
    """Main server class"""
    
    def __init__(self, log_level=logging.INFO):
        host = os.getenv('ZMQ_SERVER_HOST', '127.0.0.1')
        port = os.getenv('ZMQ_SERVER_PORT', '5555')
        self.bind_address = f"tcp://{host}:{port}"
        self.validator = JSONRequestValidator()
        self.command_factory = CommandFactory()
        self.is_running = False
        self.tasks = set()  # Track running tasks
        
        # Configure logging
        logging.basicConfig(
            level=log_level,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger(__name__)

    async def handle_request(self, msg_id: bytes, request_json: str, socket) -> None:
        """Process a single client request."""
        try:
            # Parse and validate request
            request = json.loads(request_json)
            self.validator.validate(request)
            
            command = self.command_factory.create_command(request)
            response = await command.execute()
            
            await socket.send_multipart([msg_id, json.dumps(response).encode()])
            
        except json.JSONDecodeError:
            await socket.send_multipart([msg_id, json.dumps({"error": "Invalid JSON format"}).encode()])
        except CommandError as e:
            await socket.send_multipart([
                msg_id,
                json.dumps({
                    "error": str(e),
                    "command": getattr(e, 'command', None)
                }).encode()
            ])
        except Exception as e:
            self.logger.error(f"Unexpected error: {str(e)}", exc_info=True)
            await socket.send_multipart([
                msg_id,
                json.dumps({"error": "Internal server error"}).encode()
            ])

    async def start(self) -> None:
        """Start the ZMQ server."""
        self.is_running = True
        self.logger.info(f"Server starting on {self.bind_address}")
        
        context = zmq.asyncio.Context()
        socket = context.socket(zmq.ROUTER)
        socket.bind(self.bind_address)
        
        try:
            self.logger.info("Server started successfully")
            while self.is_running:
                try:
                    # Receive message frames [id, message]
                    frames = await socket.recv_multipart()
                    if len(frames) != 2:
                        continue
                        
                    msg_id, message = frames
                    self.logger.info(f"Received request from {msg_id}: {message.decode()}")
                    
                    # Create new task for each request
                    task = asyncio.create_task(
                        self.handle_request(msg_id, message.decode(), socket)
                    )
                    self.tasks.add(task)
                    task.add_done_callback(self.tasks.discard)
                    
                except asyncio.CancelledError:
                    self.logger.info("Server shutdown initiated")
                    break
                except Exception as e:
                    self.logger.error(f"Error processing request: {str(e)}", exc_info=True)
        finally:
            # Wait for all tasks to complete
            if self.tasks:
                await asyncio.gather(*self.tasks, return_exceptions=True)
            socket.close()
            context.term()
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
