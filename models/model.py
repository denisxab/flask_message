from loguru import logger
from mysql.connector import Error

from models.helpful import wsql, rsql, hashPassword, UserNameDontExistsError
from models.shema import BaseUserSchema, MessageSchema


class BaseUser(BaseUserSchema):

    @staticmethod
    def _verification_sql_id(user_id: any):
        """
        Получить User ID из SQL ответа

        :param user_id: SQL ответ
        """
        match user_id:
            case list() if len(user_id) > 0 and user_id[0]:
                return int(user_id[0][0])
            case _:
                return False

    @classmethod
    def _get_id_from_user_name(cls, user_name: str) -> int:
        """
        Получить id пользователя по его `UserName`
        """
        res = rsql("""SELECT id FROM base_user WHERE user_name = %s;""", [user_name])
        return cls._verification_sql_id(res)

    @classmethod
    def enter_account(cls, user_name: int, password: str) -> int:
        """
        Вход пользователя в свой аккаунт

        :return: User ID
        """
        user_id = rsql("""
        SELECT id
        FROM base_user
        WHERE id = %s and hash_password =  %s;
        """, [user_name, hashPassword(password)])
        return cls._verification_sql_id(user_id)

    @classmethod
    def register_new_account(cls, user_name: str, last_name: str, password: str) -> int:
        """
        Регистрация нового пользователя

        :return: user id
        """
        try:
            wsql("""
            INSERT INTO base_user (user_name, last_name, hash_password) VALUE 
            (%s,%s,%s)
            """, [user_name, last_name, hashPassword(password)])

            return cls._get_id_from_user_name(user_name)
        except Error as e:
            logger.error(f"Ошибка регистрации {user_name=},{last_name=}", e)
            raise e

    @staticmethod
    def delete_account(user_id: int):
        """
        Удаление пользователя
        """
        try:
            wsql("""
             DELETE FROM base_user WHERE id = %s;
             """, [user_id])
        except Error as e:
            logger.error(f"Ошибка удаления аккаунта {user_id=}", e)
            raise e


class LowUser(BaseUser):

    @classmethod
    def send_message(cls, send_user_id: int, get_user_name: str, text_message: str):
        """
        Написать сообщение другому пользователю
        """
        get_user_id = cls._get_id_from_user_name(get_user_name)
        if not get_user_id:
            raise UserNameDontExistsError()

        wsql("""
            INSERT INTO message (send_user_id, get_user_id, text_message) value
                (%s,%s,%s)
        """, [send_user_id, get_user_id, text_message])


class Message(MessageSchema):

    @staticmethod
    def GetOutgoingMessageFromUser(user_id: int):
        """
        Получить список ИСХОДЯЩИХ сообщений от пользователя
        """
        return helpful.Rsql("""
        SELECT send_tabel.id, Отправитель, user_name as Получатель, message_id, text_message
        FROM (SELECT base_user.id, user_name as "Отправитель", get_user_id, message.id as message_id, text_message
              FROM base_user
                       JOIN message ON message.send_user_id = base_user.id
              where base_user.id = %s ) as send_tabel
                 JOIN base_user as get_tabel ON send_tabel.get_user_id = get_tabel.id;
        """, [user_id])

    @staticmethod
    def GetIncomingMessageFromUser(user_id: int):
        """
        Получить список ВХОДЯЩИХ сообщений к пользователю
        """
        return helpful.Rsql("""
        SELECT send_tabel.id, Отправитель, user_name as Получатель, message_id, text_message
        FROM (SELECT base_user.id,
                     user_name  as "Отправитель",
                     send_user_id,
                     message.id as message_id,
                     text_message
              FROM base_user
                       JOIN message ON message.get_user_id = base_user.id
              where base_user.id = %s) as send_tabel
                 JOIN base_user as get_tabel ON send_tabel.send_user_id = get_tabel.id;
        """, [user_id])
