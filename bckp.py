from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

users = {
    "srajansoni400@gmail.com": {"fullname": "Srajan Soni", "password": "12345678"},
    "user2@example.com": {"fullname": "User Two", "password": "password2"},
}

class UserSignup(BaseModel):
    fullname: str
    email: str
    password: str

class UserLogin(BaseModel):
    email: str
    password: str

@app.post("/signup/")
async def signup(user: UserSignup):
    if user.email in users:
        raise HTTPException(status_code=400, detail="Email already registered")
    else:
        users[user.email] = {"fullname": user.fullname, "password": user.password}
        return {"message": "Signup successful", "user": user}

@app.post("/login/")
async def login(user: UserLogin):
    if user.email in users and users[user.email]["password"] == user.password:
        return {"message": "Login successful", "user": users[user.email]}
    else:
        raise HTTPException(status_code=401, detail="Invalid email or password")
