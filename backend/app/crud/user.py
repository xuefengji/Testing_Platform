from sqlalchemy.orm import Session
from sqlalchemy import select, or_
from app.models.user import User

def get_user_by_email(db: Session, email: str) -> User | None:
    """根据邮箱查找用户"""
    return db.scalar(select(User).where(User.email == email))

def get_user_by_name(db: Session, name: str) -> User | None:
    """根据用户名查找用户"""
    return db.scalar(select(User).where(User.name == name))

def get_user_by_name_or_email(db: Session, identifier: str) -> User | None:
    """根据用户名或邮箱查找用户（支持邮箱或用户名登录）"""
    return db.scalar(select(User).where(
        or_(User.email == identifier, User.name == identifier)
    ))

def get_user_by_id(db: Session, user_id: int) -> User | None:
    return db.scalar(select(User).where(User.id == user_id))
