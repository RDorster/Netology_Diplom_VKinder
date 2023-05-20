from datetime import datetime
import vk_api
from config import access_token


class VkTools():
    def __init__(self, access_token):
        self.api = vk_api.VkApi(token=access_token)

    def get_profile_info(self, user_id):
        # Получение информации о пользователе по id
        fields = 'city,bdate,sex'
        info = self.api.method('users.get', {'user_ids': user_id, 'fields': fields})[0]
        user_info = {
            'id': info['id'],
            'name': f"{info['first_name']} {info['last_name']}",
            'bdate': info.get('bdate', None),
            'city': info['city']['id'] if 'city' in info else None,
            'sex': info.get('sex', None),
        }
        return user_info

    def search_users(self, params):
        # Поиск пользователей, удовлетворяющих заданным параметрам
        sex = 1 if params['sex'] == 2 else 2
        city = params['city']
        user_year = int(params['bdate'].split('.')[-1])
        age = datetime.now().year - user_year
        age_from = age - 5
        age_to = age + 5
        users = self.api.method('users.search', {
            'count': 10,
            'offset': 0,
            'age_from': age_from,
            'age_to': age_to,
            'sex': sex,
            'city': city,
            'status': 6,
            'is_closed': False,
        })
        users = users.get('items', [])
        res = [{'id': user['id'], 'name': f"{user['first_name']} {user['last_name']}"}
               for user in users if not user.get('is_closed')]
        return res

    def get_photos(self, user_id):
        # Получение фотографий пользователя
        photos = self.api.method('photos.get', {
            'owner_id': user_id,
            'album_id': 'profile',
            'extended': 1
        })
        photos = photos.get('items', [])
        res = [{'owner_id': photo['owner_id'], 'id': photo['id'],
                'likes': photo['likes']['count'], 'comments': photo['comments']['count']}
               for photo in photos]
        res.sort(key=lambda x: x['likes'] + x['comments'], reverse=True)
        return res

if __name__ == '__main__':
    bot = VkTools(access_token)
    user_info = bot.get_profile_info(user_id=1)
    users = bot.search_users(user_info)