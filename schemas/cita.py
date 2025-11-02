from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class CitaBase(BaseModel):
    id_paciente: str
    fecha: datetime
    hora: str
    motivo: Optional[str] = None
    doctor: Optional[str] = None

class CitaCreate(CitaBase):
    pass

class CitaUpdate(BaseModel):
    fecha: Optional[datetime] = None
    hora: Optional[str] = None
    motivo: Optional[str] = None
    doctor: Optional[str] = None
    estado: Optional[str] = None

class Cita(CitaBase):
    id_cita: str
    estado: str
    created_at: datetime

    class Config:
        from_attributes = True
