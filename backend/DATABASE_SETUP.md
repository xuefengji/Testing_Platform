# 数据库配置指南

## 问题：数据库连接失败

如果看到以下错误：
```
⚠️ Database connection failed: Access denied for user 'root'@'localhost'
```

## 解决步骤

### 1. 检查 MySQL 服务是否运行

**Windows:**
```powershell
# 检查 MySQL 服务状态
Get-Service -Name MySQL*

# 如果服务未运行，启动服务
Start-Service -Name MySQL80  # 根据你的 MySQL 版本调整服务名
```

**或者通过服务管理器：**
- 按 `Win + R`，输入 `services.msc`
- 找到 MySQL 服务，确保状态为"正在运行"

### 2. 验证 MySQL root 密码

连接到 MySQL 并测试密码：
```bash
mysql -u root -p
```

如果无法连接，可能需要：
- 重置 root 密码
- 或者使用其他有权限的用户

### 3. 创建数据库

连接到 MySQL 后，执行：
```sql
CREATE DATABASE IF NOT EXISTS autotest_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

### 4. 配置 .env 文件

在 `backend` 目录下创建或更新 `.env` 文件：

```env
# ===== MySQL Database Configuration =====
MYSQL_HOST=localhost
MYSQL_PORT=3306
MYSQL_USER=root
MYSQL_PASSWORD=你的实际MySQL密码
MYSQL_DB=autotest
```

**注意**：数据库名是 `autotest`（不是 `autotest_db`）

### 5. 测试数据库连接

在 `backend` 目录下运行测试脚本：
```bash
cd backend
python test_db_connection.py
```

### 6. 重启应用

修改 `.env` 后，重启 FastAPI 应用。

## 临时解决方案（开发环境）

如果暂时不需要数据库，应用仍然可以运行：
- API 文档可以访问：http://localhost:8000/docs
- 健康检查可以访问：http://localhost:8000/health
- 但需要数据库的 API 端点会失败

## 常见问题

### Q: 忘记 MySQL root 密码怎么办？

**Windows:**
1. 停止 MySQL 服务
2. 使用 `--skip-grant-tables` 启动 MySQL
3. 重置密码
4. 重启 MySQL 服务

详细步骤请参考 MySQL 官方文档。

### Q: 如何创建新的 MySQL 用户？

```sql
CREATE USER 'autotest_user'@'localhost' IDENTIFIED BY 'your_password';
GRANT ALL PRIVILEGES ON autotest.* TO 'autotest_user'@'localhost';
FLUSH PRIVILEGES;
```

然后在 `.env` 中使用新用户：
```env
MYSQL_USER=autotest_user
MYSQL_PASSWORD=your_password
```
