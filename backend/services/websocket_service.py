import asyncio
import websockets

# Store connected clients
connected_clients = set()

async def start_server():
    """Start WebSocket server."""
    async with websockets.serve(handler, "localhost", 8765):
        print("WebSocket server started on ws://localhost:8765")
        await asyncio.Future()
        
async def handler(websocket, path):
    """Register new clients and keep them connected."""
    connected_clients.add(websocket)
    try:
        await websocket.wait_closed()  # Keep connection open
    finally:
        connected_clients.remove(websocket)
        
# Function to send messages to all connected clients
async def send_message(message):
    """Send message to all connected clients."""
    if connected_clients:
        await asyncio.wait([client.send(message) for client in connected_clients])
    else:
        print("No clients connected, message not sent.")