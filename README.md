Написать приложение «Вишлист» с полями: название, цена, ссылка на страницу с покупкой, примечание. Или любое другое
маленькое CRUD-приложение на свой вкус. Требуемые технологии: MySQL, Python + Flask. Любая библиотека компонентов на ваш
вкус. Выложить на GitHub. Ожидаемое время выполнения: 2-4 часа. Тестовое задание требуется выложить на GitHub и написать
@skkachaev в ТГ вместе со ссылкой на резюме.

Дополнительные бонусы за:

- README файл с информацией по инсталляции/запуску
- .service файл
- Пользовательскую документацию

---

Мессенджер на Flask:

Какие технологии нужно знать:

- Установка MySql
- CRUD MySql
- Как работает шаблонизатор в Flask

Таблицы:

- Пользователь
    - ID
    - User Name
    - Имя
    - Хеш пароля

- Сообщения
    - ID сообщения
    - От кого сообщение
      (reference Пользователь.id ON DELETE CASCADE)
      Если отправитель удалил свой акант то нужно удалить все его письма
    - Кому сообщение
      (reference Пользователь.id ON DELETE NO ACTION)
      Если получатель удалил свой аккаунт то ни чего не делаем
    - Тест сообщения

Внешний вид:

1) Вход в аккаунт
    - Поле для ввода ID
    - Поле дла ввода Пароля
    - 1.1) Регистрация пользователя
        - User Name
        - Имя
        - Пароль

2) Сообщения
    - Список входящих сообщений к пользователю (С лево)
    - Список исходящих сообщение от пользователя (С право)
      2.1) Написать сообщение пользователю
        - false: Если нет пользователя вызвать ошибку
        - true: Если пользователь найден то отправить сообщение
    - 2.2) Удалить аккаунт

