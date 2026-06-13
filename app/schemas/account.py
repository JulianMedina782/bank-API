from pydantic import BaseModel
from datetime import datetime
from decimal import Decimal

class AccountCreate(BaseModel):
    tipo: str

class AccountResponse(BaseModel):
    id: int
    numero_cuenta: str
    tipo: str
    saldo: Decimal
    activo: bool
    creado_en: datetime
    user_id: int
    class Config: 
        from_attributes = True