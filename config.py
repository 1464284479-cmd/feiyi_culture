import os


class Config:

    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:wys20050727@127.0.0.1:3306/feiyi_db?charset=utf8mb4'

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = 'your-secret-key'  # 保持不变