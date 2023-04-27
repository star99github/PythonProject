
"""
应用的包构造文件，放入了初始化扩展的代码，创建并返回程序实例
"""

import os, sys
from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy


app_obj = Flask(__name__)  # 构建应用实例对象

app_obj.config["SECRET_KEY"] = "dev"
# 把 app.root_path 添加到 os.path.dirname() 中,以便把文件定位到项目根目录
app_obj.config["SQLALCHEMY_DATABASE_URI"] = os.path.join(os.path.dirname(app_obj.root_path), "data.db")
app_obj.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db_obj = SQLAlchemy(app_obj)
login_manager = LoginManager(app_obj)
login_manager.login_view = "login"


@login_manager.user_loader
def load_user(user_id):
    from .models import User
    user = User.query.get(int(user_id))
    return user


@app_obj.context_processor
def inject_user():
    from .models import User
    user = User.query.first()
    return dict(user=user)


# 注册视图函数：视图函数必须在应用对象创建之后导入，由于模板模块中同时也要导入构造文件中的程序实例，为了避免循环依赖（A 导入 B，B 导入 A），
# 把这一行导入语句放到构造文件的结尾。同样的，load_user() 函数和 inject_user() 函数中使用的模型类也在函数内进行导入。
import Account

