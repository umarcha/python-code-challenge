from pydantic import BaseModel, EmailStr

class User(BaseModel):
    email: EmailStr
    password: str

class Post(BaseModel):
    text: str
    user_email: EmailStr

class PostID(BaseModel):
    post_id: int

class Token(BaseModel):
    token: str

class TokenData(BaseModel):
    email: EmailStr = None
