from alembic import op
import sqlalchemy as sa
import bcrypt

# revision identifiers
revision = "init_admin"
down_revision = "f3194ebff74a"
branch_labels = None
depends_on = None


def upgrade():
    conn = op.get_bind()

    # 1️⃣ 准备 admin 数据
    admin_email = "admin@example.com"
    admin_name = "admin"
    # 直接使用 bcrypt 库，避免 passlib 初始化问题
    password = "Admin@123456"
    salt = bcrypt.gensalt()
    admin_password_hash = bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')

    # 2️⃣ 插入 admin 用户（如果不存在）
    result = conn.execute(
        sa.text("SELECT id FROM user WHERE email = :email"),
        {"email": admin_email},
    ).fetchone()

    if result is None:
        conn.execute(
            sa.text("""
                INSERT INTO user (email, name, password_hash, is_disabled)
                VALUES (:email, :name, :password_hash, 0)
            """),
            {
                "email": admin_email,
                "name": admin_name,
                "password_hash": admin_password_hash,
            },
        )

    # 3️⃣ 确保有默认项目
    project = conn.execute(
        sa.text("SELECT id FROM project WHERE name = 'Default Project'")
    ).fetchone()

    if project is None:
        conn.execute(
            sa.text("INSERT INTO project (name) VALUES ('Default Project')")
        )
        project_id = conn.execute(
            sa.text("SELECT LAST_INSERT_ID()")
        ).scalar()
    else:
        project_id = project.id

    # 4️⃣ 绑定 admin 为 project_admin
    admin_id = conn.execute(
        sa.text("SELECT id FROM user WHERE email = :email"),
        {"email": admin_email},
    ).scalar()

    member = conn.execute(
        sa.text("""
            SELECT id FROM project_member
            WHERE project_id = :pid AND user_id = :uid
        """),
        {"pid": project_id, "uid": admin_id},
    ).fetchone()

    if member is None:
        conn.execute(
            sa.text("""
                INSERT INTO project_member (project_id, user_id, role)
                VALUES (:pid, :uid, 'project_admin')
            """),
            {"pid": project_id, "uid": admin_id},
        )


def downgrade():
    # 一般不删除 admin（避免误删生产数据）
    pass
