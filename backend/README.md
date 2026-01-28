# FastAPI Backend

## 安装依赖

首先需要安装项目依赖：

```bash
cd backend
pip install -r requirements.txt
```

或者使用 python3：

```bash
cd backend
python3 -m pip install -r requirements.txt
```

**重要提示**：如果使用 MySQL 8.0+，需要确保安装了 `cryptography` 包（已包含在 requirements.txt 中）：
```bash
pip install cryptography
```

## 启动方式

### 方式一：使用启动脚本（推荐）

**Windows:**
```bash
cd backend
run.bat
```

**或者直接运行 Python 脚本:**
```bash
cd backend
python run.py
```

### 方式二：使用 uvicorn 命令

```bash
cd backend
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 方式三：使用 Python 模块方式

```bash
cd backend
python -m uvicorn app.main:app --reload
```

## 重要提示

⚠️ **必须在 `backend` 目录下运行**，否则会出现 `ModuleNotFoundError: No module named 'app'` 错误。

## 环境配置

### 数据库配置

1. 确保 MySQL 服务已启动
2. 创建数据库（如果不存在）：
   ```sql
   CREATE DATABASE autotest_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
   ```

3. 创建 `.env` 文件在 `backend` 目录下，配置以下环境变量：

```env
# ===== App Configuration =====
APP_NAME=AutoTest API

# ===== MySQL Database Configuration =====
MYSQL_HOST=127.0.0.1
MYSQL_PORT=3306
MYSQL_USER=root
MYSQL_PASSWORD=your_password
MYSQL_DB=autotest_db

# ===== JWT Configuration =====
JWT_SECRET=your-secret-key-change-this-in-production
JWT_ALG=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7
```

**注意**：
- 如果数据库连接失败，应用仍会启动，但会显示警告信息
- 请确保 MySQL 用户名和密码正确
- 如果使用默认配置（root/root），请确保 MySQL root 用户的密码确实是 "root"

## API 文档

启动后访问：
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc
- 健康检查: http://localhost:8000/health
