from views import enter_user, register_account, my_message, send_message, logout


def init(app):
    app.add_url_rule('/enter_user/', view_func=enter_user.as_view('enter_user'))
    app.add_url_rule('/register_account/', view_func=register_account.as_view('register_account'))
    app.add_url_rule('/my_message/', view_func=my_message.as_view('my_message'))
    app.add_url_rule('/api/send_message/', view_func=send_message.as_view('send_message'))
    app.add_url_rule('/logout/', view_func=logout.as_view('logout'))
