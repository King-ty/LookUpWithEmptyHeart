import os
from flask import redirect, url_for, flash, render_template, request, session
from flask_login import current_user, login_user, login_required, logout_user
from flask import render_template
from app.todolist import todolist_bp
from app.todolist.forms import AddForm
from app.todolist.models import todolist_list
from app import db, app


@todolist_bp.route('/todolist', methods=['GET', 'POST'])
def todolist():
    num = 0
    current_userid = current_user.id
    while todolist_list.query.filter(todolist_list.userid_id == num + 1, todolist_list.userid == current_userid).first() != None:
        num = num + 1
    null_event = todolist_list(title="",
                               event="",
                               year=0, month=0, day=0)
    list = [todolist_list.query.filter(todolist_list.userid_id == i, todolist_list.userid == current_userid).first() for i in range(num + 1)] + [null_event for i in range(32)]
    return render_template('todolist.html',
                           title="待办事项",
                           list=list,
                           num=num)


@todolist_bp.route('/add', methods=['GET', 'POST'])
def add():
    form2 = AddForm()
    current_userid = current_user.id
    num = 0
    i = 0
    while todolist_list.query.filter(todolist_list.id == i + 1).first() != None:
        first = todolist_list.query.filter(todolist_list.id == i + 1).first()
        if first.userid == current_userid:
            num = num + 1
        i = i + 1
    if form2.validate_on_submit():
        new_event = todolist_list(userid_id=num+1,
                                  userid=current_userid,
                                  title=form2.title.data,
                                  event=form2.event.data,
                                  year=form2.year.data, month=form2.month.data, day=form2.day.data)
        db.session.add(new_event)
        db.session.commit()
        return redirect(url_for('todolist.todolist'))
    return render_template('todolist_add.html', title="添加新事项", form=form2)
