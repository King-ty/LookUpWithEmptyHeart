import os, re
from app import app, db, login
from app.myblog import myblog_bp
from app.myblog.models import myblog_info
from app.bbs.models import bbs_post
from app.mycenter.models import MycenterInfo
from app.account_manage.models import user_account
from app.myblog.forms import MyblogEditForm
from flask import redirect, url_for, flash, render_template, request, session
from flask_login import login_user, logout_user, current_user, login_required
import imghdr
from PIL import Image
from werkzeug.utils import secure_filename


#### 通过用户id查询当前登陆用户
@login.user_loader
def load_user(id):
    return user_account.query.get(id)


# 个人博客展示 及 单个博客跳转进入
@myblog_bp.route('/myblog/<userid>', methods=['GET', 'POST'])
def myblog(userid):
    bloginfo = myblog_info.query.filter(
        myblog_info.user_id == userid).all()  # 博客表的一个查询视图
    userinfo = load_user(userid)
    usercenterinfo = MycenterInfo.query.filter(MycenterInfo.id == userid).first()
    isowner = False
    if userid == current_user.get_id():
        isowner = True
    kwargs = {
        "blogs": bloginfo,
        "username": userinfo.username,
        "isowner": isowner,
        "usercenterinfo": usercenterinfo,
    }
    return render_template('blog.html', **kwargs)


''' **kwargs使用示例
@app.route("/")
def index():
    products = ["iphoneX", "MacBook Pro", "Huawei"]
    kwargs = {
        "products": products
    }
    return flask.render_template("for.html", **kwargs)
'''


def uploadblogpic(formname, blog):
    size = (1024, 1024)
    (width, height) = (1200, 800)
    no_input = "''"
    if repr(request.files[formname].filename) != no_input:
        new_profilephoto = request.files[formname]
        valid_filetype = imghdr.what(new_profilephoto)
        fname = new_profilephoto.filename
        ftype = fname.split('.')[1]
        filename = blog + "_" + str(formname) + "." + str(ftype)
        if valid_filetype:
            im = Image.open(new_profilephoto)
            im.thumbnail(size)
            im = im.resize((width, height), Image.ANTIALIAS)
            basedir = os.path.join(os.path.dirname(__file__), "..")
            upload_path = os.path.join(basedir, 'static/images', filename)
            im.save(upload_path)
            dbsave = os.path.join("/images/" + filename)
            # print(dbsave)
            # print("$$$")
            return dbsave, 1
        else:
            return None, -10
    return None, 0


# 写博客
@myblog_bp.route('/myblogedit', methods=['GET', 'POST'])
def myblogedit():
    blogform = MyblogEditForm()
    #userinfo = load_user(current_user.get_id())
    bloginfo = str(current_user.get_id()) + str(myblog_info.query.count())

    if request.method == 'POST':
        # flash(u"test: 进入POST")
        if blogform.validate_on_submit():  # 所有表单数据合法且不为空
            # flash(u"test: 进入validate")
            newbloghead = blogform.head.data
            newblogbody = blogform.body.data
            newblogopen = blogform.openstate.data
            sav1, sta1 = uploadblogpic(formname="img1", blog=bloginfo)
            sav2, sta2 = uploadblogpic(formname="img2", blog=bloginfo)
            sav3, sta3 = uploadblogpic(formname="img3", blog=bloginfo)

            sta = sta1 + sta2 + sta3
            # if sta<0:
            #     flash("提交失败，图片必须是png，jpg格式，文件名不含中文")
            # elif sta>0:
            #     flash("提交成功")
            newblog = myblog_info(user_id=current_user.get_id(),
                                  head=newbloghead,
                                  body=newblogbody,
                                  openstate=newblogopen,
                                  img1=sav1,
                                  img2=sav2,
                                  img3=sav3)
            db.session.add(newblog)
            db.session.commit()
            flash("博客提交成功")
            if blogform.openstate.data:  # 选择将博客公开，将该博客插入论坛数据表
                newpost = bbs_post(
                    user_id=current_user.get_id(),
                    head=newbloghead,
                    body=newblogbody,
                    username=load_user(current_user.get_id()).username,
                )
                db.session.add(newpost)
                db.session.commit()
                flash("同步至论坛成功")
            return redirect(
                url_for('myblog.myblog_index',
                        userid=current_user.id,
                        index=myblog_info.query.count()))
        else:
            print(blogform.errors)
        # 处理上载图片
        # pass
    return render_template('blogedit.html', blogform=blogform)


# 单个博客页面
@myblog_bp.route('/myblog/<userid>/<int:index>', methods=['GET', 'POST'])
def myblog_index(userid, index):  #index是blog_id
    bloginfo = myblog_info.query.filter(
        myblog_info.id == index).first()  # 数据库中搜索目标博客
    userinfo = load_user(userid)  # 得到作者信息
    isowner = False
    if userid == current_user.get_id():
        # print("test")
        isowner = True
    # print(userid)
    # print(current_user.get_id())
    # print(isowner)
    kwargs = {
        "userid": userid,
        "author": userinfo.username,
        "time": bloginfo.time,
        "likenum": bloginfo.likenum,
        "head": bloginfo.head,
        "body": bloginfo.body,
        "openstate": bloginfo.openstate,
        "isowner": isowner,
        "single_bloginfo": bloginfo
    }
    # 接收到删除此博客命令
    if request.method == 'POST':
        # print(request.form['Action'])
        if request.form['Action'] == '删除此博客':
            # print('delete')
            db.session.delete(bloginfo)
            db.session.commit()
            flash("删除成功!")
            return redirect(url_for('myblog.myblog', userid=userid))
        else:
            # print('like')
            bloginfo.likenum = bloginfo.likenum + 1
            db.session.commit()
            flash("点赞成功!")
    return render_template('blogsingle.html', **kwargs)
