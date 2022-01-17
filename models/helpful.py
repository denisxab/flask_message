"""
Пример использования:


import helpful

from helpful import wsql

helpful.settings_db = {
    "host": "localhost",
    "user": "root",
    "password": "denis0310",
    "database": "test_db",
}


wsql("CREATE DATABASE message_db;")

"""
import abc
import hashlib
from pprint import pformat

from loguru import logger
from mysql.connector import connect, Error
from mysql.connector.abstracts import MySQLConnectionAbstract

from settings import SETTING_DB

settings_db: dict | None = SETTING_DB


def connect_db(fun):
    """
    Декоратор для создать подключение к БД
    """

    def wrapper(*arg, **kwargs):
        try:
            with connect(**settings_db) as connection:
                res = fun(connection, *arg, **kwargs)
            return res
        except Error as e:
            logger.error(e)
            raise e

    return wrapper


def mutable_command(multi: bool = False):
    """
    Декоратор для выполнения изменяемой SQL команды

    :param multi: Выполнить несколько команд (!)
    """

    def wrapper(fun):
        def decorated_function(_connection: MySQLConnectionAbstract, *arg, **kwargs) -> str:
            with _connection.cursor() as cursor:
                res = fun(*arg, **kwargs)
                cursor.execute(res[0], res[1], multi=multi)
                _connection.commit()
            return cursor.statement

        return decorated_function

    return wrapper


def read_command(multi: bool = False):
    """
    Декоратор для выполнения чтения из БД

    :param multi: Выполнить несколько команд
    """

    def wrapper(fun):
        def decorated_function(_connection: MySQLConnectionAbstract, *arg, **kwargs) -> any:
            with _connection.cursor() as cursor:
                res = fun(*arg, **kwargs)
                cursor.execute(res[0], res[1], multi=multi)

                return cursor.fetchall()

        return decorated_function

    return wrapper


def pprint_deco(fun):
    """
    Декоратор для красивого вывода результата функции в консоль
    """

    def wrapper(*arg, **kwargs):
        return pformat(fun(*arg, **kwargs))

    return wrapper


@connect_db
@read_command()
def rsql(execute: str, params: tuple | dict | list = ()) -> tuple[str, tuple | dict | list]:
    """
    Чтение из БД
    """
    return execute, params


@pprint_deco
@connect_db
@read_command()
def Rsql(execute: str, params: tuple | dict | list = ()) -> tuple[str, tuple | dict | list]:
    """
    Чтение из БД с красивым выводом в консоль
    """
    return execute, params


@connect_db
@mutable_command()
def wsql(execute: str, params: tuple | dict | list = ()) -> tuple[str, tuple | dict | list]:
    """
    Внесение изменений в БД
    """
    return execute, params


class UserNameDontExistsError(Exception):
    def __str__(self):
        return "Пользователь с таким `user name` не существует"


def hashPassword(password: str) -> str:
    """
    Захеширвоать пароль
    """
    return hashlib.sha512(password.encode('utf-8')).hexdigest()


class BaseSchema:
    """
    Базовая SQL модель
    """

    @abc.abstractstaticmethod
    def create_tabel():
        """
        Создать таблицу в БД
        """
        ...
