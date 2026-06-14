from sqlalchemy import Column, Integer, String, Boolean, DateTime, Numeric, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base

class Transaction(Base):
    __tablename__ = "transactions"
    id = Column(Integer, primary_key=True, index=True)
    tipo = Column(String, nullable=False)
    monto = Column(Numeric(precision=15, scale=2), default=0)
    descripcion = Column(String, nullable=False)
    creado_en = Column(DateTime(timezone=True), server_default=func.now())
    account_id = Column(Integer, ForeignKey("accounts.id"), nullable=False)
    cuenta = relationship("Account", back_populates="transacciones")
