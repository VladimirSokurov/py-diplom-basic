import requests
import time
import configparser

config = configparser.ConfigParser()
config.read("settings.ini")
token = config["vk"]["token"]

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
