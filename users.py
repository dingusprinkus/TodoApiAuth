from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from auth import create_access_token, hash_password
from database import get_db
from models import User
from schemas import UserCreate, UserLogin, UserResponse

router = APIRouter()


@router.post("/register", response_model=UserResponse)
def register(user: UserCreate, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == user.username).first()
    if user:
        raise HTTPException(status_code=400, detail="Usuario ja cadastrado")

    hashed = hash_password(user.password)

    new_user = User(
        username=user.username,
        hPassword=hashed,
        email=user.email,
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return user


@router.post("/login", response_model=UserLogin)
def login(user: UserLogin, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.username == user.username).first()

    if not db_user or not verify_pw(user.password, db_user.hPassword):
        raise HTTPException(status_code=401, detail="Usuario ou senha incorretos")

    access_token = create_access_token({"sub": db_user.username})

    return {"access_token": access_token, "token_type": "bearer"}
