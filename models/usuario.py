from sqlalchemy import Column, String, DateTime
from sqlalchemy.orm import relationship
from db.database import Base
from datetime import datetime

class Usuario(Base):
    __tablename__ = "usuarios"

    id_usuario = Column(String, primary_key=True, index=True)
    nombre = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    contrasena = Column(String, nullable=False)
    rol = Column(String, default="medico")
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    pacientes = relationship("Paciente", back_populates="usuario")
    fotos = relationship("Foto", back_populates="usuario")
    settings = relationship("Settings", back_populates="usuario", uselist=False)
