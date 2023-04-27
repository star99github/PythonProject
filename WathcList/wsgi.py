# 设置环境变量并导入程序实例


import os
from dotenv import load_dotenv

dotenv_path = os.path.join(os.path.dirname(__file__), ".env")
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)


from WatchList import app_obj


app_obj.run()  # 默认启动内置服务器，监听地址为本地的5000端口，默认返回界面为 404 页面无法找到
# app.run(port=2020, host="127.0.0.1", debug=True, theaded=True)  # 调用run方法启动服务，自定义服务器地址和端口号，debug：代码更新是否自动重启，theaded：是否开启多线程

