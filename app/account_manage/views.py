import os
from app.account_manage.forms import RegisterForm, LoginForm
from app.account_manage.models import user_account
from app.mycenter.models import MycenterInfo
from app import db, app, login
from flask import redirect, url_for, flash, render_template, request, session
from flask_login import current_user, login_user, login_required, logout_user
from app.account_manage import account_bp
from app.account_manage.tools import unique_user


@login.user_loader
def load_user(id):
    return user_account.query.get(id)


@account_bp.route('/', methods=['GET', 'POST'])
def index():
    form = RegisterForm()
    return render_template('index.html', title="主页", form=form)


@account_bp.route('/register/', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('account.index'))  #
    form = RegisterForm()
    if form.validate_on_submit():
        num = unique_user(form)
        if num == 1:
            flash("该用户名已被注册！", 'danger')
        elif num == 2:
            flash("该邮箱已被注册！", 'danger')
        else:
            user = user_account(username=form.username.data,
                                mail=form.mail.data,
                                phone=form.phone.data)
            user.set_password(form.password2.data)
            default_avatar = 'avatar.jpg'
            user.Avater = default_avatar
            db.session.add(user)

            this_id = user_account.query.count()  #用户账号主键id在上一步生成，然后查询

            user_info = MycenterInfo(id=this_id,
                                     name=form.username.data,
                                     gender=form.gender.data,
                                     hometown=form.hometown.data,
                                     major=form.major.data,
                                     age=form.age.data)

            db.session.add(user_info)
            db.session.commit()
            flash("注册成功！", 'success')
            return redirect(url_for('account.login'))
    else:
        if form.errors:
            flash("some error occurred!")
    return render_template("register.html", title='注册', form=form)


@account_bp.route('/login/', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('account.index'))
    form = LoginForm()
    if form.validate_on_submit() and request.method == 'POST':
        user = user_account.query.filter(
            user_account.username == form.useraccount.data).first()
        if user is None:
            user = user_account.query.filter(
                user_account.mail == form.useraccount.data).first()
        if user is None:
            flash("用户不存在！", 'danger')
            return render_template('login.html', title='登录', form=form)
        else:
            if user.check_password(form.password.data):
                flash("成功登录！", 'success')
                login_user(user, form.remember_me.data)
                return redirect(
                    request.args.get('next') or url_for('account.index'))
            else:
                flash("用户名或密码错误！", 'danger')
                return render_template("login.html", title='登录', form=form)

    return render_template('login.html', title='登录', form=form)


@account_bp.route('/logout/')
@login_required
def logout():
    if current_user.is_authenticated:
        logout_user()
        flash('注销成功！', 'success')
    return redirect(request.args.get('next') or url_for('account.index'))  #


# @account_bp.route()
# @login_required
# def myinfo():
#     return 1
