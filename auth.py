from datetime import datetime, timedelta, timezone

import jwt
from pwdlib import PasswordHash

SECRET_KEY = "_w1f+0&u_l@r_$*n0!3b^j9tf6)#kv&+y$7($7qbov48pc3="
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


pw_hash = PasswordHash.recommended()


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


# token = create_access_token({"test": "w"})
# print(token)
# payload = decode_access_token(token)
# payload = decode_access_token("asdasdsada")
# print(payload)
# senha = hash_password("senha123")
# print(verify_password("senha123", senha))
# print(verify_password("senha1234", senha))
