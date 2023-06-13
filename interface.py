import vk_api
import data_store
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.utils import get_random_id

from config import comunity_token, acces_token
from core import VkTools
from key import *


class BotInterface():
    def __init__(self, comunity_token, acces_token):
        self.vk = vk_api.VkApi(token=comunity_token)
        self.longpoll = VkLongPoll(self.vk)
        self.vk_tools = VkTools(acces_token)
        self.params = {}
        self.worksheets = []
        self.offset = 0
        print('\U0001F916 "Vkinder" запущен!', sep='\n')

    def message_send(self, user_id, message, attachment=None):
        self.vk.method('messages.send',
                       {'user_id': user_id,
                        'message': message,
                        'attachment': attachment,
                        'random_id': get_random_id(),
                        'keyboard': keyboard.get_keyboard()}
                       )

    def get_user_photo(self, user_id):
        photos = self.vk_tools.get_photos(user_id)
        photo_string = ''
        for photo in photos:
            photo_string += f'photo{photo["owner_id"]}_{photo["id"]},'
        return photo_string

    def find_city(self, user_id):
        # Функция получения города в случае его отсутствия в профиле
        self.message_send(user_id, 'Введите название города для поиска: ')
        message, user_id = self.event_handler()
        hometown = str(message)
        cities = self.vk_tools.get_cities(user_id)
        for city in cities:
            if city['title'] == hometown.title():
                self.message_send(user_id, f'Ищу в городе {hometown.title()}')
                return hometown.title()

        self.message_send(user_id, 'Некорректный ввод')
        self.find_city(user_id)

    def event_handler(self):
        for event in self.longpoll.listen():
            if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                if event.text.lower() == 'привет':
                    '''Логика для получения данных о пользователе'''
                    self.params = self.vk_tools.get_profile_info(event.user_id)
                    # Запрос доп. информации, в случае если она отсутствует в профиле
                    if self.params["city"] is None:
                        self.message_send(
                            event.user_id, f'Приветствую тебя, {self.params["name"]}!\n'
                                           f'Для продолжения работы с ботом укажи свой город')
                        event.to_me = self.find_city(event.user_id)
                    # elif self.params["bdate"] is None:
                    #     self.message_send(
                    #         event.user_id, f'Приветствую тебя, {self.params["name"]}!\n'
                    #         f'Для продолжения работы с ботом укажи дату своего рождения в формате DD.MM.YYYY')
                    #     event.to_me = self.params["bdate"]
                    else:
                        self.message_send(event.user_id, f'Приветствую тебя, {self.params["name"]}!')
                elif event.text.lower() == 'поиск':
                    '''Логика для поиска анкет'''
                    if self.worksheets:
                        worksheet = self.worksheets.pop()
                        photo_string = self.get_user_photo(worksheet['id'])
                    else:
                        self.worksheets = self.vk_tools.search_worksheet(
                            self.params, self.offset)

                        worksheet = self.worksheets.pop()
                        'првоерка анкеты в бд в соотвествие с event.user_id'

                        connection = data_store.connect_to_database()
                        data_store.create_table_seen_users(connection)
                        num_users_shown = 0  # Количество показанных пользователей
                        shown_users = set()  # Множество показанных пользователей

                        while worksheet and num_users_shown < 1:  # Показывать только 1 пользователя
                            # worksheet = worksheet.pop()
                            if str(worksheet['id']) not in shown_users:
                                shown_users.add(str(worksheet['id']))
                                num_users_shown += 1
                                # Проверка наличия пользователя в БД
                                if data_store.check_seen_user(connection, str(worksheet['id'])):
                                    self.message_send(event.user_id, f"{worksheet['name']} уже есть в базе данных.")
                                    continue

                        photo_string = self.get_user_photo(worksheet['id'])
                        self.offset += 50

                    self.message_send(event.user_id,
                                      f'Посмотри, это - {worksheet["name"]}',
                                      attachment=photo_string)
                    self.message_send(event.user_id,
                                      f'Ссылка на страницу профиля в VK: https://vk.com/id{worksheet["id"]}')

                    'добавить анкету в бд в соотвествие с event.user_id'
                    connection = data_store.connect_to_database()
                    data_store.insert_data_seen_users(connection, str(worksheet["id"]), 0)

                elif event.text.lower() == 'пока':
                    self.message_send(event.user_id, 'Пока!')
                    connection = data_store.connect_to_database()
                    data_store.remove_table_seen_users(connection)
                    data_store.disconnect_from_database(connection)
                else:
                    self.message_send(event.user_id, 'Команда не распознана')


if __name__ == '__main__':
    bot_interface = BotInterface(comunity_token, acces_token)
    bot_interface.event_handler()
