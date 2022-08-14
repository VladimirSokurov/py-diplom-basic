import requests
import time
import json
import logging


class VkPhotos:
    def __init__(self, user_id: str):
        self.user_id = user_id

    def res(self):
        '''
        returns a list with user photos;
        need to put a vk token to dir file "token.txt"
        '''
        with open('token.txt') as file_obj:
            token = file_obj.read().strip()
        URL = 'https://api.vk.com/method/photos.get'
        params = {'owner_id': self.user_id,
                  'album_id': 'profile',
                  'extended': '1',
                  'access_token': token,
                  'v': '5.131',
                  'count': '5'
                  }
        res = requests.get(url=URL, params=params)
        photos_list = res.json()['response']['items']
        return photos_list

    def the_largest_photos(self):
        '''
        returns the names and references of photos to the dict
        '''
        photos_dict = {}
        photos_list_ = VkPhotos.res(self)
        for i in photos_list_:
            max_height = max([j['height'] for j in i['sizes']])
            name = str(i['likes']['count'])
            url = None
            for j in i['sizes']:
                if j['height'] == max_height:
                    url = j['url']
            if name not in photos_dict:
                photos_dict[name] = url
            else:
                name2 = f'{name}_{time.ctime(i["date"])}'
                photos_dict[name2] = j['url']
        return photos_dict

    def sizes_list(self):
        '''
        returns the list with the largest photos sizes
        '''
        sizes_list = []
        photos_list_ = VkPhotos.res(self)
        for i in photos_list_:
            max_height = max([j['height'] for j in i['sizes']])
            sizes_list.append(max_height)
        return sizes_list


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


def logger():
    logging.basicConfig(level='DEBUG')
    logger = logging.getLogger()
    logger.debug(f'LOGGER')


if __name__ == "__main__":
    user_id = input('Введите id пользователя vk\n')
    VK_user = VkPhotos(user_id)
    ya_disk_token = input('Введите токен пользователя Яндекс.Диск\n')
    uploader = YaUploader(ya_disk_token)

    VK_user.the_largest_photos()
    uploader.create_folder(VK_user.user_id)


    def upload_photos():
        logger()
        json_list = []
        id = 0
        for name, url in VkPhotos.the_largest_photos(VK_user).items():
            json_dict = {}
            disk_file_path = f'/{VK_user.user_id}/{name}'
            uploader.upload_file_to_disk(url, disk_file_path)
            json_dict['file_name'] = name
            size = VK_user.sizes_list()[id]
            json_dict['size'] = size
            json_list.append(json_dict)
            id += 1
        with open('file.json', 'a') as file_obj:
            json.dump(json_list, file_obj)


    upload_photos()
