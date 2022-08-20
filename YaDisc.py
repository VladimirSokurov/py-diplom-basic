import requests
import configparser

def ya_disk_token():
    config = configparser.ConfigParser()
    config.read("settings.ini")
    ya_disk_token = config["ya.disc"]["token"]
    return ya_disk_token


class YaUploader:
    def __init__(self, token: str):
        self.token = token

    def get_headers(self):
        return {
            'Content-Type': 'application/json',
            'Authorization': f'OAuth {self.token}'
        }

    def create_folder(self, user_id):
        '''
        creates a folder in yandex.disc
        '''
        upload_url = "https://cloud-api.yandex.net/v1/disk/resources"
        headers = self.get_headers()
        params = {"path": user_id}
        res = requests.put(url=upload_url, headers=headers, params=params)

    def upload_file_to_disk(self, url, disk_file_path):
        '''
        uploads the largest photos
        '''
        upload_url = "https://cloud-api.yandex.net/v1/disk/resources/upload"
        headers = self.get_headers()
        params = {"url": url, "path": disk_file_path, "overwrite": "true"}
        res = requests.post(url=upload_url, headers=headers, params=params)
