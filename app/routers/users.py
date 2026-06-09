from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import User
from app.schemas.user import UserCreate, UserResponse
from app.utils import hashear_password

router = APIRouter(
    prefix="/users",
    tags=["users"]
)

@router.post("/register", response_model=UserResponse)
def registrar_usuario(usuario: UserCreate, db: Session = Depends(get_db)):
    
    db_user = db.query(User).filter(User.email == usuario.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="El email ya está registrado")
    
    nuevo_usuario = User(
        nombre=usuario.nombre,
        email=usuario.email,
        hashed_password=hashear_password(usuario.password)
    )
    
    db.add(nuevo_usuario)
    db.commit()
    db.refresh(nuevo_usuario)
    
    return nuevo_usuario