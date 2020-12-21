import os, re
from app import app, db, login
from app.mycenter import mycenter_app
# from app.mycenter.models import MycenterInfo
from .models import MycenterInfo
from app.myblog.models import myblog_info
from app.account_manage.models import user_account
from app.focus_manage.models import focus
from app.mycenter.forms import MyCenterEditForm
from flask import redirect, url_for, flash, render_template, request, session
from flask_login import login_user, logout_user, current_user, login_required
import imghdr
from PIL import Image
from werkzeug.utils import secure_filename


@login.user_loader
def load_user(id):
    return user_account.query.get(id)


def uploadheader(formname, user):
    size = (1024, 1024)
    (width, height) = (800, 800)
    no_input = "''"
    if repr(request.files[formname].filename) != no_input:
        new_profilephoto = request.files[formname]
        valid_filetype = imghdr.what(new_profilephoto)
        fname = new_profilephoto.filename
        ftype = fname.split('.')[1]
        filename = str(user.id) + "_" + str(formname) + "." + str(ftype)
        if valid_filetype:
            im = Image.open(new_profilephoto)
            im.thumbnail(size)
            im = im.resize((width, height), Image.ANTIALIAS)
            basedir = os.path.join(os.path.dirname(__file__), "..")
            upload_path = os.path.join(basedir, 'static/images', filename)
            im.save(upload_path)
            dbsave = os.path.join("/images/" + filename)
            print(dbsave)
            print("$$$")
            return dbsave, 1
        else:
            return None, -10
    return None, 0


def uploadpicwall(formname, user):
    size = (1024, 1024)
    (width, height) = (1200, 800)
    no_input = "''"
    if repr(request.files[formname].filename) != no_input:
        new_profilephoto = request.files[formname]
        valid_filetype = imghdr.what(new_profilephoto)
        fname = new_profilephoto.filename
        ftype = fname.split('.')[1]
        filename = str(user.id) + "_" + str(formname) + "." + str(ftype)
        if valid_filetype:
            im = Image.open(new_profilephoto)
            im.thumbnail(size)
            im = im.resize((width, height), Image.ANTIALIAS)
            basedir = os.path.join(os.path.dirname(__file__), "..")
            upload_path = os.path.join(basedir, 'static/images', filename)
            im.save(upload_path)
            dbsave = os.path.join("/images/" + filename)
            print(dbsave)
            print("$$$")
            return dbsave, 1
        else:
            return None, -10
    return None, 0


# 编辑照片墙
@mycenter_app.route('/mycenter/edit_imagewall', methods=['GET', 'POST'])
def mycenter_editimagewall():

    form = MyCenterEditForm()
    user = MycenterInfo.query.filter(
        MycenterInfo.id == current_user.get_id()).first()
    if request.method == 'POST':
        sav1, sta1 = uploadpicwall(formname="imagewall1", user=user)
        sav2, sta2 = uploadpicwall(formname="imagewall2", user=user)
        sav3, sta3 = uploadpicwall(formname="imagewall3", user=user)
        print(sav1, sav2, sav3, sta1, sta2, sta3)
        if sav1:
            print(sav1)
            user.picture1 = sav1
            db.session.commit()
        if sav2:
            user.picture2 = sav2
            db.session.commit()
        if sav3:
            user.picture3 = sav3
            db.session.commit()
        sta = sta1 + sta2 + sta3
        if sta < 0:
            flash("提交失败，图片必须是png，jpg格式，文件名不含中文")
        elif sta > 0:
            flash("提交成功")
    return render_template('mycenter_edit_imagewall.html',
                           user=user,
                           form=form)


# 编辑头像
@mycenter_app.route('/mycenter/edit_header', methods=['GET', 'POST'])
def mycenter_editheader():
    form = MyCenterEditForm()
    user = MycenterInfo.query.filter(
        MycenterInfo.id == current_user.get_id()).first()
    if request.method == 'POST':
        sav, sta = uploadheader(formname="header", user=user)
        if sav:
            user.header = sav
            db.session.commit()
        if sta < 0:
            flash("提交失败，图片必须是png，jpg格式，文件名不含中文")
        elif sta > 0:
            flash("提交成功")
    return render_template('mycenter_edit_header.html', user=user, form=form)

# 编辑个人信息
@mycenter_app.route('/mycenter/edit_myinfo', methods=['GET', 'POST'])
def mycenter_editmyinfo():
    editform=MyCenterEditForm()
    userinfo = load_user(current_user.get_id())
    myinfo = MycenterInfo.query.filter(
        MycenterInfo.id == userinfo.id
        ).first()
    if request.method=="POST":
        no_input=r"''"
        if editform.submit_gender.data:
            if editform.validate_on_submit():
                # 性别
                new_gender = editform.gender.data
                if repr(new_gender)!=no_input:
                    myinfo.gender = new_gender
                    db.session.commit()
                    flash("修改性别成功")
        elif editform.submit_age.data:
            if editform.validate_on_submit():
                # 年龄
                new_age = editform.age.data
                if repr(new_age)!= no_input:
                    myinfo.age = new_age
                    db.session.commit()
                    flash("修改年龄成功")
        elif editform.submit_agesub.data:
            if editform.validate_on_submit():
                # 年龄描述
                new_agesub = editform.agesub.data
                if repr(new_agesub)!=no_input:
                    myinfo.agesubintro = new_agesub
                    db.session.commit()
                    flash("修改年龄描述成功")
        elif editform.submit_major.data:
            if editform.validate_on_submit():
                # 专业
                new_major = editform.major.data
                if repr(new_major)!=no_input:
                    myinfo.major = new_major
                    db.session.commit()
                    flash("修改专业成功")
        elif editform.submit_majorsub.data:
            if editform.validate_on_submit():
                # 专业宣言
                new_majorsubintro = editform.majorsub.data
                if repr(new_majorsubintro)!=no_input:
                    myinfo.majorsubintro = new_majorsubintro
                    db.session.commit()
                    flash("修改专业宣言成功")
        elif editform.submit_hometown.data:
            if editform.validate_on_submit():
                # 家乡
                new_hometown = editform.hometown.data
                if repr(new_hometown)!=no_input:
                    myinfo.hometown = new_hometown
                    db.session.commit()
                    flash("修改家乡成功")
        elif editform.submit_hometownsub.data:
            if editform.validate_on_submit():
                # 家乡故事
                new_hometownsubintro = editform.hometownsub.data
                if repr(new_hometownsubintro)!=no_input:
                    myinfo.hometownsubintro = new_hometownsubintro
                    db.session.commit()
                    flash("修改家乡故事成功")
    return render_template('mycenter_edit_myinfo.html', form=editform, myinfo=myinfo)





# 编辑个人简介
@mycenter_app.route('/mycenter/edit_myprofile', methods=['GET', 'POST'])
def mycenter_editmyprofile():
    form = MyCenterEditForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            new_profile = form.introduction.data
            no_input = r"''"
            if repr(new_profile) != no_input:
                user = MycenterInfo.query.filter(
                    MycenterInfo.id == current_user.get_id()).first()
                user.introduction = new_profile
                db.session.commit()
                flash("修改成功")
    return render_template('mycenter_edit_myprofile.html', form=form)


# 显示个人中心
@mycenter_app.route('/mycenter/<user>', methods=['GET', 'POST'])
def mycenter(user):
    center_userinfo = user_account.query.filter(
        user_account.username == user).first()
    center_userid = center_userinfo.id
    # 是否为自己的个人中心
    isowner = False
    if center_userid == current_user.get_id():
        isowner = True
    # 是否已关注对方
    isfocus = False
    checklink = focus.query.filter(
        focus.focuser_id == current_user.get_id()
        and focus.focusee_id == center_userid).first()
    if checklink:
        isfocus = True
    center_usercenterinfo = MycenterInfo.query.filter(
        MycenterInfo.id == center_userid).first()
    center_userbloginfo = myblog_info.query.filter(
        myblog_info.user_id == center_userid).limit(4).all()  # 最近4条博客

    if (center_usercenterinfo.picture1):
        s1 = "background-image: url(../static" + center_usercenterinfo.picture1 + ");"
    else:
        s1 = "background-image: url(../static/images/picturewall_start1.jpg);"
    if (center_usercenterinfo.picture2):
        s2 = "background-image: url(../static" + center_usercenterinfo.picture1 + ");"
    else:
        s2 = "background-image: url(../static/images/picturewall_start2.jpg);"
    if (center_usercenterinfo.picture2):
        s3 = "background-image: url(../static" + center_usercenterinfo.picture1 + ");"
    else:
        s3 = "background-image: url(../static/images/picturewall_start3.jpg);"
    stylestrings = [s1, s2, s3]
    kwargs = {
        "center_usercenterinfo": center_usercenterinfo,
        "center_userinfo": center_userinfo,
        "center_userblogs": center_userbloginfo,
        "isowner": isowner,
        "stylestrings": stylestrings,
        "isfocus": isfocus,
    }
    # POST处理
    if not isowner:
        if request.method == "POST":
            if request.form['Action'] == '关注TA':
                # focus数据库处理
                if not checklink:
                    new_focus = focus(focuser_id=current_user.get_id(),
                                      focusee_id=center_userid)
                    db.session.add(new_focus)
                    db.session.commit()
                    flash("关注成功!")
                else:
                    flash("已关注!")
                return redirect(
                    url_for('mycenter_app.mycenter',
                            user=center_usercenterinfo.name))
            elif request.form['Action'] == '取关TA':
                # focus数据库处理
                if checklink:
                    db.session.delete(checklink)
                    db.session.commit()
                flash("取关成功!")
                return redirect(
                    url_for('mycenter_app.mycenter',
                            user=center_usercenterinfo.name))
            elif request.form['Action'] == '赞❤':
                flash("点赞成功!")
    else:
        if request.method == "POST":
            if request.form['Action'] == '赞❤':
                flash("给自己点赞成功:)")
    return render_template('mycenter.html', **kwargs)
