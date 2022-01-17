CREATE DATABASE message_db;

CREATE TABLE base_user
(
    id            SERIAL PRIMARY KEY,
    user_name     VARCHAR(255) NOT NULL UNIQUE,
    last_name     VARCHAR(255) NOT NULL,
    hash_password VARCHAR(255) NOT NULL
);
CREATE TABLE message
(
    id           SERIAL PRIMARY KEY,
    send_user_id int REFERENCES base_user (id) ON DELETE CASCADE,
    get_user_id  int REFERENCES base_user (id) ON DELETE CASCADE,
    text_message TEXT NOT NULL,
    CHECK ( send_user_id > 0 ),
    CHECK ( get_user_id > 0 )
);

# Исходящие сообщения
SELECT send_tabel.id, Отправитель, user_name as Получатель, message_id, text_message
FROM (SELECT base_user.id,
             user_name  as "Отправитель",
             get_user_id,
             message.id as message_id,
             text_message
      FROM base_user
               JOIN message ON message.send_user_id = base_user.id
      where base_user.id = 7) as send_tabel
         JOIN base_user as get_tabel ON send_tabel.get_user_id = get_tabel.id;

#  Входящие сообщения
SELECT send_tabel.id, Отправитель, user_name as Получатель, message_id, text_message
FROM (SELECT base_user.id,
             user_name  as "Отправитель",
             send_user_id,
             message.id as message_id,
             text_message
      FROM base_user
               JOIN message ON message.get_user_id = base_user.id
      where base_user.id = 7) as send_tabel
         JOIN base_user as get_tabel ON send_tabel.send_user_id = get_tabel.id;

# Регистрация пользователя
INSERT INTO base_user (user_name, last_name, hash_password) VALUE
    ('denis', 'Денис', '123');

# Вход пользователя
SELECT *
FROM base_user
WHERE user_name = 'ekibel6@nhs.uk'
  and hash_password = 'fNES3rB';

# Удалить аккаунт пользователя
#

# Получить id пользователя по его `UserName`
SELECT id
FROM base_user
WHERE user_name = 'denis';

# Написать сообщение другому пользователю
INSERT INTO message (send_user_id, get_user_id, text_message) value
    ();


# Удалить пользователя
DELETE
FROM base_user
WHERE id = 7;



