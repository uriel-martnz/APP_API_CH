from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class UsuarioBase(BaseModel):
    email: EmailStr
    nombre: str
    rol: Optional[str] = "medico"

class UsuarioCreate(UsuarioBase):
    contrasena: str

class UsuarioUpdate(BaseModel):
    nombre: Optional[str] = None
    contrasena: Optional[str] = None

class UsuarioLogin(BaseModel):
    email: EmailStr
    contrasena: str

class Usuario(UsuarioBase):
    id_usuario: str
    created_at: datetime

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None
