from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse

router = APIRouter()

# Simuler une base de données d'utilisateurs
fake_users_db = {}

@router.post("/register")
def register(user: dict):
    email = user.get("email")
    if email in fake_users_db:
        raise HTTPException(status_code=400, detail="User already exists")
    fake_users_db[email] = user
    return JSONResponse(status_code=201, content={"message": "User registered"})

@router.post("/login")
def login(user: dict):
    email = user.get("email")
    password = user.get("password")
    if email not in fake_users_db or fake_users_db[email].get("password") != password:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return {"access_token": "fake-jwt-token", "token_type": "bearer"}