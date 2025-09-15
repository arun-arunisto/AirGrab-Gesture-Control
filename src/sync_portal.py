import asyncio
import threading
from websockets import serve, connect

# shared clipboard (in-memory on server)
shared_clipboard = {"text": ""}

# server 
async def handler(websocket):
    global shared_clipboard
    async for message in websocket:
        cmd, *data = message.split(":", 1)
        if cmd == "COPY":
            shared_clipboard["text"] = data[0] if data else ""
            await websocket.send("COPIED")
        elif cmd == "PASTE":
            await websocket.send(shared_clipboard["text"])

def start_server(host="0.0.0.0", port=8765):
    """
    Start clipboard websocket server in background thread.
    """
    async def run():
        async with serve(handler, host, port):
            await asyncio.Future() # keep running forever
    threading.Thread(target=asyncio.run, args=(run(),), daemon=True).start()
    print(f"📡 Clipboard server running at ws://{host}:{port}")

# Client
async def send_copy(content, server_ip="127.0.0.1", port=8765):
    uri = f"ws://{server_ip}:{port}"
    async with connect(uri) as websocket:
        await websocket.send(f"COPY:{content}")
        return await websocket.recv()

async def send_paste(server_ip="127.0.0.1", port=8765):
    uri = f"ws://{server_ip}:{port}"
    async with connect(uri) as websocket:
        await websocket.send("PASTE")
        return await websocket.recv()
