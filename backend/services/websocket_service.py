import asyncio
import websockets
import os
from dotenv import load_dotenv

# Store connected clients safely
connected_clients = set()
clients_lock = asyncio.Lock()  # Prevent concurrent modification of set

async def handler(websocket, path):
    """Handle WebSocket connections."""
    async with clients_lock:
        connected_clients.add(websocket)
    
    print(f"New connection: {websocket.remote_address}")

    try:
        await websocket.wait_closed()  # Keep connection open
    except websockets.exceptions.ConnectionClosedError:
        print("Client disconnected unexpectedly")
    finally:
        async with clients_lock:
            connected_clients.remove(websocket)
        print(f"Connection closed: {websocket.remote_address}")

async def start_server():
    """Start WebSocket server in the background."""
    print("Starting WebSocket server...")
    load_dotenv()
    # Get WebSocket host from environment variables
    websocket_host = os.getenv("WEBSOCKET_HOST", "0.0.0.0")  # Default to 0.0.0.0 if not set
    websocket_port = int(os.getenv("WEBSOCKET_PORT", 10000))  # Default to 10000 if not set

    async with websockets.serve(handler, websocket_host, websocket_port):
        print(f"WebSocket server running on ws://{websocket_host}:{websocket_port}")
        await asyncio.Future()   # Keep running forever

async def send_message(message):
    """Send message to all connected clients."""
    async with clients_lock:
        if connected_clients:
            await asyncio.gather(*(client.send(message) for client in connected_clients))
        else:
            print("No clients connected, message not sent.")

