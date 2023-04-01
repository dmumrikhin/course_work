import requests
import json
# from pprint import pprint

# with open('/Users/a1/Google Диск/мое/Нетология/hw/vk_token.txt', 'r') as file_object:
#     vk_token = file_object.read().strip()


class VkUser:
    url = 'https://api.vk.com/method/'
    def __init__(self, vk_token, version=5.131):
        self.params = {
            'access_token': vk_token,
            'v': version    
        }

    def photos_list(self, owner_id=None):
        user_info_url = self.url + 'photos.get'
        photos_list_params = {
            'owner_id': owner_id,
            'album_id': 'profile',
            'extended': 1,
            'photo_sizes': 0,
            'count': 200
        }
        req = requests.get(user_info_url, params={**self.params, **photos_list_params}).json()
        print(f"Обнаружено {req['response']['count']} фотографий")
        count = 0
        result_file = []
        for item in req['response']['items']:
            photo = {}
            for size in item['sizes']:
                if not photo or photo['size'] < int(size['height'])*int(size['width']):
                    photo['name'] = f"{item['likes']['count']}_{item['date']}.jpg" 
                    photo['size'] = int(size['height'])*int(size['width'])
                    photo['size_letter'] = size['type']
                    photo['url'] = size['url']
            response = requests.get(photo['url'])
            with open(f"backup/{photo['name']}", 'wb') as image:
                image.write(response.content)
            count += 1
            print(f"Скачано {count} из {req['response']['count']} фотографий.")
            result_file.append({"file_name": photo['name'], "size": photo['size_letter']})
            photo = {}

        with open('result.json', 'w') as f:
            json.dump(result_file, f, indent=2)



        #     vk_photos[item['id']] = int(max(photo_sizes))          
        # vk_photos = dict(sorted(vk_photos.items(), key=lambda item: item[1], reverse=True))
        # vk_photos_id = list(vk_photos.keys())[0:5]
        # for item in req['response']['items']:
        #     if item['id'] in vk_photos_id:
        #         for size in item['sizes']:
        #             if int(size['height'])*int(size['width']) == vk_photos[item['id']]:
        #                 vk_photos_url.append(size['url'])            
        
        
        # return vk_photos_url  

    # def get_photos(self):
    #     vk_photos_url = self.photos_list()
    #     print(vk_photos_url)







# vk_client = VkUser(vk_token)

# vk_client.photos_list(788770602)


