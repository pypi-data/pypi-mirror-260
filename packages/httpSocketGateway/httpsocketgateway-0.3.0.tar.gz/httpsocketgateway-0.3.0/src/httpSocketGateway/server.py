from fastapi import FastAPI, WebSocket, Request, WebSocketDisconnect, UploadFile, File, Form
from typing import Optional, List
import uvicorn
import uuid
import asyncio
import time
import json
import os
from fastapi.responses import FileResponse, JSONResponse
import re
import requests

class Gateway:
    def __init__(self):
        self.app = FastAPI()
        self.app.add_api_route("/", self.http_hello_world)
        self.app.add_api_route("/api", self.http_endpoint, methods=["POST"])
        self.app.add_api_route("/download", self.download_file, methods=["GET"])
        self.app.add_api_route("/upload", self.upload_files, methods=["POST"])
        self.app.add_websocket_route("/ws", self.websocket_endpoint)
        self.active_websocket: Optional[WebSocket] = None
        self.messages_wait = []
        self.temporary_directory = "data/tmp/"
        # test if the directory exists
        if not os.path.exists(self.temporary_directory):
            os.makedirs(self.temporary_directory)
    
    def __del__(self):
        # remove the temporary directory
        if os.path.exists(self.temporary_directory):
            os.rmdir(self.temporary_directory)
      
    async def http_hello_world(self):
        return JSONResponse(content={"success": "Hello World"}, status_code=200, media_type="application/json")

    async def upload_files(self, id: str, files: List[UploadFile] = File(None)):
        print("request id", id)

        if files is None:
            return JSONResponse(content={"error": "No file uploaded"}, status_code=400, media_type="application/json")
        
        os.makedirs(f"{self.temporary_directory}{id}", exist_ok=True)
        
        with open(f"{self.temporary_directory}{id}/.temp", "w") as f:
            f.write(str(int(time.time())))
        
        for file in files:
            with open(f"{self.temporary_directory}{id}/{file.filename}", "wb+") as file_object:
                file_object.write(await file.read())  # si les fichiers sont gros, envisagez de les traiter de manière streamée
        return JSONResponse(content={"success": "File uploaded"}, status_code=200, media_type="application/json")
    
    async def http_endpoint(self, request: Request, json_data: str = Form(...), files: List[UploadFile] = File(None)):
        # generate unique id
        id = uuid.uuid4().hex
        json_data = json.loads(json_data)

        # save the file or files to the temporary directory
        # create the directory if it does not exist
        if files is not None:
            os.makedirs(f"{self.temporary_directory}{id}", exist_ok=True)
        filenames = []
        if files is not None:
            for file in files:
                file_location = f"{self.temporary_directory}{id}/{file.filename}"
                print("file_location", file_location)
                with open(file_location, "wb+") as file_object:
                    file_object.write(await file.read())  # si les fichiers sont gros, envisagez de les traiter de manière streamée
                filenames.append(file.filename)
        send = {
            "id": id,
            "type": "internal-to-external",
            "request": {
                "method": request.method,
                "endpoint": request.url.path,
                "headers": dict(request.headers),
                "body": json_data
            },
            "dest": "",
            "filenames": filenames
            }
        if send["dest"] == "" or True: # http request not used
            if self.active_websocket:
                # send request to active websocket
                await self.active_websocket.send_json(send)
            else:
                return JSONResponse(content={"error": "No active WebSocket connection"}, status_code=500, media_type="application/json")
        else:
            await self.send_http(send)
        # wait for response
        response = await self.wait_response(id=id, timeout=60*2)
        content = response["request"]["body"]
        status_code = response["request"]["status"]
        return JSONResponse(content=content, status_code=status_code)
    
    async def wait_response(self, id: str, timeout=None):
        start = time.time()
        if timeout is None:
            timeout = 60*2
        while time.time() - start < timeout:
            if self.messages_wait != []:
                for i, message in enumerate(self.messages_wait):
                    if message["id"] == id:
                        del self.messages_wait[i]
                        return message
            await asyncio.sleep(0.1)
        return {
            "id": id,
            "type": "external-to-internal",
            "response": {
                "status": "408",
                "headers": {
                    "Content-Type": "application/json"
                },
                "body": {
                    "error": "Timeout"
                }
            },
            "filenames": []
        }

    async def websocket_endpoint(self, websocket: WebSocket):
        self.active_websocket = websocket # .
        await websocket.accept()
        try:
            while True:
                data = await websocket.receive_json()
                data = json.loads(data)
                if data["type"] == "external-to-internal":
                    self.messages_wait.append(data)
        except WebSocketDisconnect:
            print("Client disconnected from WebSocket")
        finally:
            self.active_websocket = None
    
    # how limit request, need limit to external ip only
    async def send_http(self, request: dict):
        if request["dest"] == "":
            raise ValueError("Destination not found")
        if request["dest"].startswith("http://") or request["dest"].startswith("https://"):
            try:
                response = requests.post(request["dest"], json=request)
                if response.status_code == 200:
                    return response.json()
                else:
                    # .
                    return {
                        "id": request["id"],
                        "type": "external-to-internal",
                        "request": {
                            "status": response.status_code,
                            "method": response.request.method,
                            "endpoint": response.url,
                            "headers": dict(response.headers),
                            "body": json.loads(response.json())
                        },
                        "filenames": response.json().get("filenames", [])
                    }
            except Exception as e:
                return {
                    "id": request["id"],
                    "type": "external-to-internal",
                    "request": {
                        "status": "500",
                        "method": "POST",
                        "endpoint": request["dest"],
                        "headers": {},
                        "body": {
                            "error": str(e)
                        }
                    },
                    "filenames": []
                }
        else:
            return {
                "id": request["id"],
                "type": "external-to-internal",
                "request": {
                    "status": "400",
                    "method": "POST",
                    "endpoint": request["dest"],
                    "headers": {},
                    "body": {
                        "error": "Invalid destination"
                    }
                },
                "filenames": []
            }
    
    async def download_file(self, id: str, filename: str):
        # check if file exists
        file_path = f"{self.temporary_directory}{id}/{filename}"
        if not os.path.exists(file_path):
            return JSONResponse(content={"error": "File not found"}, status_code=404, media_type="application/json")
        return FileResponse(file_path, filename=filename)

    def run(self, host, port):
        uvicorn.run(self.app, host=host, port=port)

if __name__ == "__main__":
    gateway = Gateway()
    os.environ["LAURE_SELF_HOST"] = "127.0.0.1"
    os.environ["LAURE_SELF_PORT"] = "4200"
    gateway.run(host=os.environ["LAURE_SELF_HOST"], port=os.environ["LAURE_SELF_PORT"])

