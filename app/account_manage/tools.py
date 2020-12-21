from .models import user_account


def unique_user(form):
    user = user_account.query.filter(
        user_account.username == form.username.data).first()
    if user:
        return 1
    user = user_account.query.filter(
        user_account.mail == form.mail.data).first()
    if user:
        return 2
    return 0
