# telegram_bot

Приложение написано на ЯП python с использованием принципов ООП.
Данная программа состоит из одного класса Monitoring(), который реализует в себе все необходимые методы и свойства для работы бота.
Основные параметры берутся из конф файла. Нужно заметить, что при изменении параметров в файле, требуется перезапуск программы.

Класc имеет следующие входные параметры (значения по умолчанию, в случае если они не задаются при создании объекта, 
заданы в скобках):


- *frequencyOfSend (60)*
- *frequencyOfCheck (1)*
- *confFile = "config.conf"*


Он содержит следующие свойства:
- frequencyOfCheck (int) - частота опроса ссылки
- frequencyOfSend (int) - частота отправки оповещений в телеграм
- confFile (str) - имя конф файла, откуда берутся основные параметры.
- tokenKey (str)- токен бота(берется из конф файла
- chatId - Chat Id берется из конф файла
- url - берется из конф файла
- urlContext - берется из конф файла
- ethalonString - берется из конф файла

И следующие методы:
- набор сеттеров, для возможности задать значения не только из конфиг файла но и через данные методы непосредственно в коде
- get_body() - метод, который позволяет получить тело ответа по заданным параметрам
- compare_withEthalon() - позволяет сравнить строку, полученную методом get_body с эталонной.
- send_to_telegramm() - позволяет отправить сообщение в телетрам-чат с определенными заданными параметрами.
- main() - основной метод, который вызывается в конструкторе и вызывает другие методы данного класса для реализации логики мониторинга.

