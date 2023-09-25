from fastapi import APIRouter, HTTPException, Depends, status
from .models import User, Post, PostID, Token
from .deps import get_current_user
from .security import create_token
import cachetools

router = APIRouter()

users_db = {}
posts_db = {}
cache = cachetools.TTLCache(maxsize=100, ttl=300)

@router.post("/signup")
def signup(user: User):
    if user.email in users_db:
        raise HTTPException(status_code=400, detail="Email already registered")
    users_db[user.email] = user
    return {"token": create_token(user.email)}

@router.post("/login")
def login(user: User):
    if user.email not in users_db or users_db[user.email].password != user.password:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return {"token": create_token(user.email)}

@router.post("/addPost")
def add_post(post: Post, email: str = Depends(get_current_user)):
    if len(post.text.encode('utf-8')) > 1e6:
        raise HTTPException(status_code=413, detail="Payload too large")
    post_id = len(posts_db) + 1
    posts_db[post_id] = post
    return {"post_id": post_id}

@router.get("/getPosts")
def get_posts(email: str = Depends(get_current_user)):
    if email in cache:
        return cache[email]
    user_posts = [post for post in posts_db.values() if post.user_email == email]
    cache[email] = user_posts
    return user_posts

@router.post("/deletePost")
def delete_post(post_id: PostID, email: str = Depends(get_current_user)):
    if post_id.post_id not in posts_db or posts_db[post_id.post_id].user_email != email:
        raise HTTPException(status_code=404, detail="Post not found")
    del posts_db[post_id.post_id]
    if email in cache:
        del cache[email]
    return {"status": "Post deleted successfully"}
