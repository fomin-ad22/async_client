# async_client
async client and API on FAST API with DB (SQLModel connection, API pytest control, The ability to assemble a container in Docker or pull in Docker Hub)

Асинхронный автономный клиент извлекает данные о двух тикетах BTC и ETH с сайта deribit.com и сохраняет их в формате записи {id,ticket,price,date} 

Cервис предоставляет методы для работы с базой данных, основанной на изменениях BTC и ETH. Также реализовано подключение к БД и хранению данных в ней (В текущем проекте SQLlite).
Добавлена возможность тестов API c помощью pytest. Возможна компиляция проекта в Docker image или импорт его из Docker Hub.

Основные классы:

• test_currency=Currency({'id':"special_id", 'ticket':"name", 'price':15.00, 'date':"some date in YYYY-MM-DD format"})

Основные обозначения:
• ticket_name - имя валюты для анализа ("BTC" или "ETH")
• date - дата для анализа (передавать в формате YYYY-MM-DD, в БД хранится в формате UNIX timestamp)

Основные функции контроля валют:

• Просмотрите всю историю изменений валюты get_story_price("ticket_name"). 
• Просмотрите последнюю запись об изменении валюты get_curr_price("ticket_name").
• Просмотрите всю историю изменений валюты по дате get_story_price("ticket_name",date).

Как использовать сервис:

Для работы с сервисом вам необходимо из рабочей директории запустить API через терминал командой "uvicorn main:app".
Взаимодействие с сервисом осуществляется через файл client.py или через отправку http запросов в браузере.

Для проверки работоспособности API клиента с помощью pytest, необходимо сперва запустить API, далее запустить тесты через терминал.
Для компиляции в Docker image: в корне проекта присутствует Dockerfile. Репозиторий для импорта из Docker Hub: fominad22/myapi:v1. (Для запуска контейнера: docker run --name yourcountainername -d -p 8000:8000 fominad22/myapi:v1)

С вопросами и предложениями @fomin_ad22 tg
