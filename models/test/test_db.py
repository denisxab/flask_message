from models import helpful

from db import RegisterNewUser, EnterUser, _getIdFromUserName, SendMessage
from models.helpful import wsql

helpful.settings_db = {
    "host": "localhost",
    "user": "root",
    "password": "denis0310",
    "database": "message_db",
}


def test_full_base_user():
    wsql("""
    insert into base_user (user_name, last_name, hash_password )
    values ('bcleynaert0@biblegateway.com', 'Cleynaert', 'fGz6KIU1pjI'),
           ('dabramov1@house.gov', 'Abramov', 'ZoODrLBKDe'),
           ('mwillmett2@paginegialle.it', 'Willmett', 'S6jr7E3fE'),
           ('ldressel3@tmall.com', 'Dressel', 'kySs54g2'),
           ('dalvarado4@marriott.com', 'Alvarado', '0glcT0z'),
           ('sitzchaki5@mlb.com', 'Itzchaki', 'FQalheT3j9YH'),
           ('ekibel6@nhs.uk', 'Kibel', 'fNES3rB'),
           ('asturr7@delicious.com', 'Sturr', 'mpt6GEf'),
           ('kjanjusevic8@illinois.edu', 'Janjusevic', 'GjH4FH'),
           ('tvanderhoog9@ibm.com', 'Van Der Hoog', '9yrDrcDzf')
    """)


def test_full_message():
    wsql("""
    insert into message (send_user_id, get_user_id,text_message)
    values (6, 7, 'University of Modena'),
           (4, 3, 'Kwangju National University of Education'),
           (10, 7, 'Edogawa University'),
           (5, 3, 'Grambling State University'),
           (9, 10, 'Woosuk University'),
           (3, 10, 'Universidade Metropolitana de Santos'),
           (4, 9, 'Matsusaka University'),
           (7, 6, 'Nova Scotia Agricultural College'),
           (6, 9, 'Deakin University'),
           (8, 9, 'University of the Free State');
    """)


# Проверка регистрации нового пользователя
def test_RegisterNewUser():
    RegisterNewUser("denis", "Денис", "123")


def test_EnterUser():
    assert EnterUser("denis", "123") != False


def test__getIdFromUserName():
    assert _getIdFromUserName("denis") == 17


def test_SendMessage():
    SendMessage(17, "asturr7@delicious.com", "Привет друг")
