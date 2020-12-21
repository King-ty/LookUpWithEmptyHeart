import os, re, random
from app import app, db, login
from app.mycenter import mycenter_app
from app.mycenter.models import MycenterInfo
from app.account_manage.models import user_account
from app.focus_manage import focus_bp
from app.focus_manage.models import focus
from flask import redirect, url_for, flash, render_template, request, session
from flask_login import login_user, logout_user, current_user, login_required
import sys

sys.path.append("..")


@login.user_loader
def load_user(id):
    return user_account.query.get(id)


@focus_bp.route('/friendlist/<int:my_id>', methods=['GET', 'POST'])
def friendlist(my_id):

    #获取好友列表,显示时候需要id名称头像三个内容
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
        this_friend_avatar = url_for('static',
                                     filename='images/header_start.jpg')
        if center_usercenterinfo.header:
            this_friend_avatar = url_for('static',
                                         filename=center_usercenterinfo.header)
        this_friend_introduction = this_friend.introduction
        this_friend = [
            this_friend_id, this_friend_name, this_friend_avatar,
            this_friend_introduction
        ]
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
        this_friend_avatar = url_for('static',
                                     filename='images/header_start.jpg')
        if center_usercenterinfo.header:
            this_friend_avatar = url_for('static',
                                         filename=center_usercenterinfo.header)
        this_friend_introduction = this_friend.introduction
        this_friend = [
            this_friend_id, this_friend_name, this_friend_avatar,
            this_friend_introduction
        ]
        if this_friend not in friendlist:  #防止双向关注重复添加
            friendlist.append(this_friend)

    #可能认识的人
    potenialfriendlist = []
    cnt = 0
    user_count = MycenterInfo.query.count()
    while cnt < min(user_count - len(friendlist), 8):
        this_id = random.randint(1, user_count)
        is_friend_already = focus.query.filter_by(focuser_id=my_id,
                                                  focusee_id=this_id).count()
        is_friend_already += focus.query.filter_by(focusee_id=my_id,
                                                   focuser_id=this_id).count()
        if is_friend_already == 0:
            this_potenial_friend = MycenterInfo.query.filter(
                MycenterInfo.id == this_id).first()
            this_potenial_friend_id = this_id
            this_potenial_friend_name = this_potenial_friend.name
            center_usercenterinfo = MycenterInfo.query.filter(
                MycenterInfo.id == this_potenial_friend_id).first()
            this_potenial_friend_avatar = url_for(
                'static', filename='images/header_start.jpg')
            if center_usercenterinfo.header:
                this_potenial_friend_avatar = url_for(
                    'static', filename=center_usercenterinfo.header)
            this_potenial_friend_introction = this_potenial_friend.introduction
            this_potenial_friend = [
                this_potenial_friend_id, this_potenial_friend_name,
                this_potenial_friend_avatar, this_potenial_friend_introction
            ]
            if this_potenial_friend not in potenialfriendlist:
                potenialfriendlist.append(this_potenial_friend)
                cnt += 1

    return render_template('friendlist.html',
                           friendlist=friendlist,
                           potenialfriendlist=potenialfriendlist)
