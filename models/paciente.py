from sqlalchemy import Column, String, Date, ForeignKey, Boolean, DateTime
from sqlalchemy.orm import relationship
from db.database import Base
from datetime import datetime

class Paciente(Base):
    __tablename__ = "pacientes"

    id_paciente = Column(String, primary_key=True, index=True)
    id_usuario = Column(String, ForeignKey("usuarios.id_usuario"), nullable=False)
    nombre = Column(String, nullable=False)
    apellidos = Column(String, nullable=False)
    fecha_nacimiento = Column(Date, nullable=False)
    sexo = Column(String, nullable=False)
    telefono = Column(String)
    email = Column(String)
    direccion = Column(String)
    estado = Column(String, default="activo")  # activo/inactivo
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    usuario = relationship("Usuario", back_populates="pacientes")
    citas = relationship("Cita", back_populates="paciente", cascade="all, delete-orphan")
    notas = relationship("Nota", back_populates="paciente", cascade="all, delete-orphan")
    fotos = relationship("Foto", back_populates="paciente", cascade="all, delete-orphan")
