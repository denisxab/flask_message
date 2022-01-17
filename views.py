from flask import render_template, abort, jsonify
from flask import request
from flask.views import MethodView
from loguru import logger

from models.model import BaseUser
from settings import app


class enter_user(MethodView):
    methods = ['GET', 'POST']

    def post(self):
        match request.form:
            case {"UserName": user_name, "Password": password}:
                logger.info(f"{user_name=},{password=}")
                res = BaseUser.enter_account(user_name, password)
                if not res:
                    return jsonify({"error": "Имя или пароль не верный"})
                return render_template("index.html",
                                       title='Home',
                                       )
            case _:
                abort(403)

    def get(self):
        return render_template("enter_user.html",
                               title='Home',
                               )


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
                return render_template("index.html",
                                       title='Home',
                                       )
            case _:
                abort(403)

    def get(self):
        return render_template("register_account.html",
                               title='Home',
                               )


@app.route('/my_message')
def my_message():
    pass


@app.route('/disconnect_user')
def disconnect_user():
    pass
