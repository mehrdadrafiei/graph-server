import zmq
import json
import argparse
import logging
from typing import Dict, Any

class ZMQClient:
    def __init__(self, server_address: str = "tcp://localhost:5555"):
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.REQ)
        self.socket.connect(server_address)
        logging.info(f"Connected to server at {server_address}")

    def send_command(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Send a command to the server and return the response."""
        try:
            self.socket.send_string(json.dumps(request))
            response = self.socket.recv_string()
            return json.loads(response)
        except Exception as e:
            return {"error": f"Client error: {str(e)}"}

def main():
    parser = argparse.ArgumentParser(description='ZMQ Client')
    parser.add_argument('--type', choices=['os', 'compute'], required=True,
                        help='Command type (os or compute)')
    parser.add_argument('--cmd', help='Command name for OS commands')
    parser.add_argument('--params', nargs=argparse.REMAINDER,
                        help='Parameters for OS commands')
    parser.add_argument('--expr', help='Expression for compute commands')
    
    args = parser.parse_args()
    
    client = ZMQClient()
    
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

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    main()