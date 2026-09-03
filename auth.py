from datetime import datetime, timedelta, timezone
from database import get_db

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2, OAuth2PasswordBearer
import jwt
from pwdlib import PasswordHash

from models import User

SECRET_KEY = "_w1f+0&u_l@r_$*n0!3b^j9tf6)#kv&+y$7($7qbov48pc3="
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


pw_hash = PasswordHash.recommended()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


def hash_password(password):
    hashed = pw_hash.hash(password)
    return hashed


def verify_password(password, hashed_pw):
    is_correct = pw_hash.verify(password, hashed_pw)
    return is_correct


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def decode_access_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None


def get_curr_user(token: str = Depends(oauth2_scheme), db=Depends(get_db)):
    payload = decode_access_token(token)
    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Token  Invalido"
        )

    username = payload.get("sub")

    user = db.query(User).filter(User.username == username).first()

    if user is None:
        raise HTTPException(status_code=401, detail="Usuario  nao encontrado")


# token = create_access_token({"test": "w"})
# print(token)
# payload = decode_access_token(token)
# payload = decode_access_token("asdasdsada")
# print(payload)
# senha = hash_password("senha123")
# print(verify_password("senha123", senha))
# print(verify_password("senha1234", senha))
