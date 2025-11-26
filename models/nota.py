from sqlalchemy import Column, String, DateTime, ForeignKey, Text, Date, JSON
from sqlalchemy.orm import relationship
from db.database import Base
from datetime import datetime

class Nota(Base):
    __tablename__ = "notas"

    id_nota = Column(String, primary_key=True, index=True)
    id_paciente = Column(String, ForeignKey("pacientes.id_paciente"), nullable=False)
    fecha = Column(Date, nullable=False)
    motivo_consulta = Column(Text)
    sintomas = Column(Text)
    diagnostico = Column(Text, nullable=False)
    tratamiento = Column(Text)
    observaciones = Column(Text)
    signos_vitales = Column(JSON)  # JSON object with vital signs
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    paciente = relationship("Paciente", back_populates="notas")
