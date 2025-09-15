import asyncio
import time
import threading
from src.sync_portal import start_server, send_copy, send_paste

def run_server():
    """
    Start the server in a background thread.
    """
    start_server(host="127.0.0.1", port=8765)
    while True:
        time.sleep(1)
    

def test_sync_portal():
    # start server in background thread
    server_thread = threading.Thread(target=run_server, daemon=True)
    server_thread.start()

    time.sleep(1) # give server time to start

    # 1. Copy some text remotely
    text_to_copy = "Hello from System AI"
    result = asyncio.run(send_copy(text_to_copy, server_ip="127.0.0.1"))
    print("Server Response (COPY):",result)

    #2. Paste the text remotely
    pasted_text = asyncio.run(send_paste(server_ip="127.0.0.1"))
    print("Server Response (PASTE):",pasted_text)

    assert pasted_text == text_to_copy, "Clipboard sync failed"


if __name__ == "__main__":
    test_sync_portal()