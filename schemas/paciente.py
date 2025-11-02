from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import date, datetime

class PacienteBase(BaseModel):
    nombre: str
    apellidos: str
    fecha_nacimiento: date
    sexo: str
    telefono: Optional[str] = None
    email: Optional[EmailStr] = None
    direccion: Optional[str] = None

class PacienteCreate(PacienteBase):
    pass

class PacienteUpdate(BaseModel):
    nombre: Optional[str] = None
    apellidos: Optional[str] = None
    fecha_nacimiento: Optional[date] = None
    sexo: Optional[str] = None
    telefono: Optional[str] = None
    email: Optional[EmailStr] = None
    direccion: Optional[str] = None
    estado: Optional[str] = None

class Paciente(PacienteBase):
    id_paciente: str
    id_usuario: str
    estado: str
    created_at: datetime

    class Config:
        from_attributes = True
