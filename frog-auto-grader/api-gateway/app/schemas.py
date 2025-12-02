from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from typing import Optional, List

class AuthUser(BaseModel):
    uid: str
    email: Optional[str] = None
    roles: List[str] = []

class UserOut(BaseModel):
    uid: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[str] = None
    username: str
    active: bool
    last_update: Optional[datetime] = None
    roles: List[str] = []

# Alias de compatibilidad
StaffOut = UserOut

class TokenOut(BaseModel):
    access_token: str
    token_type: str = "bearer"

class MeOut(BaseModel):
    user: StaffOut
    token: TokenOut
    roles: List[str] = []