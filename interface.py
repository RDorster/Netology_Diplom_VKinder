import vk_api
import data_store
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.utils import get_random_id
from config import community_token, access_token
from core import VkTools
from key import keyboard

class BotInterface():

    def __init__(self, community_token, access_token):
        self.interface = vk_api.VkApi(token=community_token)
        self.api = VkTools(access_token)
        self.params = None
        self.keyboard = keyboard
        print('\U0001F916 "Vkinder" запущен!', 'Для прекращения работы бота нажмите CTRL + C', sep='\n')

    def message_send(self, user_id, message, attachment=None, keyboard=None):
        '''Отправляет сообщение пользователю.
        Args:
            user_id (int): ID пользователя.
            message (str): Текст сообщения.
            attachment (str, optional): Строка с прикреплением. По умолчанию None.
            keyboard (object, optional): Объект клавиатуры. По умолчанию None.
        '''
        self.interface.method('messages.send', {
            'user_id': user_id,
            'message': message,
            'attachment': attachment,
            'random_id': get_random_id(),
            'keyboard': keyboard
        })

    # Обработчик сообщений от пользователя
    def event_handler(self):
        longpoll = VkLongPoll(self.interface)
        shown_users = set()  # Множество показанных пользователей

        for event in longpoll.listen():
            if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                command = event.text.lower()
                if command == 'привет':
                    self.params = self.api.get_profile_info(event.user_id)
                    self.message_send(event.user_id, f'Приветствую тебя, {self.params["name"]}')
                elif command in ('поиск', 'следующие'):
                    connection = data_store.connect_to_database()
                    data_store.create_table_seen_users(connection)
                    users = self.api.search_users(self.params)
                    num_users_shown = 0  # Количество показанных пользователей

                    while users and num_users_shown < 10:  # Показывать только 10 пользователей
                        user = users.pop()
                        if str(user["id"]) not in shown_users:
                            shown_users.add(str(user["id"]))
                            num_users_shown += 1
                            # Проверка наличия пользователя в БД
                            if data_store.check_seen_user(connection, str(user["id"])):
                                self.message_send(event.user_id, f"{user['name']} уже есть в базе данных.")
                            else:
                                # Если пользователь отсутствует в БД, добавляем его
                                data_store.insert_data_seen_users(connection, str(user["id"]), 0)
                                photos_user = self.api.get_photos(user['id'])
                                attachment = ''
                                for num, photo in enumerate(photos_user):
                                    attachment += f'photo{photo["owner_id"]}_{photo["id"]},'
                                    if num == 2:
                                        break
                                self.message_send(event.user_id,
                                                  f'Посмотри, это - {user["name"]}',
                                                  attachment=attachment
                                                  )
                                self.message_send(event.user_id,
                                                  f'Ссылка на страницу профиля в VK: https://vk.com/id{user["id"]}')
                    data_store.disconnect_from_database(connection)
                elif command == 'пока':
                    self.message_send(event.user_id, 'Пока!')
                    connection = data_store.connect_to_database()
                    data_store.remove_table_seen_users(connection)
                    data_store.disconnect_from_database(connection)
                else:
                    self.message_send(event.user_id, 'Команда не распознана.')

if __name__ == '__main__':
    bot = BotInterface(community_token, access_token)
    bot.event_handler()
