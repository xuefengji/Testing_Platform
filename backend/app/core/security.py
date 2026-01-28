from datetime import datetime, timedelta, timezone
import jwt
import hashlib
from app.core.config import settings

# bcrypt 限制：密码不能超过 72 字节
BCRYPT_MAX_LENGTH = 72

# 延迟导入和初始化 CryptContext，避免初始化时的 bug 检测问题
_pwd_context = None
_use_direct_bcrypt = False

def get_pwd_context():
    """获取密码上下文，延迟初始化以避免初始化时的 bug 检测"""
    global _pwd_context, _use_direct_bcrypt
    if _pwd_context is None:
        try:
            from passlib.context import CryptContext
            # 尝试初始化 CryptContext
            # 如果失败，我们将使用直接的 bcrypt 库
            _pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
            # 测试是否正常工作
            test_hash = _pwd_context.hash("test")
            _pwd_context.verify("test", test_hash)
        except (ValueError, Exception) as e:
            # 如果 passlib 初始化失败，使用直接的 bcrypt 库作为备选
            try:
                import bcrypt
                _use_direct_bcrypt = True
                _pwd_context = None  # 不使用 passlib
            except ImportError:
                raise RuntimeError(
                    f"Failed to initialize password hashing. "
                    f"Both passlib and bcrypt libraries failed. Error: {e}"
                )
    return _pwd_context

def _hash_with_bcrypt(password: str) -> str:
    """直接使用 bcrypt 库哈希密码"""
    import bcrypt
    password_bytes = password.encode('utf-8')
    if len(password_bytes) > BCRYPT_MAX_LENGTH:
        # 超过 72 字节，先 SHA256
        password_bytes = hashlib.sha256(password_bytes).hexdigest().encode('utf-8')
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password_bytes, salt)
    return hashed.decode('utf-8')

def _verify_with_bcrypt(password: str, hashed: str) -> bool:
    """直接使用 bcrypt 库验证密码"""
    import bcrypt
    password_bytes = password.encode('utf-8')
    
    # 尝试新格式（SHA256 预处理）
    if len(password_bytes) > BCRYPT_MAX_LENGTH:
        prepared = hashlib.sha256(password_bytes).hexdigest().encode('utf-8')
        try:
            return bcrypt.checkpw(prepared, hashed.encode('utf-8'))
        except Exception:
            pass
        # 尝试旧格式（截断）
        try:
            truncated = password_bytes[:BCRYPT_MAX_LENGTH]
            return bcrypt.checkpw(truncated, hashed.encode('utf-8'))
        except Exception:
            return False
    else:
        try:
            return bcrypt.checkpw(password_bytes, hashed.encode('utf-8'))
        except Exception:
            return False

def _prepare_password(password: str) -> str:
    """
    准备密码以符合 bcrypt 的 72 字节限制
    如果密码超过 72 字节，先进行 SHA256 哈希（转为十六进制字符串）
    """
    password_bytes = password.encode('utf-8')
    if len(password_bytes) > BCRYPT_MAX_LENGTH:
        # 如果密码超过 72 字节，先进行 SHA256 哈希，然后转为十六进制字符串
        # 这样确保长度不超过 72 字节（SHA256 十六进制字符串是 64 字符）
        return hashlib.sha256(password_bytes).hexdigest()
    return password

def hash_password(pw: str) -> str:
    """哈希密码，自动处理超过 72 字节的情况"""
    if _use_direct_bcrypt:
        return _hash_with_bcrypt(pw)
    prepared = _prepare_password(pw)
    return get_pwd_context().hash(prepared)

def verify_password(pw: str, hashed: str) -> bool:
    """
    验证密码，自动处理超过 72 字节的情况
    支持两种格式：
    1. 新格式：超过 72 字节的密码先 SHA256 哈希（转为十六进制），再 bcrypt
    2. 旧格式：直接截断到 72 字节后 bcrypt（向后兼容）
    """
    if _use_direct_bcrypt:
        return _verify_with_bcrypt(pw, hashed)
    
    password_bytes = pw.encode('utf-8')
    context = get_pwd_context()
    
    # 如果密码超过 72 字节，尝试新格式（SHA256 预处理）
    if len(password_bytes) > BCRYPT_MAX_LENGTH:
        try:
            # 新格式：先 SHA256 再 bcrypt（转为十六进制字符串）
            prepared = hashlib.sha256(password_bytes).hexdigest()
            if context.verify(prepared, hashed):
                return True
        except Exception:
            pass
        
        # 如果新格式失败，尝试旧格式（截断）
        try:
            truncated = pw[:BCRYPT_MAX_LENGTH]
            return context.verify(truncated, hashed)
        except Exception:
            return False
    else:
        # 密码不超过 72 字节，直接验证
        try:
            return context.verify(pw, hashed)
        except Exception:
            return False

def create_token(payload: dict, expires_delta: timedelta) -> str:
    now = datetime.now(timezone.utc)
    to_encode = payload.copy()
    to_encode.update({"iat": int(now.timestamp()), "exp": int((now + expires_delta).timestamp())})
    return jwt.encode(to_encode, settings.JWT_SECRET, algorithm=settings.JWT_ALG)

def create_access_token(user_id: int, project_id: int | None, roles: list[str]) -> str:
    payload = {"sub": str(user_id), "pid": project_id, "roles": roles, "typ": "access"}
    return create_token(payload, timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES))

def create_refresh_token(user_id: int) -> str:
    payload = {"sub": str(user_id), "typ": "refresh"}
    return create_token(payload, timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS))

def decode_token(token: str) -> dict:
    return jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.JWT_ALG])
