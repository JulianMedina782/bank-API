from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import User
from app.schemas.user import UserCreate, UserResponse, UserLogin
from app.utils import hashear_password
from app.auth import crear_token
from app.utils import verificar_password
from fastapi.security import OAuth2PasswordBearer
from app.auth import verificar_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/login")

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

@router.post("/login")
def login(usuario: UserLogin, db: Session = Depends(get_db)):
    
    db_user = db.query(User).filter(User.email == usuario.email).first()
    if not db_user:
        raise HTTPException(status_code=401, detail="Credenciales incorrectas")
    
    if not verificar_password(usuario.password, db_user.hashed_password):
        raise HTTPException(status_code=401, detail="Credenciales incorrectas")
    
    token = crear_token({"sub": str(db_user.id), "email": db_user.email})
    
    return {"access_token": token, "token_type": "bearer"}

@router.get("/me", response_model=UserResponse)
def obtener_usuario_actual(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    payload = verificar_token(token)
    user_id = payload.get("sub")
    
    usuario = db.query(User).filter(User.id == int(user_id)).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    return usuario