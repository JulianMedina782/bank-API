from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.account import Account
from app.models.transaction import Transaction
from app.schemas.transaction import TransactionCreate, TransactionResponse, TransferCreate
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

@router.post("/transfer", response_model=TransactionResponse)
def transfer(
    transaccion: TransferCreate,
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    payload = verificar_token(token)
    user_id = int(payload.get("sub"))

    cuenta_salida = db.query(Account).filter(
        Account.id == transaccion.account_id_origen,
        Account.user_id == user_id
    ).first()
    if not cuenta_salida:
        raise HTTPException(status_code=404, detail="Cuenta no encontrada")
    
    cuenta_entrada = db.query(Account).filter(
        Account.id == transaccion.account_id_destino,
    ).first()
    if not cuenta_entrada:
        raise HTTPException(status_code=404, detail="Cuenta no encontrada")
    
    if transaccion.account_id_origen == transaccion.account_id_destino:
         raise HTTPException(status_code=400, detail="Las cuentas deben ser diferentes")

    if cuenta_salida.saldo < transaccion.monto:
         raise HTTPException(status_code=400, detail="Saldo insuficiente")
    
    cuenta_salida.saldo -= transaccion.monto
    db.add(cuenta_salida)

    cuenta_entrada.saldo += transaccion.monto
    db.add(cuenta_entrada)

    trans_salida = Transaction(
        tipo="transferencia_salida",
        monto=transaccion.monto,
        descripcion=transaccion.descripcion,
        account_id=transaccion.account_id_origen
    )
    trans_entrada = Transaction(
        tipo="transferencia_entrada",
        monto=transaccion.monto,
        descripcion=transaccion.descripcion,
        account_id=transaccion.account_id_destino
    )
    db.add(trans_salida)
    db.add(trans_entrada)
    db.commit()
    db.refresh(trans_salida)
    return trans_salida