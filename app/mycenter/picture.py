from app import db
from flask import request, render_template, redirect, url_for, flash, session, Blueprint
from app.models import user_login,user_info
import os
import sys
from datetime import timedelta
import uuid
from functools import wraps
#======================================================
#辅助函数
# 1.0设置允许的文件格式
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'JPG', 'PNG', 'bmp'])

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

# 1.1图片上传相关方法，用于修改照片墙和修改头像
#choice 1 2 3->mycenter/picturewall 0->header
def upload_pic(userid, choice):
    user = user_info.query.filter(user_info.id == userid).first()
    f = request.files['file']
    if not (f and allowed_file(f.filename)):
        flash(u"请检查上传的图片类型，仅限于png、jpg、bmp", 'warning')
        return 0
    else:
        # 路径获取
        basepath = os.path.dirname(__file__)
        ext = os.path.splitext(f.filename)[1]
        new_filename = str(uuid.uuid1()) + ext
        # 注意：没有的文件夹一定要先创建，不然会提示没有该路径
        if choice >= 1 & choice <=3:       
            upload_path = os.path.join(basepath, '../static/images',
                                new_filename)
        elif choice == 0:
            upload_path = os.path.join(basepath, '../static/head_images',
                                new_filename)
        # 保存图片
        f.save(upload_path)  
        # 删除原来的图片 
        if choice==1:#照片1，可能是默认照片
            if user.picture1 and user.picture1 != '/static/images/picturewall_start.jpg':  
                del_path = os.path.join(basepath, '../static/', user.picture1)
                if os.path.exists(del_path):
                    os.remove(del_path)
            user.picture1 = 'images/' + new_filename
        if choice==2:#照片2
            if user.picture2:  
                del_path = os.path.join(basepath, '../static/', user.picture2)
                if os.path.exists(del_path):
                    os.remove(del_path)
            user.picture1 = 'images/' + new_filename
        if choice==3:#照片3
            if user.picture1:  
                del_path = os.path.join(basepath, '../static/', user.picture3)
                if os.path.exists(del_path):
                    os.remove(del_path)
            user.picture1 = 'images/' + new_filename
        elif choice==0:#头像
            if user.head and user.head != '../static/images/header_start.jpg':             
                del_path = os.path.join(basepath, '../static/', user.header)
                if os.path.exists(del_path):
                    os.remove(del_path)
            user.head = 'images/' + new_filename
        db.session.commit()
        flash(u'上传成功！', 'success')
        return 1

