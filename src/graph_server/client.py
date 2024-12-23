import argparse
import json
import logging
import uuid
from typing import Any, Dict

import zmq


class ZMQClient:
    def __init__(self, server_address: str = "tcp://localhost:5555"):
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.DEALER)
        # Generate a unique client ID
        self.client_id = str(uuid.uuid4()).encode()
        self.socket.identity = self.client_id
        self.socket.connect(server_address)
        logging.info(f"Connected to server at {server_address}")

    def send_command(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Send a command to the server and return the response."""
        try:
            # Send message frames
            message = json.dumps(request).encode()
            self.socket.send_multipart([message])
            
            # Receive response
            response = self.socket.recv_multipart()
            return json.loads(response[0].decode())
        except Exception as e:
            return {"error": f"Client error: {str(e)}"}

    def close(self):
        """Close the client connection."""
        self.socket.close()
        self.context.term()

def main():
    parser = argparse.ArgumentParser(description='ZMQ Client')
    parser.add_argument('--type', choices=['os', 'compute'], required=True, help='Command type (os or compute)')
    parser.add_argument('--cmd', help='Command name for OS commands')
    parser.add_argument('--params', nargs=argparse.REMAINDER, help='Parameters for OS commands')
    parser.add_argument('--expr', help='Expression for compute commands')
    
    args = parser.parse_args()
    
    client = ZMQClient()
    
    try:
        if args.type == 'os':
            if not args.cmd:
                parser.error("--cmd is required for OS commands")
            request = {
                "command_type": "os",
                "command_name": args.cmd,
                "parameters": args.params if args.params else []
            }
        else:  # compute
            if not args.expr:
                parser.error("--expr is required for compute commands")
            request = {
                "command_type": "compute",
                "expression": args.expr
            }
        
        response = client.send_command(request)
        print(json.dumps(response, indent=2))
    finally:
        client.close()

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    main()