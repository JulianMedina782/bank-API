from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional


class UserCreate(BaseModel):
    email: EmailStr
    password: str
    nombre: str

class UserResponse(BaseModel):
    id: int
    nombre: str
    email: EmailStr
    activo: bool
    creado_en: datetime
    class Config:
        from_attributes = True
     

class UserLogin(BaseModel):
    email: EmailStr
    password: str