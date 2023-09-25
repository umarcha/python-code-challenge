import jwt
from datetime import datetime, timedelta
from fastapi import HTTPException

TOKEN_SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"

def verify_token(token: str):
    try:
        payload = jwt.decode(token, TOKEN_SECRET_KEY, algorithms=["HS256"])
        email: str = payload.get("sub")
        if email is None:
            raise HTTPException(status_code=401, detail="Could not validate credentials")
        return email
    except:
        raise HTTPException(status_code=401, detail="Could not validate credentials")

def create_token(email: str):
    token_data = {"sub": email, "exp": datetime.utcnow() + timedelta(minutes=15)}
    token = jwt.encode(token_data, TOKEN_SECRET_KEY)
    return token
