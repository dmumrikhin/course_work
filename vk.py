import requests
import json

class VkUser:
    url = 'https://api.vk.com/method/'
    def __init__(self, vk_token, version=5.131):
        self.params = {
            'access_token': vk_token,
            'v': version    
        }

    def get_id(self, vk_id_screen_name):
        get_id_url = self.url + 'utils.resolveScreenName'
        get_id_params = {
            'screen_name': vk_id_screen_name
        }
        req = requests.get(get_id_url, params={**self.params, **get_id_params
                                               }).json()
        if len(req['response']) == 0:
            vk_id = vk_id_screen_name
        else:
            vk_id = req['response']['object_id']
        return(vk_id) 
    
    def json_save_to_disc(self, result):
        with open('result.json', 'w') as f:
            json.dump(result, f, indent=2)

    def photos_list(self, owner_id=None):
        user_info_url = self.url + 'photos.get'
        photos_list_params = {
            'owner_id': owner_id,
            'album_id': 'profile',
            'extended': 1,
            'photo_sizes': 0,
            'count': 200
        }
        req = requests.get(user_info_url, params={**self.params, **photos_list_params
                                                  }).json()
        if 'error' in req:
            return('input error')
        else:
            print(f"Обнаружено {req['response']['count']} фотографий")
            count = 0
            result_file = []
            for item in req['response']['items']:
                photo = {}
                for size in item['sizes']:
                    if not photo or photo['size'] < int(size['height']
                                                        )*int(size['width']):
                        photo['name'] = f"{item['likes']['count']}_{item['date']}.jpg" 
                        photo['size'] = int(size['height'])*int(size['width'])
                        photo['size_letter'] = size['type']
                        photo['url'] = size['url']
                response = requests.get(photo['url'])
                result_file.append({"file_name": photo['name'
                                                    ], "size": photo['size_letter'], 
                    "url": photo['url']})
                photo = {}
            self.json_save_to_disc(result_file)

