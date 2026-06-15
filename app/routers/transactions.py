from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.account import Account
from app.models.transaction import Transaction
from app.schemas.transaction import TransactionCreate, TransactionResponse
from fastapi.security import OAuth2PasswordBearer
from app.auth import verificar_token
from typing import List

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/login")

router = APIRouter(
    prefix="/transactions",
    tags=["transactions"]
)
@router.post("/deposit", response_model=TransactionResponse)
def deposit(
    transaccion: TransactionCreate,
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    payload = verificar_token(token)
    user_id = int(payload.get("sub"))

    cuenta = db.query(Account).filter(
        Account.id == transaccion.account_id,
        Account.user_id == user_id
    ).first()
    if not cuenta:
        raise HTTPException(status_code=404, detail="Cuenta no encontrada")
    
    cuenta.saldo += transaccion.monto
    db.add(cuenta)
    
    nueva_transaccion = Transaction(
        tipo=transaccion.tipo,
        monto=transaccion.monto,
        descripcion=transaccion.descripcion,
        account_id=transaccion.account_id
    )
    
    db.add(nueva_transaccion)
    db.commit()
    db.refresh(nueva_transaccion)
    return nueva_transaccion
    
@router.post("/withdraw", response_model=TransactionResponse)
def withdraw(
    transaccion: TransactionCreate,
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    payload = verificar_token(token)
    user_id = int(payload.get("sub"))

    cuenta = db.query(Account).filter(
        Account.id == transaccion.account_id,
        Account.user_id == user_id
    ).first()
    if not cuenta:
        raise HTTPException(status_code=404, detail="Cuenta no encontrada")
    
    if cuenta.saldo < transaccion.monto:
        raise HTTPException(status_code=400, detail="Saldo insuficiente")
    
    cuenta.saldo -= transaccion.monto
    db.add(cuenta)
    
    nueva_transaccion = Transaction(
        tipo=transaccion.tipo,
        monto=transaccion.monto,
        descripcion=transaccion.descripcion,
        account_id=transaccion.account_id
    )
    
    db.add(nueva_transaccion)
    db.commit()
    db.refresh(nueva_transaccion)
    return nueva_transaccion

@router.get("/history/{account_id}", response_model=List[TransactionResponse])
def historial(
    account_id: int,
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    payload = verificar_token(token)
    user_id = int(payload.get("sub"))

    cuenta = db.query(Account).filter(
        Account.id == account_id,
        Account.user_id == user_id
    ).first()
    if not cuenta:
        raise HTTPException(status_code=404, detail="Cuenta no encontrada")
    
    transacciones = db.query(Transaction).filter(Transaction.account_id == account_id).all()

    return transacciones