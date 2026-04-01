# run.py
print(">>> 1. 程序开始启动...")

try:
    from app import create_app, db
    print(">>> 2. 成功导入 app 模块")
except Exception as e:
    print(f"!!! 导入模块失败: {e}")
    exit()

print(">>> 3. 正在创建 Flask 应用实例...")
app = create_app()
print(">>> 4. Flask 应用实例创建完成")

if __name__ == '__main__':
    print(">>> 5. 进入主程序入口")
    try:
        with app.app_context():
            print(">>> 6. 正在尝试连接数据库 (如果卡在这里，说明数据库配置不对)...")
            # 这行代码会自动根据你的模型创建数据库表
            db.create_all()
            print(">>> 7. 数据库连接成功，表结构检查/创建完毕！")
    except Exception as e:
        print(f"!!! 数据库操作失败: {e}")
        print("请检查 config.py 里的密码、端口、数据库名是否正确，以及 MySQL 是否已启动。")
        exit()

    print(">>> 8. 正在启动 Flask 服务器...")
    app.run(host='0.0.0.0', port=5000)