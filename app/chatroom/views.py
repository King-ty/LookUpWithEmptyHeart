import os, re
from app import app, db, login
from app.mycenter import mycenter_app
from app.mycenter.models import MycenterInfo
from app.account_manage.models import user_account
from app.mycenter.forms import MyCenterEditForm
from app.chatroom import chatroom_bp
from app.chatroom.models import chat_message
from app.chatroom.forms import ChatroomForm
from app.focus_manage import focus_bp
from app.focus_manage.models import focus
from flask import redirect, url_for, flash, render_template, request, session
from flask_login import login_user, logout_user, current_user, login_required
import sys

sys.path.append("..")


@login.user_loader
def load_user(id):
    return user_account.query.get(id)


def get_timestamp_key(elem):
    return elem.timestamp


def get_msg_list(my_id, friend_id):
    list1 = chat_message.query.filter_by(sender_id=my_id,
                                         receiver_id=friend_id).all()
    list2 = chat_message.query.filter_by(sender_id=friend_id,
                                         receiver_id=my_id).all()
    total_list = list1 + list2
    total_list.sort(key=get_timestamp_key, reverse=False)
    return total_list


# 1.聊天交互界面
@chatroom_bp.route('/chatroom/<int:my_id>/<int:friend_id>',
                   methods=['GET', 'POST'])
def chatroom(my_id, friend_id=1):

    #读取表单
    form = ChatroomForm()

    #获取我的名字
    my = MycenterInfo.query.filter_by(id=my_id).first()
    my_name = my.name

    #获取正在聊天的朋友的名字
    friend = MycenterInfo.query.filter_by(id=friend_id).first()
    friend_name = friend.name

    #获取正在聊天的朋友头像路径
    center_usercenterinfo = MycenterInfo.query.filter(
        MycenterInfo.id == friend_id).first()
    if center_usercenterinfo.header:
        friend_avatar = url_for('static',
                                filename=center_usercenterinfo.header)
    else:
        friend_avatar = url_for('static', filename='images/header_start.jpg')

    #获取我和这位朋友的聊天总数
    count1 = chat_message.query.filter_by(sender_id=my_id,
                                          receiver_id=friend_id).count()
    count2 = chat_message.query.filter_by(sender_id=friend_id,
                                          receiver_id=my_id).count()
    total_count = count1 + count2

    #获取左侧好友列表,显示时候需要id名称头像三个内容
    friendlist = []

    #我关注的人
    friendlist1 = focus.query.filter(focus.focuser_id == my_id).all()
    for focus_relation in friendlist1:
        this_friend_id = focus_relation.focusee_id
        this_friend = MycenterInfo.query.filter(
            MycenterInfo.id == this_friend_id).first()
        this_friend_name = this_friend.name
        center_usercenterinfo = MycenterInfo.query.filter(
            MycenterInfo.id == this_friend_id).first()
        if center_usercenterinfo.header:
            this_friend_avatar = url_for('static',
                                         filename=center_usercenterinfo.header)
        else:
            this_friend_avatar = url_for('static',
                                         filename='images/header_start.jpg')
        # this_friend_avatar = url_for('static',
        #                              filename='images/' + str(this_friend_id) +
        #                              '/avatar.png')
        this_friend = [this_friend_id, this_friend_name, this_friend_avatar]
        friendlist.append(this_friend)

    #关注我的人
    friendlist2 = focus.query.filter(focus.focusee_id == my_id).all()
    for focus_relation in friendlist2:
        this_friend_id = focus_relation.focuser_id
        this_friend = MycenterInfo.query.filter(
            MycenterInfo.id == this_friend_id).first()
        this_friend_name = this_friend.name
        center_usercenterinfo = MycenterInfo.query.filter(
            MycenterInfo.id == this_friend_id).first()
        if center_usercenterinfo.header:
            this_friend_avatar = url_for('static',
                                         filename=center_usercenterinfo.header)
        else:
            this_friend_avatar = url_for('static',
                                         filename='images/header_start.jpg')
        # this_friend_avatar = url_for('static',
        #                              filename='images/' + str(this_friend_id) +
        #                              '/avatar.png')
        this_friend = [this_friend_id, this_friend_name, this_friend_avatar]
        if this_friend not in friendlist:  #防止双向关注重复添加
            friendlist.append(this_friend)

    #冒泡排序，按照最近一条消息时间对左侧聊天好友列表排序(消息主键id自增，比消息id就行)
    friendlist_len = len(friendlist)
    for j in range(friendlist_len):
        for i in range(friendlist_len - 1 - j):

            this_friend = friendlist[i]
            that_friend = friendlist[i + 1]
            this_friend_id = this_friend[0]
            that_friend_id = that_friend[0]

            latest_msg_with_this_friend = -1  #我和这位朋友之间最新消息id
            latest_msg_with_that_friend = -1  #我和那位朋友之间最新消息id

            #搜索我发给这位朋友的最新消息，更新
            msg_sent_to_this_friend = chat_message.query.filter_by(
                sender_id=my_id, receiver_id=this_friend_id).all()
            msg_sent_to_this_friend_count = len(msg_sent_to_this_friend)
            if msg_sent_to_this_friend_count > 0:
                latest_msg_with_this_friend = msg_sent_to_this_friend[-1].id

            #搜索我收到这位朋友的最新消息，更新
            msg_sent_by_this_friend = chat_message.query.filter_by(
                sender_id=this_friend_id, receiver_id=my_id).all()
            msg_sent_by_this_friend_count = len(msg_sent_by_this_friend)
            if msg_sent_by_this_friend_count > 0:
                if msg_sent_by_this_friend[-1].id > latest_msg_with_this_friend:
                    latest_msg_with_this_friend = msg_sent_by_this_friend[
                        -1].id

            #搜索我发给那位朋友的最新消息，更新
            msg_sent_to_that_friend = chat_message.query.filter_by(
                sender_id=my_id, receiver_id=that_friend_id).all()
            msg_sent_to_that_friend_count = len(msg_sent_to_that_friend)
            if msg_sent_to_that_friend_count > 0:
                latest_msg_with_that_friend = msg_sent_to_that_friend[-1].id

            #搜索我收到那位朋友的最新消息，更新
            msg_sent_by_that_friend = chat_message.query.filter_by(
                sender_id=that_friend_id, receiver_id=my_id).all()
            msg_sent_by_that_friend_count = len(msg_sent_by_that_friend)
            if msg_sent_by_that_friend_count > 0:
                if msg_sent_by_that_friend[-1].id > latest_msg_with_that_friend:
                    latest_msg_with_that_friend = msg_sent_by_that_friend[
                        -1].id

            if latest_msg_with_this_friend < latest_msg_with_that_friend:
                friendlist[i], friendlist[i + 1] = friendlist[i +
                                                              1], friendlist[i]

    #获取需要显示的消息列表
    message_list = get_msg_list(my_id, friend_id)

    #发送新消息表单提交
    if request.method == 'POST':
        # 接受表单提交的消息存入数据库
        msg = chat_message(sender_id=my_id,
                           receiver_id=friend_id,
                           text=request.form["message-to-send"])
        db.session.add(msg)
        db.session.commit()
        #发送新表单后刷新页面
        return redirect(url_for('chatroom_bp.chatroom', my_id=my_id, friend_id=friend_id))

    return render_template('chatroomnew.html',
                           my_id=my_id,
                           my_name=my_name,
                           total_count=total_count,
                           form=form,
                           friend_id=friend_id,
                           friend_name=friend_name,
                           friend_avatar=friend_avatar,
                           friendlist=friendlist,
                           message_list=message_list)
