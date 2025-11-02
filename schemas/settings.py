from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class SettingsBase(BaseModel):
    modo_oscuro: Optional[bool] = False
    notificaciones_activas: Optional[bool] = True
    minutos_recordatorio: Optional[int] = 30

class SettingsCreate(SettingsBase):
    id_usuario: str

class SettingsUpdate(BaseModel):
    modo_oscuro: Optional[bool] = None
    notificaciones_activas: Optional[bool] = None
    minutos_recordatorio: Optional[int] = None

class Settings(SettingsBase):
    id_settings: str
    id_usuario: str
    created_at: datetime

    class Config:
        from_attributes = True
