from pydantic import BaseModel
from typing import Optional, Dict, Any
from datetime import datetime, date

class SignosVitales(BaseModel):
    presion_sistolica: Optional[float] = None
    presion_diastolica: Optional[float] = None
    frecuencia_cardiaca: Optional[float] = None
    temperatura: Optional[float] = None
    peso: Optional[float] = None
    altura: Optional[float] = None
    saturacion_oxigeno: Optional[float] = None
    frecuencia_respiratoria: Optional[float] = None

class NotaBase(BaseModel):
    fecha: date
    motivo_consulta: Optional[str] = None
    sintomas: Optional[str] = None
    diagnostico: str
    tratamiento: Optional[str] = None
    observaciones: Optional[str] = None
    signos_vitales: Optional[Dict[str, Any]] = None

class NotaCreate(NotaBase):
    pass

class NotaUpdate(BaseModel):
    fecha: Optional[date] = None
    motivo_consulta: Optional[str] = None
    sintomas: Optional[str] = None
    diagnostico: Optional[str] = None
    tratamiento: Optional[str] = None
    observaciones: Optional[str] = None
    signos_vitales: Optional[Dict[str, Any]] = None

class Nota(NotaBase):
    id_nota: str
    id_paciente: str
    created_at: datetime

    class Config:
        from_attributes = True
