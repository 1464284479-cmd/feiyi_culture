# app/__init__.py
print("--- Init: 开始读取 __init__.py ---")
import pymysql
pymysql.install_as_MySQLdb()

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from config import Config

print("--- Init: 导入库完成，准备初始化 SQLAlchemy ---")
db = SQLAlchemy()

print("--- Init: 定义 create_app 函数 ---")
def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    CORS(app, resources={r"/api/*": {"origins": "*"}})

    # 注意：如果你的 import 放到了函数外面，这里可能会卡住
    print("--- Init: 正在导入 models ---")
    from app import models

    with app.app_context():
        db.create_all()

    print("--- Init: 正在导入 routes ---")
    from app.routes import bp
    app.register_blueprint(bp)

    return app

print("--- Init: 读取完毕 ---")