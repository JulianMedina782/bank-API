from sqlalchemy import Column, Integer, String, Boolean, DateTime, Numeric, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base

class Account(Base):   
    __tablename__ = "accounts"
    id = Column(Integer, primary_key=True, index=True)
    numero_cuenta = Column(String(20), nullable=False, unique=True)
    tipo = Column(String, nullable=False)
    saldo = Column(Numeric(precision=15, scale=2), default=0)
    activo = Column(Boolean, default=True)
    creado_en = Column(DateTime(timezone=True), server_default=func.now())
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    usuario = relationship("User", back_populates="cuentas")