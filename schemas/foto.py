from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class FotoBase(BaseModel):
    descripcion: Optional[str] = None

class FotoCreate(FotoBase):
    id_paciente: str
    id_usuario: str
    url: str
    nombre_archivo: str

class Foto(FotoBase):
    id_foto: str
    id_paciente: str
    id_usuario: str
    url: str
    nombre_archivo: str
    created_at: datetime

    class Config:
        from_attributes = True
