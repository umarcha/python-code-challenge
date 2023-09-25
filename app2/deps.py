from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from .security import verify_token

token_url = "/token"
oauth2_scheme = OAuth2PasswordBearer(tokenUrl=token_url)

def get_current_user(token: str = Depends(oauth2_scheme)):
    return verify_token(token)
