from datetime import datetime, timedelta
from typing import Optional
from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt
from passlib.context import CryptContext
from database import users_collection
from models import RegisterRequest, LoginRequest, TokenResponse, OnboardingRequest

router = APIRouter(prefix="/auth", tags=["auth"])

SECRET_KEY = "micro-learning-secret-key-2024-very-secure"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_DAYS = 7

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
security = HTTPBearer()


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(days=ACCESS_TOKEN_EXPIRE_DAYS))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise HTTPException(status_code=401, detail="Invalid token")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

    user = await users_collection.find_one({"email": email})
    if user is None:
        raise HTTPException(status_code=401, detail="User not found")
    user["_id"] = str(user["_id"])
    return user


@router.post("/register")
async def register(req: RegisterRequest):
    existing = await users_collection.find_one({"email": req.email})
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed_password = pwd_context.hash(req.password)
    user_doc = {
        "name": req.name,
        "email": req.email,
        "password": hashed_password,
        "level": None,
        "interests": [],
        "xp": 0,
        "streak": 0,
        "last_active": None,
        "created_at": datetime.utcnow(),
    }
    result = await users_collection.insert_one(user_doc)
    token = create_access_token(data={"sub": req.email})
    return {"access_token": token, "token_type": "bearer", "user_id": str(result.inserted_id)}


@router.post("/login")
async def login(req: LoginRequest):
    user = await users_collection.find_one({"email": req.email})
    if not user or not pwd_context.verify(req.password, user["password"]):
        raise HTTPException(status_code=401, detail="Invalid email or password")

    token = create_access_token(data={"sub": req.email})
    return {
        "access_token": token,
        "token_type": "bearer",
        "user_id": str(user["_id"]),
        "has_onboarded": bool(user.get("level")),
    }


@router.post("/onboarding")
async def onboarding(req: OnboardingRequest, user=Depends(get_current_user)):
    await users_collection.update_one(
        {"email": user["email"]},
        {"$set": {"interests": req.interests, "level": req.level}},
    )
    return {"message": "Onboarding complete"}


@router.get("/me")
async def get_me(user=Depends(get_current_user)):
    user.pop("password", None)
    return user
