import json
import logging
import YaDisc
import Vk
from Vk import VkPhotos
from YaDisc import YaUploader

user_id = Vk.screen_name()
VK_user = VkPhotos(user_id)

ya_disk_token = YaDisc.ya_disk_token()
uploader = YaUploader(ya_disk_token)
VK_user.the_largest_photos()
uploader.create_folder(VK_user.user_id)


def logger():
    logging.basicConfig(level='DEBUG')
    logger = logging.getLogger()
    logger.debug(f'LOGGER')


def create_json():
    logger()
    json_list = []
    id = 0
    for name, url in VkPhotos.the_largest_photos(VK_user).items():
        json_dict = {}
        json_dict['file_name'] = name
        size = VK_user.sizes_list()[id]
        json_dict['size'] = size
        json_list.append(json_dict)
        id += 1
    with open('file.json', 'a') as file_obj:
        json.dump(json_list, file_obj)


def upload_photos():
    for name, url in VkPhotos.the_largest_photos(VK_user).items():
        disk_file_path = f'/{VK_user.user_id}/{name}'
        uploader.upload_file_to_disk(url, disk_file_path)


if __name__ == "__main__":
    create_json()
    upload_photos()
