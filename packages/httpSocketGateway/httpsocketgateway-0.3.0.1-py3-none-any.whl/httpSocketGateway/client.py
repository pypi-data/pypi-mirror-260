import json
import _thread as thread
import time
from websocket._app import WebSocketApp
import requests
import os
from .utils import download_file, upload_files
from typing import Dict, List, Tuple

class WSClient:
    def __init__(self, host, port, reconnect=True, simple=False):
        self.host = host
        self.port = port
        self.wsurl = f"wss://{host}:{port}/ws"
        self.reconnect = reconnect
        self.simple = simple
        self.temporary_directory = "data/tmp/"
        os.makedirs(self.temporary_directory, exist_ok=True)
    
    def run(self):
        self.ws = WebSocketApp(self.wsurl,
                               on_message=self.on_message,
                               on_error=self.on_error,
                               on_close=self.on_close)
        self.ws.on_open = self.on_open
        self.thread = thread.start_new_thread(self.ws.run_forever, ())
        time.sleep(0.1)

    def on_message(self, ws, message):
        message = json.loads(message)
        files_path = []
        
        if not self.simple:
            for filename in message.get("filenames", []):
                file_path = os.path.join(self.temporary_directory, message["id"], filename)
                self.retrieve_file(id=message["id"], filename=filename, file_path=file_path)
                files_path.append(file_path)
        
        response, files_path = self.process_message(message["request"]["body"], files_path)

        if self.simple:
            self.send_json(json.dumps(response))
            return
        
        status_code = 500
        if "error" in response:
            response = {
                "error": "An error occurred"
                }
        else:
            status_code = 200
            
        response = {
            "id": message["id"],
            "type": "external-to-internal",
            "request": {
                "status": status_code,
                "method": message["request"]["method"],
                "endpoint": message["request"]["endpoint"],
                "headers": {
                    "Content-Type": "application/json"
                },
                "body": response
            },
            "dest": "",
            "filenames": files_path
        }
        self.send_json(json.dumps(response))
    
    def retrieve_file(self, id, filename, file_path):
        download_file(url=f"https://{self.host}:{self.port}/download/", id=id, filename=filename, file_path=file_path)
    
    def process_message(self, message, files_path=None) -> Tuple[Dict, List[str]]:
        print(f"Message received: {message}")
        print(f"Files path: {files_path}")
        # raise NotImplementedError("You must implement this method process_message")
        return {"success": "Hello World"}, []

    def on_error(self, ws, error):
        print(f"Error occurred: {error}")

    def on_close(self, ws, close_status_code, close_msg):
        print("Connection closed")
        #if self.reconnect:
        #    self.run()

    def on_open(self, ws):
        print("Connection established")

    def send_json(self, data):
        json_data = json.dumps(data)
        self.ws.send(json_data)

    def close(self):
        self.reconnect = False
        self.ws.close()
        os.rmdir(self.temporary_directory)
    
    def is_connected(self):
        if self.ws.sock is None:
            return False
        return self.ws.sock.connected
    
    def is_closed(self):
        if self.ws.sock is None:
            return True
        return not self.ws.sock.connected
    
    def upload_files(self, id, file_paths):
        upload_files(url=f"https://{self.host}:{self.port}/upload/", id=id, file_paths=file_paths)

# Exemple of use
if __name__ == "__main__":
    host = "127.0.0.1"
    port = 4200
    client = WSClient(host=host,
                             port=port
                             )
    client.run()
    try:
        time.sleep(60)
    except KeyboardInterrupt:
        client.close()
    except Exception as e:
        print(f"An error occurred: {e}")
