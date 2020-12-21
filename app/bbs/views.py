import os, re
from app import app, db, login
from app.bbs import bbs_bp
from .models import bbs_post, bbs_comment
from app.account_manage.models import user_account
from app.mycenter.models import MycenterInfo
from .forms import AddPostForm, EditDeleteForm, AddCommentForm
from flask import redirect, url_for, flash, render_template, request, session, get_flashed_messages
from flask_login import login_user, logout_user, current_user, login_required


def setPaginate(page_num, per_page_num):
    page = int(request.args.get('page', page_num))
    per_page = int(request.args.get('per_page', per_page_num))
    return page, per_page


def deletePost(post, comments):
    for comment in comments:
        db.session.delete(comment)
        db.session.commit()
    db.session.delete(post)
    db.session.commit()
    return None


# # 通过id查询当前登陆用户
# @login.user_loader
# def load_user(id):
#     return user_account.query.get(id)

# # 论坛主页展示
# @bbs_bp.route('/bbs', methods=['GET', 'POST'])
# def bbs():
#     return render_template('bbs.html')


# 单个帖子展示
@bbs_bp.route('/singlepost/<post_id>', methods=['GET', 'POST'])
@login_required
def bbs_singlepost(post_id):
    post = bbs_post.query.get(int(post_id))
    if post == None:
        redirect(url_for('bbs.bbs_allpost'))
    edit_delete_form = EditDeleteForm()
    comment_form = AddCommentForm()
    comment_body = comment_form.comment.data
    comments = bbs_comment.query.filter(
        bbs_comment.post_id == post_id).order_by(bbs_comment.time.asc())
    cur_position = 0
    for comment in comments:
        cur_position = comment.position
    cur_position = cur_position + 1
    if edit_delete_form.validate_on_submit():
        if edit_delete_form.submitDelete.data:
            deletePost(post, comments)
            flash('删除成功', 'success')
            return redirect(url_for('bbs.bbs_myposts'))
        elif edit_delete_form.submitEdit.data:
            flash('开始编辑', 'info')
            return redirect(
                url_for('bbs.bbs_addpost', saved_post_id=post.post_id))
        elif comment_form.submitComment.data:
            # replied_position = comment_form.comment_replied_pos.data
            # if replied_position == None:
            #     replied_position = 0
            comment = bbs_comment(user_id=current_user.id,
                                  post_id=post_id,
                                  username=current_user.username,
                                  body=comment_body,
                                  position=cur_position)
            db.session.add(comment)
            db.session.commit()
            post.commentnum = post.commentnum + 1
            db.session.commit()
            flash('评论成功', 'success')
            return redirect(url_for('bbs.bbs_singlepost', post_id=post_id))
    center_usercenterinfo = MycenterInfo.query.filter(
        MycenterInfo.id == post.user_id).first()
    return render_template('bbs_singlepost.html',
                           title='BBS - 讨论详情',
                           post=post,
                           edit_delete_form=edit_delete_form,
                           comment_form=comment_form,
                           comments=comments,
                           curUser_ID=current_user.id,
                           center_usercenterinfo=center_usercenterinfo)


@bbs_bp.route('/allposts/')
@login_required
def bbs_allposts():
    all_posts = bbs_post.query.filter(1 == 1).order_by(bbs_post.time.desc())

    # print(type(all_posts))
    # flash(str(all_posts.count()))
    # print(all_posts)
    page, per_page = setPaginate(1, 5)
    paginate1 = all_posts.paginate(page, per_page, error_out=False)
    postsAll = paginate1.items

    return render_template("bbs_allposts.html",
                           title='论坛 - 全部讨论',
                           posts=all_posts,
                           paginate=paginate1,
                           postsAll=postsAll)


@bbs_bp.route('/myposts/')
@login_required
def bbs_myposts():
    if current_user.is_authenticated:
        all_posts = bbs_post.query.filter(
            bbs_post.user_id == current_user.id).order_by(bbs_post.time.desc())
    else:
        flash('请先登录！', 'danger')
        return redirect(url_for('account.login'))
    page, per_page = setPaginate(1, 5)
    paginate1 = all_posts.paginate(page, per_page, error_out=False)
    # posts = paginate1.items
    return render_template('bbs_myposts.html',
                           title='BBS - 我的讨论',
                           posts=all_posts,
                           paginate=paginate1)


# 发帖
@bbs_bp.route('/addpost',
              defaults={'saved_post_id': None},
              methods=['GET', 'POST'])
@bbs_bp.route('/addpost/<saved_post_id>', methods=['GET', 'POST'])
@login_required
def bbs_addpost(saved_post_id):
    form = AddPostForm()
    if saved_post_id:
        post_id = saved_post_id
        saved_post = bbs_post.query.get(int(saved_post_id))
        form.topic.data = saved_post.head
        form.content.data = saved_post.comment_body
    else:
        post_id = None
    if form.validate_on_submit():

        flash('发布成功')  #, 'success'
        # message = get_flashed_messages(with_categories=True)
        # for a in message:
        #     flash('111:' + str(a[0]))
        if saved_post_id:
            db.session.delete(saved_post)
            db.session.commit()
        post = bbs_post(post_id=post_id,
                        head=form.topic.data,
                        body=form.content.data,
                        user_id=current_user.id,
                        username=current_user.username)
        db.session.add(post)
        db.session.commit()
        post_id = post.post_id
        return redirect(url_for('bbs.bbs_singlepost', post_id=post_id))  #
    else:
        if form.errors:
            flash("some error occurred!", 'danger')
    return render_template('bbspost.html', title='论坛 - 发起讨论', form=form)
