# feiyi_culture

项目已整理为单仓库结构：

- `backend/`：Flask 后端
- `frontend/`：Vue 3 + Vite 前端

## 本地启动

后端：

```bash
cd backend
python -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
PORT=5000 python run.py
```

后端支持通过 `DATABASE_URL` 覆盖数据库连接；未设置时默认使用 `backend/feiyi.db`。

前端：

```bash
cd frontend
npm install --legacy-peer-deps
VITE_API_PROXY_TARGET=http://127.0.0.1:5000 npm run dev
```

如需修改端口，可设置：

- `PORT`：后端端口
- `VITE_PORT`：前端端口
- `VITE_API_PROXY_TARGET`：前端代理到的后端地址
