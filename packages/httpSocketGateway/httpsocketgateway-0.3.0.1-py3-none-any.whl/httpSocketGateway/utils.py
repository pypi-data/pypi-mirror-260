import requests
import os
import json

def path_to_file(file_path):
    if not os.path.isfile(file_path):
        print(f"The file {file_path} does not exist")
        return
    with open(file_path, "rb") as f:
        return f.read()

def paths_to_files(file_paths):
    files = []
    for file_path in file_paths:
        file_content = path_to_file(file_path)
        file_name = os.path.basename(file_path)
        files.append(("files", (file_name, file_content)))
    return files

def upload_files(url, id, file_paths):
    files = paths_to_files(file_paths)
    params = {"id": id}
    response = requests.post(url, files=files, params=params)
    if response.status_code == 200:
        pass
        # print("Files uploaded successfully")
    else:
        # print("Error while uploading files")
        if response.content:
            print("Réponse du serveur : ", response.content.decode())
        # raise Exception("Error while uploading files")

def download_file(url, id, filename, file_path):
    response = requests.get(url, params={"id": id, "filename": filename})
    if response.status_code == 200:
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, "wb+") as file:
            file.write(response.content)
    else:
        print("error while downloading file")
        if response.content:
            print("response from server : ", response.content.decode())

def send_http_request(url, file_paths=[], **datas):
    files = paths_to_files(file_paths)
    data = {
        "json_data": json.dumps(datas)
    }
    try:
        response = requests.post(url, data=data, files=files)
        if response.status_code == 200:
            return response.json()
        else:
            print("error while sending http request")
            if response.content:
                print("response from server : ", response.content.decode())
    except Exception as e:
        return {
            "error": "error while sending http request : " + str(e),
        }

if __name__ == "__main__":
    pass
    # print(send_http_request("http://127.0.0.1:4200/api", file_paths=["./test.txt", "./test2.txt"], key="value"))
    # upload_files("http://127.0.0.1:4200/upload", "6a506994e8ce496da6854cc07b116c08", ["./test.txt"])
    # download_file("http://127.0.0.1:4200/download", "6a506994e8ce496da6854cc07b116c08", "test.txt", "./test2.txt")
