<h1><font color="red">VKinder</font></h1>

*VK Users Search Bot 🤖*




## RUS

Данный код представляет собой реализацию бота для социальной сети ВКонтакте (VK). Он выполняет следующие функции:

1. `interface.py` - основной файл, в котором создается экземпляр класса `BotInterface`. Он отвечает за взаимодействие с пользователем через сообщения и обработку команд.
   - `BotInterface` инициализирует объекты `VkTools` и `vk_api.VkApi` для выполнения запросов к API ВКонтакте.
   - Метод `message_send` отправляет сообщения пользователю, используя метод `messages.send` API ВКонтакте.
   - Метод `event_handler` отслеживает новые сообщения в диалоге и выполняет соответствующие действия в зависимости от команды пользователя.

2. `core.py` - файл, содержащий класс `VkTools`, который предоставляет методы для работы с API ВКонтакте.
   - `VkTools` инициализирует объект `vk_api.VkApi` для выполнения запросов к API ВКонтакте.
   - Метод `get_profile_info` получает информацию о пользователе по его ID.
   - Метод `search_users` выполняет поиск пользователей, удовлетворяющих заданным параметрам.- Метод `get_photos` получает фотографии пользователя.

3. `data_store.py` - файл, содержащий функции для работы с базой данных.
   - `connect_to_database` устанавливает соединение с базой данных PostgreSQL.
   - `create_table_seen_users` создает таблицу `seen_users`, если она еще не существует.
   - `check_seen_user` проверяет, есть ли указанный пользователь в таблице `seen_users`.
   - `insert_data_seen_users` добавляет данные о просмотренном пользователе в таблицу `seen_users`.
   - `disconnect_from_database` закрывает соединение с базой данных.

4. `Key.py` - файл, содержащий объект клавиатуры `keyboard`, который используется для отображения кнопок в сообщениях.

## Использование
Общий сценарий работы бота:
- Бот ожидает новые сообщения от пользователей.
- При получении команды "привет", он приветствует пользователя и получает информацию о нем.
- При получении команды "поиск", бот выполняет поиск пользователей, удовлетворяющих параметрам пользователя.
- При получении команды "следующие", бот переходит к следующему пользователю в результате поиска.
- При получении команды "пока", бот прощается с пользователем.
- Если получена нераспознанная команда, бот отправляет соответствующее сообщение.

В целом, код реализует простого бота-поисковика пользователей в ВКонтак

те с использованием клавиатуры и базы данных для отслеживания просмотренных пользователей.


## ENG

This code repository contains an implementation of a bot for the VKontakte (VK) social network. The bot serves the following functions:

1. `interface.py` - the main file where an instance of the `BotInterface` class is created. It handles user interaction through messages and command processing.
   - `BotInterface` initializes objects `VkTools` and `vk_api.VkApi` to make requests to the VK API.
   - The `message_send` method sends messages to users using the `messages.send` method of the VK API.
   - The `event_handler` method tracks new messages in the conversation and performs corresponding actions based on user commands.

2. `core.py` - a file containing the `VkTools` class, which provides methods for working with the VK API.
   - `VkTools` initializes the `vk_api.VkApi` object to make requests to the VK API.
   - The `get_profile_info` method retrieves information about a user based on their ID.
   - The `search_users` method performs a search for users based on specified parameters.
   - The `get_photos` method retrieves a user's photos.

3. `data_store.py` - a file containing functions for working with the database.
   - `connect_to_database` establishes a connection to a PostgreSQL database.
   - `create_table_seen_users` creates the `seen_users` table if it does not exist.
   - `check_seen_user` checks if a specified user exists in the `seen_users` table.
   - `insert_data_seen_users` adds data about a viewed user to the `seen_users` table.
   - `disconnect_from_database` closes the connection to the database.

4. `Key.py` - a file containing the `keyboard` object, which is used to display buttons in messages.

## Usage

The bot follows the following workflow:

- The bot awaits new messages from users.
- Upon receiving the "привет" (hello) command, it greets the user and retrieves information about them.
- Upon receiving the "поиск" (search) command, the bot performs a search for users based on the user's parameters.
- Upon receiving the "следующие" (next) command, the bot moves to the next user in the search results.
- Upon receiving the "пока" (goodbye) command, the bot bids farewell to the user.
- If an unrecognized command is received, the bot sends an appropriate message.

Overall, the code implements a simple VK user search bot using a keyboard interface and a database to track viewed users.