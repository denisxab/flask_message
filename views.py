from flask import render_template, abort, jsonify, redirect, url_for
from flask import request
from flask.views import MethodView
from loguru import logger

from models.helpful import hashPassword
from models.model import BaseUser, Message, LowUser
from settings import app


def is_login() -> bool:
    """
    Проверка аутентификации пользователя
    """
    match request.cookies:
        case {"user_id": user_id, "hash_password": hash_password} if user_id.isdigit:
            is_login = BaseUser.check_password(int(user_id),
                                               hash_password)
            if is_login:
                return True
    return False


def login(fun):
    """
    Декоратор проверки аутентификации пользователя
    """

    def wrapper(*arg, **kwargs):
        if is_login():
            res = fun(*arg, **kwargs)
            return res
        abort(403)

    return wrapper


class enter_user(MethodView):
    methods = ['GET', 'POST']

    def post(self):
        match request.form:
            case {"UserName": user_name, "Password": password}:
                logger.info(f"{user_name=},{password=}")
                res = BaseUser.enter_account(user_name, password)

                if not res:
                    return jsonify({"error": "Имя или пароль не верный"})

                response = redirect(url_for('my_message'))
                response.set_cookie("user_name", user_name)
                response.set_cookie("user_id", str(res))
                response.set_cookie("hash_password", hashPassword(password), max_age=None)
                return response
            case _:
                abort(403)

    def get(self):
        return redirect(url_for('my_message')) if is_login() else render_template("enter_user.html")


class register_account(MethodView):
    methods = ['GET', 'POST']

    def post(self):
        match request.form:
            case {
                "UserName": user_name, "Password": password,
                "Name": name
            }:
                logger.info(f"{user_name=},{password=},{name=}")
                res = BaseUser.register_new_account(user_name, name, password)
                if not res:
                    return jsonify({"error": "Ошибка регистрации"})
                return redirect(url_for('enter_user'))
            case _:
                abort(403)

    def get(self):
        return redirect(url_for('my_message')) if is_login() else render_template("register_account.html")


class my_message(MethodView):
    methods = ['GET', 'POST']

    def post(self):
        ...

    @login
    def get(self):
        _user_id = int(request.cookies.get('user_id'))
        return render_template("my_message.html",
                               user_name=request.cookies.get('user_name'),
                               user_id=_user_id,
                               GetOutgoingMessageFromUser=Message.GetOutgoingMessageFromUser(_user_id),
                               GetIncomingMessageFromUser=Message.GetIncomingMessageFromUser(_user_id)
                               )


class send_message(MethodView):
    methods = ['GET', 'POST']

    @login
    def post(self):
        LowUser.send_message(int(request.cookies.get("user_id")),
                             request.form.get("get_user_name"),
                             request.form.get("text_message"), )
        return jsonify({"cod": "200"})

    @login
    def get(self):
        ...


class logout(MethodView):
    """
    ВЫти из профиля
    """
    methods = ['GET']

    @login
    def get(self):
        response = redirect(url_for('enter_user'))
        response.delete_cookie('user_name')
        response.delete_cookie('user_id')
        response.delete_cookie('hash_password')
        return response


@app.route('/')
def index():
    return redirect(url_for("enter_user"))
