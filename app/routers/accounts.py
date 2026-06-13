from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.account import Account
from app.schemas.account import AccountCreate, AccountResponse
from fastapi.security import OAuth2PasswordBearer
from app.auth import verificar_token
import uuid

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/login")

router = APIRouter(
    prefix="/accounts",
    tags=["accounts"]
)

@router.post("/", response_model=AccountResponse)
def crear_cuenta(
    cuenta: AccountCreate,
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    payload = verificar_token(token)
    user_id = int(payload.get("sub"))
    
    numero_cuenta = str(uuid.uuid4())[:12].upper()
    
    nueva_cuenta = Account(
        numero_cuenta=numero_cuenta,
        tipo=cuenta.tipo,
        user_id=user_id
    )
    
    db.add(nueva_cuenta)
    db.commit()
    db.refresh(nueva_cuenta)
    
    return nueva_cuenta