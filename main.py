import json
from yandex import YaUploader
from vk import VkUser

with open('/Users/a1/Google Диск/мое/Нетология/hw/vk_token.txt', 'r') as file_object:
    vk_token = file_object.read().strip()
with open('/Users/a1/Google Диск/мое/Нетология/hw/ya_token.txt', 'r') as file_object:
    ya_token = file_object.read().strip()

vk_id = input('Введите id пользователя в ВК: ')
photos_number = input('Введите количество фото для загрузки на ЯД')


if __name__ == '__main__':
    if vk_id == '':
        vk_id = 788770602
    if photos_number == '':
        photos_number = 5
    vk_client = VkUser(vk_token)
    vk_client.photos_list(vk_id)

    YaUploader(ya_token).create_new_folder()

    with open ('result.json') as f:
        photos_list = json.load(f)
        photos_list.sort(key=lambda dictionary: dictionary['size'], reverse = True)        
        photos_uploaded = 0
        for photo in photos_list:
            if photos_uploaded < photos_number: 
                disk_file_path = f"course_work/{photo['file_name']}"
                filename = f"backup/{photo['file_name']}"
                ya = YaUploader(ya_token)
                ya.upload_file_to_disk(disk_file_path, filename)        
                photos_uploaded += 1
                print(f'Загружено фото {photos_uploaded} из {photos_number}')    



