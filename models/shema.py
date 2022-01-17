from models import helpful
from models.helpful import BaseSchema, wsql
from settings import SETTING_DB


class BaseUserSchema(BaseSchema):
    @staticmethod
    def create_tabel():
        wsql("""
        CREATE TABLE base_user
        (
            id            SERIAL PRIMARY KEY,
            user_name     VARCHAR(255) NOT NULL UNIQUE,
            last_name     VARCHAR(255) NOT NULL,
            hash_password VARCHAR(255) NOT NULL
        );
        """)


class MessageSchema(BaseSchema):
    @staticmethod
    def create_tabel():
        wsql("""
        CREATE TABLE message
        (
            id           SERIAL PRIMARY KEY,
            send_user_id int REFERENCES base_user (id) ON DELETE CASCADE,
            get_user_id  int REFERENCES base_user (id) ON DELETE CASCADE,
            text_message TEXT NOT NULL,
            CHECK ( send_user_id > 0 ),
            CHECK ( get_user_id > 0 )
        );
        """)


def create_tables():
    BaseUserSchema.create_tabel()
    MessageSchema.create_tabel()


def create_data_base():
    #  Удаляем конкретную базу данных
    helpful.settings_db.pop("database")
    wsql("""CREATE DATABASE message_db;""")
    # Возвращаем подключение к конкретной БД
    helpful.settings_db = SETTING_DB


if __name__ == '__main__':
    # create_data_base()
    create_tables()
