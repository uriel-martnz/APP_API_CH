from sqlalchemy import Column, String, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from db.database import Base
from datetime import datetime

class Foto(Base):
    __tablename__ = "fotos"

    id_foto = Column(String, primary_key=True, index=True)
    id_paciente = Column(String, ForeignKey("pacientes.id_paciente"), nullable=False)
    id_usuario = Column(String, ForeignKey("usuarios.id_usuario"), nullable=False)
    url = Column(String, nullable=False)
    descripcion = Column(Text)
    nombre_archivo = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    paciente = relationship("Paciente", back_populates="fotos")
    usuario = relationship("Usuario", back_populates="fotos")
