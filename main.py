import json
import sys

from yandex import YaUploader
from vk import VkUser

import configparser

config = configparser.ConfigParser()
config.read('/Users/a1/Google Диск/мое/Нетология/hw/settings.ini')
vk_token = config['Course_work']['vk_token']
ya_token = config['Course_work']['ya_token']

vk_id_screen_name = input('Введите id пользователя или никнейм в ВК: ')
photos_number = input('Введите количество фото для загрузки на ЯД: ')

if __name__ == '__main__':
    vk_client = VkUser(vk_token)
    vk_id = vk_client.get_id(vk_id_screen_name)
    if vk_client.photos_list(vk_id) == 'input error':
        print('Введен неправильный id или никнейм')
        quit()
    YaUploader(ya_token).create_new_folder()
    with open ('result.json') as f:
        photos_list = json.load(f)
        photos_list.sort(key=lambda dictionary: dictionary['size'
                                                        ], reverse=True)        
        photos_uploaded = 0
        for photo in photos_list:
            if photos_uploaded < photos_number: 
                disk_file_path = f"course_work/{photo['file_name']}"
                source_link = photo['url']
                ya = YaUploader(ya_token)
                ya.upload_file_to_disk(disk_file_path, source_link) 
                photos_uploaded += 1
                print(f'Загружено фото {photos_uploaded} из {photos_number}')    

