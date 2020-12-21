from app import app
from app.account_manage import account_bp
from app.mycenter import mycenter_app
from app.chatroom import chatroom_bp
from app.focus_manage import focus_bp
from app.myblog import myblog_bp
from app.bbs import bbs_bp
from app.todolist import todolist_bp

app.register_blueprint(account_bp)
app.register_blueprint(mycenter_app)
app.register_blueprint(focus_bp)
app.register_blueprint(chatroom_bp)
app.register_blueprint(myblog_bp)
app.register_blueprint(bbs_bp)
app.register_blueprint(todolist_bp)

if __name__ == '__main__':
    app.run(debug=True, host="127.0.0.1", port=5000)