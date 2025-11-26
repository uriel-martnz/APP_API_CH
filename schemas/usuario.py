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
    apellidos: Optional[str] = None
    email: Optional[EmailStr] = None
    telefono: Optional[str] = None
    especialidad: Optional[str] = None

class ChangePassword(BaseModel):
    current_password: str
    new_password: str

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
