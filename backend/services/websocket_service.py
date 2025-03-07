import asyncio
import websockets

# Store connected clients safely
connected_clients = set()
clients_lock = asyncio.Lock()  # Prevent concurrent modification of set

async def handler(websocket, path):
    """Handle WebSocket connections."""
    async with clients_lock:  # Ensure thread safety
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
    """Start WebSocket server on 0.0.0.0 for Render compatibility."""
    async with websockets.serve(handler, "0.0.0.0", 8765):
        print("WebSocket server started on ws://0.0.0.0:8765")
        await asyncio.Future()  # Keep running forever

async def send_message(message):
    """Send message to all connected clients."""
    async with clients_lock:
        if connected_clients:
            await asyncio.gather(*(client.send(message) for client in connected_clients))
        else:
            print("No clients connected, message not sent.")

if __name__ == "__main__":
    asyncio.run(start_server())
