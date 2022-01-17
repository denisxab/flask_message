from views import enter_user, register_account


def init(app):
    app.add_url_rule('/enter_user/', view_func=enter_user.as_view('enter_user'))
    app.add_url_rule('/register_account/', view_func=register_account.as_view('register_account'))
