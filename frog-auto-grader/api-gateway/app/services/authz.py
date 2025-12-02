from enum import Enum
from fastapi import HTTPException, Depends, status
from typing import Iterable
from app.schemas import AuthUser
from app.deps import current_user

class Role(str, Enum):
    ADMIN = "ADMIN"
    PROFESSOR = "PROFESSOR"
    STUDENT = "STUDENT"

def has_any_role(user_roles: Iterable[str], allowed: Iterable[str]) -> bool:
    s = set(user_roles or [])
    return any(r in s for r in allowed)

def require_roles(*allowed: Role):
    """
    Uso:
      @router.post(..., dependencies=[Depends(require_roles(Role.ADMIN))])
    """
    allowed_str = [r.value if isinstance(r, Role) else str(r) for r in allowed]
    def _inner(user: AuthUser = Depends(current_user)) -> AuthUser:
        if not has_any_role(user.roles, allowed_str):
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Insuficientes permisos")
        return user
    return _inner