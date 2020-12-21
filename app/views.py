from app import app
from flask import render_template #,request
#from .forms import *
from .models import *

@app.route('/about')
def html_about():
    return render_template('about.html')
@app.route('/base')
def html_base():
    return render_template('base.html')
@app.route('/blog')
def html_blog():
    return render_template('blog.html')
@app.route('/contact')
def html_contact():
    return render_template('contact.html')
@app.route('/forum')
def html_forum():
    return render_template('forum.html')
@app.route('/friendlist')
def html_friendlist():
    return render_template('friendlist.html')
@app.route('/index')
def html_index():
    return render_template('index.html')
@app.route('/login')
def html_login():
    return render_template('login.html')
@app.route('/myblog')
def html_myblog():
    return render_template('myblog.html')
# @app.route('/mycenter')
# def html_mycenter():
#     return render_template('mycenter.html')
@app.route('/portfolio')
def html_portfolio():
    return render_template('portfolio.html')
@app.route('/post')
def html_post():
    return render_template('post.html')
@app.route('/')
def html_signup_index():
    return render_template('signup_index.html')
@app.route('/single_post')
def html_single_post():
    return render_template('single_post.html')
@app.route('/todolist')
def html_todolist():
    return render_template('todolist.html')
@app.route('/blogedit')
def html_blogedit():
    return render_template('blogedit.html')
# @app.route('/mycenter-edit')
# def html_mycenteredit():
#     return render_template('mycenter-edit.html')

