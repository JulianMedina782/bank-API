from pydantic import BaseModel
from datetime import datetime
from decimal import Decimal

class TransactionCreate(BaseModel):
    tipo: str
    monto: Decimal
    descripcion: str
    account_id: int

class TransactionResponse(BaseModel):
    id: int
    tipo: str
    monto: Decimal
    descripcion: str
    creado_en: datetime
    account_id: int
    class Config:
        from_attributes = True