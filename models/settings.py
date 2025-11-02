from sqlalchemy import Column, String, Boolean, Integer, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from db.database import Base
from datetime import datetime

class Settings(Base):
    __tablename__ = "settings"

    id_settings = Column(String, primary_key=True, index=True)
    id_usuario = Column(String, ForeignKey("usuarios.id_usuario"), unique=True, nullable=False)
    modo_oscuro = Column(Boolean, default=False)
    notificaciones_activas = Column(Boolean, default=True)
    minutos_recordatorio = Column(Integer, default=30)  # minutos antes de la cita
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    usuario = relationship("Usuario", back_populates="settings")
