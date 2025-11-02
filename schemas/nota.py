from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class NotaBase(BaseModel):
    contenido: str
    peso: Optional[float] = None
    presion_sistolica: Optional[float] = None
    presion_diastolica: Optional[float] = None
    pulso: Optional[float] = None
    autor: Optional[str] = None

class NotaCreate(NotaBase):
    id_paciente: str

class NotaUpdate(BaseModel):
    contenido: Optional[str] = None
    peso: Optional[float] = None
    presion_sistolica: Optional[float] = None
    presion_diastolica: Optional[float] = None
    pulso: Optional[float] = None
    autor: Optional[str] = None

class Nota(NotaBase):
    id_nota: str
    id_paciente: str
    created_at: datetime

    class Config:
        from_attributes = True
